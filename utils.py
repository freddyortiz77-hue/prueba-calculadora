from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def ensure_dir(path: str) -> None:
    if not path:
        return
    os.makedirs(path, exist_ok=True)

def export_csv(data: np.ndarray, path: str) -> str:
    ensure_dir(os.path.dirname(path))
    np.savetxt(path, data, delimiter=",", header="value", comments="")
    return path

def save_histogram(data, path: str, bins: int = 20, title: str = "Histograma") -> str:
    ensure_dir(os.path.dirname(path))
    plt.figure()
    plt.hist(data, bins=bins, edgecolor="black")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path
