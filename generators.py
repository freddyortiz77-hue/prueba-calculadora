from __future__ import annotations
import numpy as np

def middle_square(seed: int, n: int = 100, width: int = 8) -> np.ndarray:
    """
    Método de cuadrados medios.
    - seed: semilla entera (preferiblemente con 'width' dígitos)
    - n: cantidad de números a generar
    - width: número de dígitos que se mantienen (ej. 4,6,8)
    Retorna array en [0,1).
    """
    if width <= 0:
        raise ValueError("width debe ser positivo (número de dígitos).")
    x = int(seed)
    out = []
    mod = 10 ** width
    for _ in range(n):
        sq = x * x
        s = str(sq).zfill(2 * width)
        start = (len(s) // 2) - (width // 2)
        mid = s[start:start + width]
        x = int(mid)
        out.append(x / mod)
    return np.array(out, dtype=float)

def mult_congruential(seed: int, a: int, m: int, n: int = 100) -> np.ndarray:
    """
    Multiplicative Congruential Generator (c = 0): X_{k+1} = (a * X_k) mod m
    Retorna array en [0,1).
    """
    if m <= 0:
        raise ValueError("m debe ser positivo.")
    x = int(seed) % m
    out = []
    for _ in range(n):
        x = (a * x) % m
        out.append(x / m)
    return np.array(out, dtype=float)

def numpy_rng(seed: int | None, n: int = 1000) -> np.ndarray:
    import numpy as _np
    rng = _np.random.default_rng(seed)
    return rng.random(n)
