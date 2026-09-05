import os
import io
import json
import threading
import PIL.Image

# Lazy importing of PyTorch to keep startup times fast
torch = None
transforms = None
CropGuardMobileNet = None

_model = None
_labels = None
_lock = threading.Lock()

def _init_pytorch():
    global torch, transforms, CropGuardMobileNet
    if torch is None:
        import torch as t
        from torchvision import transforms as tf
        from ml.model import CropGuardMobileNet as net
        torch = t
        transforms = tf
        CropGuardMobileNet = net

def get_labels():
    global _labels
    if _labels is not None:
        return _labels
        
    base_dir = os.path.dirname(os.path.abspath(__file__))
    labels_path = os.path.join(base_dir, "labels.json")
    if os.path.exists(labels_path):
        try:
            with open(labels_path, "r") as f:
                _labels = json.load(f)
        except Exception as e:
            print(f"[Inference] Error loading labels.json: {e}")
            _labels = []
    else:
        print("[Inference] Warning: labels.json not found.")
        _labels = []
    return _labels

def get_model():
    global _model, _lock
    with _lock:
        if _model is not None:
            return _model

        _init_pytorch()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Check TorchScript (.pt) first
        pt_path = os.path.join(base_dir, "models", "cropguard_hybrid.pt")
        # Check standard PyTorch (.pth) second
        pth_path = os.path.join(base_dir, "models", "cropguard_hybrid.pth")
        
        # Fallback search path in case running from backend root
        if not os.path.exists(pt_path) and not os.path.exists(pth_path):
            pt_path = os.path.join(os.path.dirname(base_dir), "models", "cropguard_hybrid.pt")
            pth_path = os.path.join(os.path.dirname(base_dir), "models", "cropguard_hybrid.pth")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if os.path.exists(pt_path):
            try:
                print(f"[Inference] Loading TorchScript model from {pt_path} on {device}...")
                _model = torch.jit.load(pt_path, map_location=device)
                _model.eval()
                print("[Inference] TorchScript model loaded successfully.")
                return _model
            except Exception as e:
                print(f"[Inference] Failed to load TorchScript model: {e}. Falling back to state dict...")

        if os.path.exists(pth_path):
            try:
                print(f"[Inference] Loading model state dict from {pth_path} on {device}...")
                labels = get_labels()
                num_classes = len(labels) if labels else 38
                model = CropGuardMobileNet(num_classes=num_classes, pretrained=False)
                model.load_state_dict(torch.load(pth_path, map_location=device))
                model.to(device)
                model.eval()
                _model = model
                print("[Inference] Model state dict loaded successfully.")
                return _model
            except Exception as e:
                print(f"[Inference] Failed to load model state dict: {e}")
                
        print("[Inference] No trained model weights found yet. Local model prediction will be skipped.")
        return None

def predict(image_bytes: bytes) -> dict | None:
    """
    Runs local MobileNetV3 model prediction on the given image.
    Returns: {
        "crop": str (standardized),
        "disease": str (standardized),
        "confidence": float (0-100),
        "class_index": int,
        "display_crop": str,
        "display_disease": str
    } or None if model is not loaded/fails.
    """
    try:
        model = get_model()
        if model is None:
            return None

        # Prepare transform
        _init_pytorch()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        eval_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # Load image
        img = PIL.Image.open(io.BytesIO(image_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Transform and add batch dimension
        tensor = eval_transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            conf, class_idx = torch.max(probabilities, dim=0)
            
            # Extract top 5 classifications
            labels = get_labels()
            top5 = []
            if labels:
                topk_probs, topk_indices = torch.topk(probabilities, min(5, len(labels)))
                for p_val, idx_val in zip(topk_probs, topk_indices):
                    p_pct = float(p_val.item()) * 100.0
                    idx_int = int(idx_val.item())
                    if idx_int < len(labels):
                        top5.append({
                            "crop": labels[idx_int]["crop"],
                            "disease": labels[idx_int]["disease"],
                            "confidence": round(p_pct, 1)
                        })

        class_idx_int = int(class_idx.item())
        confidence_pct = float(conf.item()) * 100.0

        if labels and class_idx_int < len(labels):
            label_info = labels[class_idx_int]
            return {
                "crop": label_info["crop"],
                "disease": label_info["disease"],
                "confidence": round(confidence_pct, 1),
                "class_index": class_idx_int,
                "display_crop": label_info["display_crop"],
                "display_disease": label_info["display_disease"],
                "top5": top5
            }
        else:
            # Fallback if labels are empty
            return {
                "crop": "Unknown",
                "disease": f"Class {class_idx_int}",
                "confidence": round(confidence_pct, 1),
                "class_index": class_idx_int,
                "display_crop": "Unknown",
                "display_disease": f"Class {class_idx_int}",
                "top5": []
            }
            
    except Exception as e:
        print(f"[Inference ERROR] {e}")
        return None
