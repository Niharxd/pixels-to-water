"""Train an ImageNet-pretrained ResNet-18 on the fixed sorghum split.

This script deliberately reads only the training and validation manifests.
It performs a small end-to-end sanity check before beginning full training.
"""

import copy
import json
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.optim import AdamW
from torchvision.models import ResNet18_Weights, resnet18

from dataset import SorghumDataset, build_class_to_idx, make_loader
from preprocessing import IMAGE_SIZE, get_train_transform, get_val_transform


SEED = 42
BATCH_SIZE = 32
MAX_EPOCHS = 20
LEARNING_RATE = 0.0001
WEIGHT_DECAY = 0.0001
PRETRAINED_WEIGHTS = "ResNet18_Weights.IMAGENET1K_V1"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"
MODELS_DIR = PROJECT_ROOT / "models"
TRAIN_MANIFEST = RESULTS_DIR / "train.csv"
VALIDATION_MANIFEST = RESULTS_DIR / "validation.csv"
IMAGE_DIR = PROJECT_ROOT.parent / "Dataset"


def set_seed(seed: int = SEED) -> None:
    """Set all relevant random seeds for reproducible training."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def build_model(num_classes: int, device: torch.device) -> nn.Module:
    """Load ResNet-18 ImageNet weights and replace its classifier."""
    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model.to(device)


def run_epoch(model, loader, criterion, device, optimizer=None):
    """Run one training epoch when optimizer is supplied, otherwise validate."""
    is_training = optimizer is not None
    model.train(is_training)
    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    context = torch.enable_grad() if is_training else torch.no_grad()
    with context:
        for images, labels in loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            if is_training:
                optimizer.zero_grad(set_to_none=True)
            outputs = model(images)
            loss = criterion(outputs, labels)
            if is_training:
                loss.backward()
                optimizer.step()

            batch_size = labels.size(0)
            total_loss += loss.item() * batch_size
            total_correct += (outputs.argmax(dim=1) == labels).sum().item()
            total_samples += batch_size

    return total_loss / total_samples, total_correct / total_samples


def sanity_check(model, train_loader, validation_loader, criterion, optimizer, device, num_classes):
    """Verify data, model, loss, and one optimizer step before full training."""
    train_images, train_labels = next(iter(train_loader))
    val_images, val_labels = next(iter(validation_loader))

    expected_shape = (3, IMAGE_SIZE, IMAGE_SIZE)
    for name, images, labels in (("training", train_images, train_labels), ("validation", val_images, val_labels)):
        if images.ndim != 4 or tuple(images.shape[1:]) != expected_shape:
            raise RuntimeError(f"{name} batch has unexpected image shape: {tuple(images.shape)}")
        if labels.ndim != 1 or not torch.all((labels >= 0) & (labels < num_classes)):
            raise RuntimeError(f"{name} batch contains invalid labels.")

    model.train()
    images, labels = train_images.to(device), train_labels.to(device)
    optimizer.zero_grad(set_to_none=True)
    outputs = model(images)
    if tuple(outputs.shape) != (images.shape[0], num_classes):
        raise RuntimeError(f"Unexpected model output shape: {tuple(outputs.shape)}")
    loss = criterion(outputs, labels)
    if not torch.isfinite(loss):
        raise RuntimeError("Sanity-check loss is not finite.")
    loss.backward()
    optimizer.step()

    return {
        "training_batch_shape": list(train_images.shape),
        "validation_batch_shape": list(val_images.shape),
        "labels_valid": True,
        "model_output_shape": list(outputs.shape),
        "loss_calculation_works": True,
        "backward_optimizer_step_works": True,
    }


def save_curves(history: pd.DataFrame, output_path: Path) -> None:
    """Save loss and accuracy learning curves."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(history["epoch"], history["train_loss"], label="Training")
    axes[0].plot(history["epoch"], history["val_loss"], label="Validation")
    axes[0].set(title="ResNet-18 Loss", xlabel="Epoch", ylabel="Cross-entropy loss")
    axes[1].plot(history["epoch"], history["train_accuracy"], label="Training")
    axes[1].plot(history["epoch"], history["val_accuracy"], label="Validation")
    axes[1].set(title="ResNet-18 Accuracy", xlabel="Epoch", ylabel="Accuracy")
    for axis in axes:
        axis.legend()
        axis.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def update_experiment_report(config: dict) -> None:
    """Replace the ResNet-18 section with results from this exact run."""
    report_path = PROJECT_ROOT / "reports" / "experiments.md"
    report = report_path.read_text(encoding="utf-8")
    heading = "# ResNet-18 Training"
    existing = report.find(heading)
    if existing != -1:
        report = report[:existing].rstrip() + "\n"

    observations = (
        "Training completed for the configured maximum of "
        f"{config['epochs_completed']} epochs. The selected checkpoint is from epoch "
        f"{config['best_epoch']} based on highest validation accuracy; validation loss "
        "was used as the tie-breaker."
    )
    section = f'''\n\n{heading}\n\n- Number of classes: {config['num_classes']}\n- Training samples: {config['training_samples']}\n- Validation samples: {config['validation_samples']}\n- Input size: {config['input_size']}\n- Pretrained weights: {config['pretrained_weights']}\n- Optimizer: {config['optimizer']}\n- Learning rate: {config['learning_rate']}\n- Batch size: {config['batch_size']}\n- Epochs completed: {config['epochs_completed']}\n- Best validation accuracy: {config['best_validation_accuracy']:.4f}\n- Best validation loss: {config['best_validation_loss']:.6f}\n- Best epoch: {config['best_epoch']}\n- Training observations: {observations}\n'''
    report_path.write_text(report.rstrip() + section, encoding="utf-8")


