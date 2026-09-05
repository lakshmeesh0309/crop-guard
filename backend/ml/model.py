import torch
import torch.nn as nn
import torchvision.models as models

class CropGuardMobileNet(nn.Module):
    def __init__(self, num_classes=38, pretrained=True):
        super(CropGuardMobileNet, self).__init__()
        # Use newer weights API if available, fallback to pretrained=True
        if pretrained:
            try:
                weights = models.MobileNet_V3_Large_Weights.IMAGENET1K_V1
                self.backbone = models.mobilenet_v3_large(weights=weights)
            except AttributeError:
                # Support older torchvision versions
                try:
                    self.backbone = models.mobilenet_v3_large(pretrained=True)
                except Exception:
                    self.backbone = models.mobilenet_v3_large(pretrained=False)
        else:
            try:
                self.backbone = models.mobilenet_v3_large(weights=None)
            except TypeError:
                self.backbone = models.mobilenet_v3_large(pretrained=False)
            
        # Replace the final classification layer of the mobilenet_v3_large classifier
        # The classifier of mobilenet_v3_large is a Sequential block:
        # classifier[0]: Linear(960, 1280)
        # classifier[1]: Hardswish
        # classifier[2]: Dropout
        # classifier[3]: Linear(1280, 1000)
        in_features = self.backbone.classifier[3].in_features
        self.backbone.classifier[3] = nn.Linear(in_features, num_classes)

    def forward(self, x):
        return self.backbone(x)
