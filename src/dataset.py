"""
dataset.py
----------
PyTorch Dataset and DataLoader utilities for the Sorghum cultivar dataset.

The class-to-index mapping is derived from the training manifest and saved
to results/class_to_index.json so it is identical across all splits and
both future models.
"""

import json
from pathlib import Path

import pandas as pd
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms


class SorghumDataset(Dataset):
    """
    Loads sorghum images from a manifest CSV.

    Parameters
    ----------
    manifest : pd.DataFrame
        Must contain columns 'image' and 'cultivar'.
    image_dir : Path
        Directory containing the PNG images.
    transform : transforms.Compose
        Torchvision transform pipeline to apply.
    class_to_idx : dict
        Mapping from cultivar string to integer class index.
    """

    def __init__(
        self,
        manifest: pd.DataFrame,
        image_dir: Path,
        transform: transforms.Compose,
        class_to_idx: dict,
    ) -> None:
        self.manifest = manifest.reset_index(drop=True)
        self.image_dir = Path(image_dir)
        self.transform = transform
        self.class_to_idx = class_to_idx

    def __len__(self) -> int:
        return len(self.manifest)

    def __getitem__(self, idx: int):
        row = self.manifest.iloc[idx]
        img_path = self.image_dir / row["image"]
        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)
        label = self.class_to_idx[row["cultivar"]]
        return image, label


def build_class_to_idx(train_manifest: pd.DataFrame) -> dict:
    """
    Build a deterministic cultivar → integer index mapping from the training
    manifest. Cultivars are sorted alphabetically so the mapping is stable.
    """
    cultivars = sorted(train_manifest["cultivar"].unique())
    return {c: i for i, c in enumerate(cultivars)}


def save_class_to_idx(class_to_idx: dict, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(class_to_idx, f, indent=2, sort_keys=True)


def load_class_to_idx(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def make_loader(
    dataset: SorghumDataset,
    batch_size: int = 32,
    shuffle: bool = False,
    num_workers: int = 0,
    seed: int = 42,
) -> DataLoader:
    """
    Wrap a SorghumDataset in a DataLoader.

    Parameters
    ----------
    dataset     : SorghumDataset
    batch_size  : int   (default 32 — practical baseline, not claimed optimal)
    shuffle     : bool  (True for training, False for val/test)
    num_workers : int
    seed        : int   (generator seed for reproducible shuffling)
    """
    import torch
    generator = torch.Generator()
    generator.manual_seed(seed)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        generator=generator if shuffle else None,
    )
