"""
create_balanced_subset.py
August 16, 2026

Creates a reproducible, class-balanced subset manifest from the validated
image-cultivar mapping produced on August 15.

No images are copied. The output is a CSV manifest (balanced_subset.csv)
that references the original image filenames.

Reproducibility:
    - validated mapping: results/validated_image_cultivar_mapping.csv
    - image directory:   ../../Dataset  (flat, images live directly here)
    - random seed:       42
    - sampling rule:     min(available_per_class, target_per_class) images
                         per cultivar, where target defaults to the minimum
                         class size across all cultivars (fully balanced).
"""

from pathlib import Path
import warnings
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
VALIDATED_MAPPING = Path("results/validated_image_cultivar_mapping.csv")
IMAGE_DIR         = Path("../Dataset")
OUTPUT_DIR        = Path("results")
RANDOM_SEED       = 42
# Set to None to auto-select (uses minimum class size for full balance).
IMAGES_PER_CULTIVAR = None
DATASET_VERSION   = "balanced_subset_v1"


def load_and_verify(mapping_path: Path) -> pd.DataFrame:
    assert mapping_path.exists(), f"Validated mapping not found: {mapping_path}"
    df = pd.read_csv(mapping_path)
    assert "image" in df.columns, "Column 'image' missing"
    assert "cultivar" in df.columns, "Column 'cultivar' missing"
    assert df["image"].notna().all(), "Null values in 'image' column"
    assert df["cultivar"].notna().all(), "Null values in 'cultivar' column"
    assert df["image"].duplicated().sum() == 0, "Duplicate image filenames found"
    conflicts = df.groupby("image")["cultivar"].nunique()
    assert (conflicts == 1).all(), "Images with conflicting cultivar labels found"
    return df


def verify_images_exist(df: pd.DataFrame, image_dir: Path) -> pd.DataFrame:
    df = df.copy()
    df["source_path"] = df["image"].apply(lambda f: str(image_dir / f))
    df["_exists"] = df["image"].apply(lambda f: (image_dir / f).exists())
    missing = df[~df["_exists"]]
    if len(missing) > 0:
        print(f"  WARNING: {len(missing)} images missing from disk — excluded.")
    df = df[df["_exists"]].drop(columns=["_exists"]).reset_index(drop=True)
    return df


def determine_sample_size(counts: pd.Series, target: int | None) -> int:
    min_count = int(counts.min())
    if target is None:
        return min_count
    if target > min_count:
        print(f"  WARNING: requested {target} > min class size {min_count}; "
              f"using {min_count}.")
        return min_count
    return target


def sample_balanced(df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    return (
        df.groupby("cultivar", group_keys=False)
          .apply(lambda g: g.sample(n=n, random_state=seed))
          .reset_index(drop=True)
    )


def main():
    warnings.filterwarnings("ignore", category=FutureWarning)
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. Load and verify mapping
    print("Loading validated mapping …")
    df = load_and_verify(VALIDATED_MAPPING)
    print(f"  Rows loaded: {len(df)}")

    # 2. Verify images exist on disk
    print("Checking images on disk …")
    df = verify_images_exist(df, IMAGE_DIR)
    total_valid = len(df)
    print(f"  Valid image-cultivar pairs: {total_valid}")

    # 3. Class distribution
    counts = df.groupby("cultivar").size().sort_values()
    n_cultivars = len(counts)
    min_count   = int(counts.min())
    max_count   = int(counts.max())
    median_count = float(counts.median())
    print(f"  Cultivars: {n_cultivars}")
    print(f"  Images per cultivar — min: {min_count}, max: {max_count}, "
          f"median: {median_count}")

    # 4. Determine sample size
    n = determine_sample_size(counts, IMAGES_PER_CULTIVAR)
    total_selected = n * n_cultivars
    print(f"  Chosen images per cultivar: {n}")
    print(f"  Total selected: {total_selected}")

    # 5. Balanced sampling (deterministic)
    subset = sample_balanced(df[["image", "cultivar", "source_path"]], n, RANDOM_SEED)

    # 6. Save balanced_subset.csv
    subset_path = OUTPUT_DIR / "balanced_subset.csv"
    subset.to_csv(subset_path, index=False)
    print(f"  Saved: {subset_path}")

    # 7. Save distribution CSV
    dist = (
        subset.groupby("cultivar")
              .size()
              .reset_index(name="selected_images")
              .sort_values("cultivar")
    )
    dist_path = OUTPUT_DIR / "balanced_subset_distribution.csv"
    dist.to_csv(dist_path, index=False)
    print(f"  Saved: {dist_path}")

    # 8. Save summary CSV
    summary = pd.DataFrame([
        ("Dataset version",              DATASET_VERSION),
        ("Original validated images",    total_valid),
        ("Number of cultivars",          n_cultivars),
        ("Minimum images per cultivar",  min_count),
        ("Maximum images per cultivar",  max_count),
        ("Median images per cultivar",   median_count),
        ("Chosen images per cultivar",   n),
        ("Total selected images",        total_selected),
        ("Random seed",                  RANDOM_SEED),
        ("Sampling method",              "stratified random sample, fixed seed"),
        ("All classes equally represented",
         str((dist["selected_images"] == n).all())),
        ("Unique images in subset",      subset["image"].nunique()),
        ("Duplicate images in subset",   int(subset["image"].duplicated().sum())),
        ("Source mapping",               str(VALIDATED_MAPPING)),
        ("Image directory",              str(IMAGE_DIR)),
    ], columns=["Metric", "Value"])
    summary_path = OUTPUT_DIR / "balanced_subset_summary.csv"
    summary.to_csv(summary_path, index=False)
    print(f"  Saved: {summary_path}")

    # 9. Validation checks
    assert subset["image"].nunique() == total_selected, "Duplicate images in subset"
    assert len(subset["cultivar"].unique()) == n_cultivars, "Missing cultivars"
    assert (dist["selected_images"] == n).all(), "Unequal class sizes"
    missing_on_disk = subset["image"].apply(
        lambda f: not (IMAGE_DIR / f).exists()
    ).sum()
    assert missing_on_disk == 0, f"{missing_on_disk} selected images missing on disk"
    print("  All validation checks passed.")

    print("\nDone.")


if __name__ == "__main__":
    main()
