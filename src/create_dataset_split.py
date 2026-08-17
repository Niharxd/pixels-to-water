"""
Create a reproducible stratified train/validation/test split from the balanced subset.
Split ratio: 80% train, 10% validation, 10% test, stratified by cultivar.
Random seed: 42
"""

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
RESULTS_DIR = Path(__file__).parent.parent / "results"
DATASET_DIR = Path(__file__).parent.parent.parent / "Dataset"


def load_and_validate(csv_path: Path) -> pd.DataFrame:
    assert csv_path.exists(), f"Input file not found: {csv_path}"
    df = pd.read_csv(csv_path)

    assert "image" in df.columns, "Column 'image' missing"
    assert "cultivar" in df.columns, "Column 'cultivar' missing"

    dupes = df["image"].duplicated().sum()
    assert dupes == 0, f"Duplicate image entries found: {dupes}"

    missing = [img for img in df["image"] if not (DATASET_DIR / img).exists()]
    assert len(missing) == 0, f"{len(missing)} images missing from disk: {missing[:5]}"

    multi = df.groupby("image")["cultivar"].nunique()
    bad = multi[multi > 1]
    assert len(bad) == 0, f"Images with multiple cultivars: {bad.index.tolist()}"

    print(f"  Input validated: {len(df)} images, {df['cultivar'].nunique()} cultivars")
    return df


def check_small_classes(df: pd.DataFrame) -> None:
    counts = df["cultivar"].value_counts()
    # Need at least 10 per class for 80/10/10 (1 val + 1 test minimum)
    small = counts[counts < 10]
    if len(small) > 0:
        print(f"  WARNING: {len(small)} cultivar(s) have fewer than 10 images.")
        print(f"  Affected: {small.to_dict()}")
        print("  Stratified split will still be attempted; counts may deviate from 80/10/10.")
    else:
        print(f"  All {len(counts)} cultivars have >= 10 images. Stratified split is safe.")


def perform_split(df: pd.DataFrame):
    # First split: 80% train, 20% temp
    train_df, temp_df = train_test_split(
        df,
        test_size=0.20,
        stratify=df["cultivar"],
        random_state=RANDOM_SEED,
    )
    # Second split: 50% of temp → val, 50% → test  (each = 10% of total)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        stratify=temp_df["cultivar"],
        random_state=RANDOM_SEED,
    )
    return train_df.copy(), val_df.copy(), test_df.copy()


def verify_no_leakage(train_df, val_df, test_df, original_df) -> None:
    train_imgs = set(train_df["image"])
    val_imgs = set(val_df["image"])
    test_imgs = set(test_df["image"])

    assert len(train_imgs & val_imgs) == 0, "LEAKAGE: train ∩ validation is not empty"
    assert len(train_imgs & test_imgs) == 0, "LEAKAGE: train ∩ test is not empty"
    assert len(val_imgs & test_imgs) == 0, "LEAKAGE: validation ∩ test is not empty"

    all_split = train_imgs | val_imgs | test_imgs
    original_imgs = set(original_df["image"])
    assert all_split == original_imgs, "Split images do not match balanced subset exactly"

    # No duplicates within each split
    for name, split_df in [("train", train_df), ("validation", val_df), ("test", test_df)]:
        dupes = split_df["image"].duplicated().sum()
        assert dupes == 0, f"Duplicate images within {name} split: {dupes}"

    print("  All leakage checks passed.")


def save_manifests(train_df, val_df, test_df, results_dir: Path) -> None:
    for name, split_df in [("train", train_df), ("validation", val_df), ("test", test_df)]:
        out = split_df[["image", "cultivar"]].copy()
        out["split"] = name
        out.to_csv(results_dir / f"{name}.csv", index=False)

    master = pd.concat([
        train_df[["image", "cultivar"]].assign(split="train"),
        val_df[["image", "cultivar"]].assign(split="validation"),
        test_df[["image", "cultivar"]].assign(split="test"),
    ], ignore_index=True)
    master.to_csv(results_dir / "dataset_split.csv", index=False)
    print(f"  Saved train.csv ({len(train_df)}), validation.csv ({len(val_df)}), "
          f"test.csv ({len(test_df)}), dataset_split.csv ({len(master)})")


def save_class_distribution(train_df, val_df, test_df, results_dir: Path) -> None:
    train_counts = train_df["cultivar"].value_counts().rename("Train")
    val_counts = val_df["cultivar"].value_counts().rename("Validation")
    test_counts = test_df["cultivar"].value_counts().rename("Test")

    dist = pd.concat([train_counts, val_counts, test_counts], axis=1).fillna(0).astype(int)
    dist["Total"] = dist["Train"] + dist["Validation"] + dist["Test"]
    dist.index.name = "Cultivar"
    dist = dist.reset_index()
    dist.to_csv(results_dir / "split_class_distribution.csv", index=False)
    print(f"  Saved split_class_distribution.csv ({len(dist)} cultivars)")


