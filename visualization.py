import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def ndvi_colormap():
    return LinearSegmentedColormap.from_list(
        "ndvi", [(0.0, "#8B5E34"), (0.5, "#D9C34B"), (1.0, "#4C8C4A")]
    )


def save_ndvi_map(ndvi: np.ndarray, path: str = "ndvi_map.png"):
    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(ndvi, cmap=ndvi_colormap(), vmin=-0.2, vmax=0.8)
    ax.set_title("NDVI Map")
    ax.axis("off")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("NDVI (stressed -> healthy)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def save_histogram(ndvi: np.ndarray, path: str = "ndvi_histogram.png"):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(ndvi.flatten(), bins=40, color="#4C8C4A", edgecolor="#2B3A55")
    ax.set_xlabel("NDVI value")
    ax.set_ylabel("Pixel count")
    ax.set_title("NDVI Distribution Across Field")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)