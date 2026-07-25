import numpy as np

#per-pixel NDVI
def compute_ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
    red = red.astype(np.float32)
    nir = nir.astype(np.float32)
    eps = 1e-6 #avoids a zero div when bands read near zero
    ndvi = (nir - red) / (nir + red + eps)
    return np.clip(ndvi, -1.0, 1.0)

def classify_ndvi(ndvi: np.ndarray) -> dict:
    classes = {
        "bare / water (NDVI < 0.1)": ndvi < 0.1,
        "stressed vegetation (0.1 - 0.3)": (ndvi >= 0.1) & (ndvi < 0.3),
        "moderate vegetation (0.3 - 0.5)": (ndvi >= 0.3) & (ndvi < 0.5),
        "healthy vegetation (>= 0.5)": ndvi >= 0.5,
    }
    total = ndvi.size


    results = {}

    for label, mask in classes.items():
        results[label] = 100.0 * mask.sum() / total

    return results