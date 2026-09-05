import os
import sys
import argparse
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split, Dataset
from torchvision import transforms, datasets
from model import CropGuardMobileNet

class DatasetFromSubset(Dataset):
    def __init__(self, subset, transform=None):
        self.subset = subset
        self.transform = transform

    def __getitem__(self, index):
        img, label = self.subset[index]
        if self.transform:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.subset)

def parse_args():
    parser = argparse.ArgumentParser(description="Train CropGuard v4 MobileNetV3 Model")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--dataset-dir", type=str, default=None, help="Path to dataset directory")
    parser.add_argument("--model-path", type=str, default=None, help="Path to save the best model (.pth)")
    parser.add_argument("--kaggle-username", type=str, default=None, help="Kaggle username for download")
    parser.add_argument("--kaggle-key", type=str, default=None, help="Kaggle API key for download")
    return parser.parse_args()

def download_dataset(dataset_dir, username, key):
    print("[TRAIN STATUS] downloading 5")
    print(f"[Setup] Configuring Kaggle credentials...")
    kaggle_dir = os.path.join(os.path.expanduser("~"), ".kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)
    kaggle_json = os.path.join(kaggle_dir, "kaggle.json")
    with open(kaggle_json, "w") as f:
        f.write(f'{{"username":"{username}","key":"{key}"}}')
    
    # Windows/Linux permission handling
    try:
        os.chmod(kaggle_json, 0o600)
    except Exception:
        pass
        
    print("[TRAIN STATUS] downloading 10")
    print("[Download] Downloading abdallahalidev/plantvillage-dataset from Kaggle...")
    import subprocess
    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", "abdallahalidev/plantvillage-dataset",
         "-p", dataset_dir, "--unzip"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # Fallback to emmarex/plantdisease if abdallahalidev fails
        print("[Download] Primary dataset failed. Trying fallback emmarex/plantdisease...")
        result = subprocess.run(
            ["kaggle", "datasets", "download", "-d", "emmarex/plantdisease",
             "-p", dataset_dir, "--unzip"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Kaggle download failed"
            raise RuntimeError(f"Kaggle download failed: {error_msg}")

    print("[TRAIN STATUS] downloading 25")
    print("[Download] Dataset downloaded and extracted successfully.")

def main():
    args = parse_args()
    
    # Set default paths if not specified
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = args.dataset_dir or os.path.join(base_dir, "dataset")
    model_path = args.model_path or os.path.join(base_dir, "models", "cropguard_hybrid.pth")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Check if download is required
    if args.kaggle_username and args.kaggle_key:
        try:
            download_dataset(dataset_dir, args.kaggle_username, args.kaggle_key)
        except Exception as e:
            print(f"[ERROR] Dataset setup failed: {e}")
            sys.exit(1)

    print("[TRAIN STATUS] training 30")
    print("[Data] Scanning dataset directories...")
    # Find directory containing class folders (could be nested inside dataset_dir)
    data_dir = dataset_dir
    found_dirs = False
    for root, dirs, files in os.walk(dataset_dir):
        # We look for a folder containing many subdirectories representing classes
        if len(dirs) >= 15:
            data_dir = root
            found_dirs = True
            break
            
    if not found_dirs:
        print(f"[ERROR] Could not find class directories inside {dataset_dir}. Please download the dataset first.")
        sys.exit(1)

    print(f"[Data] Using data directory: {data_dir}")
    
    # Load dataset with ImageFolder (without transforms initially so we can split and apply different transforms)
    full_dataset = datasets.ImageFolder(data_dir, transform=None)
    classes = full_dataset.classes
    num_classes = len(classes)
    print(f"[Data] Found {num_classes} classes.")
    
    # Save classes to labels index json if it doesn't match labels.json, or just output
    print(f"[Data] Classes detected: {classes}")

    # Split dataset: 70% train, 15% val, 15% test
    total_len = len(full_dataset)
    train_len = int(0.7 * total_len)
    val_len = int(0.15 * total_len)
    test_len = total_len - train_len - val_len
    
    train_set, val_set, test_set = random_split(
        full_dataset, [train_len, val_len, test_len],
        generator=torch.Generator().manual_seed(42)
    )
    
    # Define augmentations
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # Wrap subsets in dataset loaders
    train_dataset = DatasetFromSubset(train_set, transform=train_transform)
    val_dataset = DatasetFromSubset(val_set, transform=val_transform)
    test_dataset = DatasetFromSubset(test_set, transform=val_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)
    
    print(f"[Data] Splits: Train={len(train_dataset)}, Val={len(val_dataset)}, Test={len(test_dataset)}")
    print("[TRAIN STATUS] training 40")
    
    # Setup Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Model] Using device: {device}")
    
    # Initialize Model
    model = CropGuardMobileNet(num_classes=num_classes, pretrained=True)
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    
    best_val_acc = 0.0
    
    print("[TRAIN STATUS] training 50")
    print("[Model] Starting training loop...")
    
    for epoch in range(args.epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        
        for batch_idx, (inputs, targets) in enumerate(train_loader):
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total_train += targets.size(0)
            correct_train += predicted.eq(targets).sum().item()
            
        epoch_train_loss = running_loss / len(train_dataset)
        epoch_train_acc = correct_train / total_train
        
        # Validation
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0
        
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item() * inputs.size(0)
                _, predicted = outputs.max(1)
                total_val += targets.size(0)
                correct_val += predicted.eq(targets).sum().item()
                
        epoch_val_loss = val_loss / len(val_dataset)
        epoch_val_acc = correct_val / total_val
        
        # Log status
        progress = 50 + int((epoch + 1) / args.epochs * 40) # map 50 to 90
        print(f"[TRAIN STATUS] training {progress}")
        print(f"[Epoch {epoch+1}/{args.epochs}] loss={epoch_train_loss:.4f} accuracy={epoch_train_acc:.4f} val_loss={epoch_val_loss:.4f} val_accuracy={epoch_val_acc:.4f}")
        
        # Save best model
        if epoch_val_acc > best_val_acc:
            best_val_acc = epoch_val_acc
            print(f"[Model] Val accuracy improved to {best_val_acc:.4f}. Saving checkpoint...")
            torch.save(model.state_dict(), model_path)
            
            # Also export to TorchScript for production inference speed if possible
            try:
                model.eval()
                example_input = torch.rand(1, 3, 224, 224).to(device)
                traced_script_module = torch.jit.trace(model, example_input)
                script_path = model_path.replace(".pth", ".pt")
                traced_script_module.save(script_path)
                print(f"[Model] Exported TorchScript model to {script_path}")
            except Exception as script_err:
                print(f"[Model] TorchScript export failed: {script_err}")
                
    print("[TRAIN STATUS] training 95")
    print(f"[Done] Training complete! Best validation accuracy: {best_val_acc*100:.2f}%")
    print(f"[Done] Saved best model weights to {model_path}")
    print("[TRAIN STATUS] training 100")

if __name__ == "__main__":
    main()
