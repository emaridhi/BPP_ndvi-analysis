import numpy as np


def generate_synthetic_field(size = 128, stress_level = 0.35, seed = None
) -> tuple[np.ndarray, np.ndarray]:

    rng = np.random.default_rng(seed)

    # Low-frequency noise field as a stand-in for real canopy variation
    seed_grid = rng.random((8, 8))
    x = np.linspace(0, 8, size, endpoint=False)
    y = np.linspace(0, 8, size, endpoint=False)
    xi = np.floor(x).astype(int) % 8
    yi = np.floor(y).astype(int) % 8
    fx = x - np.floor(x)
    fy = y - np.floor(y)

    health = np.zeros((size, size), dtype=np.float32)
    for j in range(size):
        y0, y1 = yi[j], (yi[j] + 1) % 8
        wy = fy[j]
        row_lo = seed_grid[y0, xi] * (1 - fx) + seed_grid[y0, (xi + 1) % 8] * fx
        row_hi = seed_grid[y1, xi] * (1 - fx) + seed_grid[y1, (xi + 1) % 8] * fx
        health[j, :] = row_lo * (1 - wy) + row_hi * wy

    health = np.clip(health, 0, 1) ** (1 + stress_level * 2)

    noise = (rng.random((size, size)) - 0.5) * 0.03
    red = np.clip(0.32 - health * 0.20 + noise, 0.02, 1.0)
    nir = np.clip(0.18 + health * 0.55 + noise, 0.02, 1.0)
    return red, nir
