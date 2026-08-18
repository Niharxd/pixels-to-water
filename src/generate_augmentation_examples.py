"""
generate_augmentation_examples.py
----------------------------------
Generates results/augmentation_examples.png and runs batch sanity checks.
Run once; not part of training.
"""

import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import torch
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from preprocessing import get_train_transform, get_val_transform, get_test_transform
from dataset import SorghumDataset, build_class_to_idx, save_class_to_idx, make_loader

SEED = 42
random.seed(SEED)
torch.manual_seed(SEED)

REPO_ROOT = Path(__file__).parent.parent
IMAGE_DIR = REPO_ROOT.parent / "Dataset"
RESULTS   = REPO_ROOT / "results"

# ── Load manifests ────────────────────────────────────────────────────────────
train_df = pd.read_csv(RESULTS / "train.csv")
val_df   = pd.read_csv(RESULTS / "validation.csv")
test_df  = pd.read_csv(RESULTS / "test.csv")

# ── Class mapping ─────────────────────────────────────────────────────────────
class_to_idx = build_class_to_idx(train_df)
save_class_to_idx(class_to_idx, RESULTS / "class_to_index.json")
print(f"Class mapping: {len(class_to_idx)} cultivars saved to results/class_to_index.json")

# ── Datasets ──────────────────────────────────────────────────────────────────
train_ds = SorghumDataset(train_df, IMAGE_DIR, get_train_transform(), class_to_idx)
val_ds   = SorghumDataset(val_df,   IMAGE_DIR, get_val_transform(),   class_to_idx)
test_ds  = SorghumDataset(test_df,  IMAGE_DIR, get_test_transform(),  class_to_idx)

# ── DataLoaders ───────────────────────────────────────────────────────────────
train_loader = make_loader(train_ds, batch_size=32, shuffle=True,  seed=SEED)
val_loader   = make_loader(val_ds,   batch_size=32, shuffle=False, seed=SEED)
test_loader  = make_loader(test_ds,  batch_size=32, shuffle=False, seed=SEED)

# ── Batch sanity checks ───────────────────────────────────────────────────────
def check_batch(loader, name):
    imgs, labels = next(iter(loader))
    assert imgs.ndim == 4,                    f"{name}: expected 4D tensor"
    assert imgs.shape[1] == 3,               f"{name}: expected 3 channels"
    assert imgs.shape[2] == 224,             f"{name}: expected height 224"
    assert imgs.shape[3] == 224,             f"{name}: expected width 224"
    assert imgs.dtype == torch.float32,      f"{name}: expected float32"
    assert labels.dtype == torch.int64,      f"{name}: expected int64 labels"
    assert labels.min() >= 0,               f"{name}: negative label"
    assert labels.max() < len(class_to_idx), f"{name}: label out of range"
    print(f"[OK] {name:10s}  shape={tuple(imgs.shape)}  "
          f"dtype={imgs.dtype}  labels=[{labels.min()}, {labels.max()}]  "
          f"pixel_mean={imgs.mean():.4f}  pixel_std={imgs.std():.4f}")

check_batch(train_loader, "train")
check_batch(val_loader,   "val")
check_batch(test_loader,  "test")

# ── Determinism check for val/test ────────────────────────────────────────────
imgs_v1, _ = next(iter(val_loader))
imgs_v2, _ = next(iter(val_loader))
assert torch.allclose(imgs_v1, imgs_v2), "val transform is not deterministic!"
print("[OK] val_transform is deterministic")

imgs_t1, _ = next(iter(test_loader))
imgs_t2, _ = next(iter(test_loader))
assert torch.allclose(imgs_t1, imgs_t2), "test transform is not deterministic!"
print("[OK] test_transform is deterministic")

# ── Augmentation examples figure ─────────────────────────────────────────────
# Pick one image; show original + 5 augmented versions
sample_row = train_df.sample(1, random_state=SEED).iloc[0]
orig_img = Image.open(IMAGE_DIR / sample_row["image"]).convert("RGB")

val_tf   = get_val_transform()
train_tf = get_train_transform()

IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
IMAGENET_STD  = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)

def denorm(t):
    return (t * IMAGENET_STD + IMAGENET_MEAN).clamp(0, 1).permute(1, 2, 0).numpy()

N_AUG = 5
fig, axes = plt.subplots(1, N_AUG + 2, figsize=(14, 3))

# Original (resized for display)
axes[0].imshow(orig_img.resize((224, 224)))
axes[0].set_title("Original", fontsize=9)
axes[0].axis("off")

# Preprocessed (val transform, deterministic)
axes[1].imshow(denorm(val_tf(orig_img)))
axes[1].set_title("Preprocessed\n(val/test)", fontsize=9)
axes[1].axis("off")

# Augmented versions
torch.manual_seed(SEED)
for i in range(N_AUG):
    axes[i + 2].imshow(denorm(train_tf(orig_img)))
    axes[i + 2].set_title(f"Augmented {i+1}", fontsize=9)
    axes[i + 2].axis("off")

fig.suptitle(
    f"Sorghum cultivar: {sample_row['cultivar']}  |  "
    "Original vs Preprocessed vs Augmented (train)",
    fontsize=10,
)
plt.tight_layout()
out_path = RESULTS / "augmentation_examples.png"
plt.savefig(out_path, dpi=120, bbox_inches="tight")
plt.close()
print(f"[OK] Saved {out_path}")
print("\nAll checks passed.")