def save_summary(train_df, val_df, test_df, results_dir: Path) -> None:
    total = len(train_df) + len(val_df) + len(test_df)
    rows = [
        ("Total images", total),
        ("Training images", len(train_df)),
        ("Validation images", len(val_df)),
        ("Test images", len(test_df)),
        ("Number of cultivars", train_df["cultivar"].nunique()),
        ("Training percentage", f"{len(train_df) / total * 100:.2f}%"),
        ("Validation percentage", f"{len(val_df) / total * 100:.2f}%"),
        ("Test percentage", f"{len(test_df) / total * 100:.2f}%"),
        ("Random seed", RANDOM_SEED),
    ]
    pd.DataFrame(rows, columns=["Metric", "Value"]).to_csv(
        results_dir / "split_summary.csv", index=False
    )
    print(f"  Saved split_summary.csv")


def save_visualization(train_df, val_df, test_df, results_dir: Path) -> None:
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use("Agg")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Bar chart: total images per split
    splits = ["Training", "Validation", "Test"]
    counts = [len(train_df), len(val_df), len(test_df)]
    colors = ["#4878CF", "#6ACC65", "#D65F5F"]
    axes[0].bar(splits, counts, color=colors, width=0.5)
    axes[0].set_title("Images per Split")
    axes[0].set_ylabel("Number of Images")
    for i, v in enumerate(counts):
        axes[0].text(i, v + 5, str(v), ha="center", va="bottom", fontsize=10)
    axes[0].set_ylim(0, max(counts) * 1.12)

    # Per-cultivar distribution across splits
    train_counts = train_df["cultivar"].value_counts().sort_index()
    val_counts = val_df["cultivar"].value_counts().sort_index()
    test_counts = test_df["cultivar"].value_counts().sort_index()

    axes[1].plot(range(len(train_counts)), train_counts.values, color="#4878CF",
                 linewidth=1, label=f"Train (n={len(train_df)})")
    axes[1].plot(range(len(val_counts)), val_counts.values, color="#6ACC65",
                 linewidth=1, label=f"Validation (n={len(val_df)})")
    axes[1].plot(range(len(test_counts)), test_counts.values, color="#D65F5F",
                 linewidth=1, label=f"Test (n={len(test_df)})")
    axes[1].set_title("Per-Cultivar Image Counts Across Splits")
    axes[1].set_xlabel("Cultivar (sorted)")
    axes[1].set_ylabel("Number of Images")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(results_dir / "split_distribution.png", dpi=150)
    plt.close(fig)
    print("  Saved split_distribution.png")


def print_summary(train_df, val_df, test_df) -> None:
    total = len(train_df) + len(val_df) + len(test_df)
    print("\n=== Split Summary ===")
    print(f"  Total images : {total}")
    print(f"  Train        : {len(train_df)} ({len(train_df)/total*100:.1f}%)")
    print(f"  Validation   : {len(val_df)} ({len(val_df)/total*100:.1f}%)")
    print(f"  Test         : {len(test_df)} ({len(test_df)/total*100:.1f}%)")
    print(f"  Cultivars    : train={train_df['cultivar'].nunique()}, "
          f"val={val_df['cultivar'].nunique()}, test={test_df['cultivar'].nunique()}")
    print(f"  Random seed  : {RANDOM_SEED}")


def main():
    print("Step 1: Loading and validating balanced_subset.csv ...")
    df = load_and_validate(RESULTS_DIR / "balanced_subset.csv")

    print("Step 2: Checking class sizes ...")
    check_small_classes(df)

    print("Step 3: Performing stratified split (80/10/10) ...")
    train_df, val_df, test_df = perform_split(df)

    print("Step 4: Verifying no data leakage ...")
    verify_no_leakage(train_df, val_df, test_df, df)

    print("Step 5: Saving split manifests ...")
    save_manifests(train_df, val_df, test_df, RESULTS_DIR)

    print("Step 6: Saving class distribution ...")
    save_class_distribution(train_df, val_df, test_df, RESULTS_DIR)

    print("Step 7: Saving split summary ...")
    save_summary(train_df, val_df, test_df, RESULTS_DIR)

    print("Step 8: Saving visualization ...")
    save_visualization(train_df, val_df, test_df, RESULTS_DIR)

    print_summary(train_df, val_df, test_df)
    print("\nDone. All outputs written to results/")


if __name__ == "__main__":
    main()
