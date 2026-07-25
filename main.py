import argparse
from ndvi_core import compute_ndvi, classify_ndvi
from field_generator import generate_synthetic_field
from image_io import load_band
from visualization import save_ndvi_map, save_histogram


def main():
    parser = argparse.ArgumentParser(description="NDVI analysis tool")
    parser.add_argument("--red", type=str, default=None, help="Path to red-band grayscale image")
    parser.add_argument("--nir", type=str, default=None, help="Path to NIR-band grayscale image")
    parser.add_argument("--stress", type=float, default=0.35, help="Synthetic field stress level [0-1]")
    parser.add_argument("--size", type=int, default=128, help="Synthetic field size (pixels per side)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for synthetic field")
    args = parser.parse_args()

    if args.red and args.nir:
        print(f"Loading real imagery:\n  Red: {args.red}\n  NIR: {args.nir}")
        red = load_band(args.red)
        nir = load_band(args.nir)
        if red.shape != nir.shape:
            raise ValueError(f"Band shape mismatch: red {red.shape} vs nir {nir.shape}")
    else:
        print(f"No image paths given -- generating synthetic field (stress={args.stress}, size={args.size})")
        red, nir = generate_synthetic_field(size=args.size, stress_level=args.stress, seed=args.seed)

    ndvi = compute_ndvi(red, nir)

    print("NDVI Summary")
    print(f"Mean NDVI: {ndvi.mean():.3f}")
    print(f"Min NDVI:  {ndvi.min():.3f}")
    print(f"Max NDVI:  {ndvi.max():.3f}")

    print("Vegetation Health Classification")
    for label, pct in classify_ndvi(ndvi).items():
        print(f"{label:35s}: {pct:5.1f}%")

    save_ndvi_map(ndvi, "outputs/ndvi_map.png")
    save_histogram(ndvi, "outputs/ndvi_histogram.png")
    print("\nSaved ndvi_map.png and ndvi_histogram.png")


if __name__ == "__main__":
    main()