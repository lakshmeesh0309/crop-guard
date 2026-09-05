import os
import sys
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets
from model import CropGuardMobileNet
from train import DatasetFromSubset

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(base_dir, "dataset")
    model_path = os.path.join(base_dir, "models", "cropguard_hybrid.pth")
    report_path = os.path.join(base_dir, "models", "evaluation_report.json")
    
    if not os.path.exists(model_path):
        print(f"[ERROR] Model file not found at {model_path}. Train the model first.")
        sys.exit(1)
        
    data_dir = dataset_dir
    found_dirs = False
    for root, dirs, files in os.walk(dataset_dir):
        if len(dirs) >= 15:
            data_dir = root
            found_dirs = True
            break
            
    if not found_dirs:
        print(f"[ERROR] Could not find class directories inside {dataset_dir}.")
        sys.exit(1)
        
    print(f"[Evaluation] Using data directory: {data_dir}")
    full_dataset = datasets.ImageFolder(data_dir, transform=None)
    classes = full_dataset.classes
    num_classes = len(classes)
    
    # Replicate training split seed to get the exact same test split
    total_len = len(full_dataset)
    train_len = int(0.7 * total_len)
    val_len = int(0.15 * total_len)
    test_len = total_len - train_len - val_len
    
    _, _, test_set = random_split(
        full_dataset, [train_len, val_len, test_len],
        generator=torch.Generator().manual_seed(42)
    )
    
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    test_dataset = DatasetFromSubset(test_set, transform=val_transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Evaluation] Loading model and running evaluation on {device}...")
    
    model = CropGuardMobileNet(num_classes=num_classes, pretrained=False)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    
    all_preds = []
    all_targets = []
    
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = outputs.max(1)
            all_preds.extend(preds.cpu().numpy().tolist())
            all_targets.extend(targets.numpy().tolist())
            
    # Compute accuracy
    correct = sum(1 for p, t in zip(all_preds, all_targets) if p == t)
    total = len(all_targets)
    accuracy = correct / total if total > 0 else 0.0
    
    # Calculate precision, recall, f1 per class
    report = {
        "overall_accuracy": accuracy,
        "total_test_samples": total,
        "class_metrics": {}
    }
    
    for i, class_name in enumerate(classes):
        tp = sum(1 for p, t in zip(all_preds, all_targets) if p == i and t == i)
        fp = sum(1 for p, t in zip(all_preds, all_targets) if p == i and t != i)
        fn = sum(1 for p, t in zip(all_preds, all_targets) if p != i and t == i)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        report["class_metrics"][class_name] = {
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "support": sum(1 for t in all_targets if t == i)
        }
        
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"[Evaluation] Report saved to {report_path}")
    print(f"[Evaluation] Overall Accuracy: {accuracy*100:.2f}%")

if __name__ == "__main__":
    main()
