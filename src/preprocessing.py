"""
preprocessing.py
----------------
Reusable image preprocessing and augmentation utilities.

Input resolution : 224 x 224 (compatible with ResNet-18 and EfficientNet-B0)
Normalization    : ImageNet mean/std (both models use ImageNet-pretrained weights)
Augmentation     : training only; validation and test use deterministic transforms
"""

from torchvision import transforms

# ── Constants ────────────────────────────────────────────────────────────────

IMAGE_SIZE = 224

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

# ── Transform pipelines ──────────────────────────────────────────────────────

def get_train_transform() -> transforms.Compose:
    """
    Training pipeline:
      RandomResizedCrop  → mild random rotation → horizontal flip
      → color jitter → tensor → ImageNet normalization

    Augmentations are conservative to preserve cultivar-defining plant
    structures. Vertical flip is omitted because field images have a
    consistent ground-up orientation.
    """
    return transforms.Compose([
        transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.8, 1.0)),
        transforms.RandomRotation(degrees=10),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1, hue=0.05),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_val_transform() -> transforms.Compose:
    """
    Validation pipeline (deterministic):
      Resize → CenterCrop → tensor → ImageNet normalization
    """
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_test_transform() -> transforms.Compose:
    """
    Test pipeline (deterministic, identical to validation):
      Resize → CenterCrop → tensor → ImageNet normalization
    """
    return get_val_transform()