def main() -> None:
    set_seed()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    train_manifest = pd.read_csv(TRAIN_MANIFEST)
    validation_manifest = pd.read_csv(VALIDATION_MANIFEST)
    class_to_idx = build_class_to_idx(train_manifest)
    num_classes = len(class_to_idx)
    if not set(validation_manifest["cultivar"].unique()).issubset(class_to_idx):
        raise ValueError("Validation manifest contains cultivars absent from training manifest.")

    train_dataset = SorghumDataset(train_manifest, IMAGE_DIR, get_train_transform(), class_to_idx)
    validation_dataset = SorghumDataset(validation_manifest, IMAGE_DIR, get_val_transform(), class_to_idx)
    train_loader = make_loader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, seed=SEED)
    validation_loader = make_loader(validation_dataset, batch_size=BATCH_SIZE, shuffle=False, seed=SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Sanity check is intentionally isolated from the trained model state.
    sanity_model = build_model(num_classes, device)
    sanity_optimizer = AdamW(sanity_model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    criterion = nn.CrossEntropyLoss()
    sanity = sanity_check(sanity_model, train_loader, validation_loader, criterion, sanity_optimizer, device, num_classes)
    del sanity_model, sanity_optimizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    set_seed()
    model = build_model(num_classes, device)
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    history_rows = []
    best_accuracy = -float("inf")
    best_loss = float("inf")
    best_epoch = 0
    best_state = None

    print(f"Sanity check passed. Training on {device} for up to {MAX_EPOCHS} epochs.")
    for epoch in range(1, MAX_EPOCHS + 1):
        train_loss, train_accuracy = run_epoch(model, train_loader, criterion, device, optimizer)
        val_loss, val_accuracy = run_epoch(model, validation_loader, criterion, device)
        history_rows.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "val_loss": val_loss,
            "val_accuracy": val_accuracy,
        })
        print(
            f"Epoch {epoch:02d}/{MAX_EPOCHS} | train loss {train_loss:.4f}, acc {train_accuracy:.4f} "
            f"| val loss {val_loss:.4f}, acc {val_accuracy:.4f}"
        )
        if val_accuracy > best_accuracy or (val_accuracy == best_accuracy and val_loss < best_loss):
            best_accuracy, best_loss, best_epoch = val_accuracy, val_loss, epoch
            best_state = copy.deepcopy(model.state_dict())

    history = pd.DataFrame(history_rows, columns=["epoch", "train_loss", "train_accuracy", "val_loss", "val_accuracy"])
    history.to_csv(RESULTS_DIR / "resnet18_training_history.csv", index=False)
    save_curves(history, RESULTS_DIR / "resnet18_training_curves.png")
    torch.save({
        "model_state_dict": best_state,
        "model_name": "resnet18",
        "num_classes": num_classes,
        "class_to_idx": class_to_idx,
        "pretrained_weights": PRETRAINED_WEIGHTS,
        "best_epoch": best_epoch,
        "best_validation_accuracy": best_accuracy,
        "best_validation_loss": best_loss,
    }, MODELS_DIR / "resnet18_best.pth")

    config = {
        "model": "resnet18",
        "pretrained_weights": PRETRAINED_WEIGHTS,
        "device": str(device),
        "random_seed": SEED,
        "num_classes": num_classes,
        "training_samples": len(train_dataset),
        "validation_samples": len(validation_dataset),
        "input_size": [3, IMAGE_SIZE, IMAGE_SIZE],
        "loss_function": "CrossEntropyLoss",
        "optimizer": "AdamW",
        "learning_rate": LEARNING_RATE,
        "weight_decay": WEIGHT_DECAY,
        "batch_size": BATCH_SIZE,
        "maximum_epochs": MAX_EPOCHS,
        "epochs_completed": len(history),
        "best_epoch": best_epoch,
        "best_validation_accuracy": best_accuracy,
        "best_validation_loss": best_loss,
        "model_selection": "Highest validation accuracy; lowest validation loss breaks ties.",
        "test_set_used": False,
        "sanity_check": sanity,
    }
    (RESULTS_DIR / "resnet18_experiment_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    update_experiment_report(config)
    print(f"Best epoch: {best_epoch}; validation accuracy: {best_accuracy:.4f}; validation loss: {best_loss:.6f}")


if __name__ == "__main__":
    main()
