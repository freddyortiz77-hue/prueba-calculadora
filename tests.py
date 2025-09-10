from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class MeanTestResult:
    mean: float
    expected: float
    statistic_z: float
    n: int

@dataclass
class VarianceTestResult:
    variance: float
    expected: float
    chi2_stat: float
    n: int

@dataclass
class Chi2Result:
    statistic: float
    k: int
    expected: np.ndarray
    observed: np.ndarray
    bins: np.ndarray

def test_mean_uniform(u: np.ndarray) -> MeanTestResult:
    u = np.asarray(u, dtype=float)
    u = u[(u >= 0.0) & (u <= 1.0)]
    n = len(u)
    if n == 0:
        raise ValueError("No hay datos válidos.")
    mean = float(u.mean())
    expected = 0.5
    var_mean = (1.0 / 12.0) / n
    z = (mean - expected) / (var_mean ** 0.5)
    return MeanTestResult(mean=mean, expected=expected, statistic_z=float(z), n=n)

def test_variance_uniform(u: np.ndarray) -> VarianceTestResult:
    u = np.asarray(u, dtype=float)
    u = u[(u >= 0.0) & (u <= 1.0)]
    n = len(u)
    if n < 2:
        raise ValueError("Se requieren al menos 2 observaciones.")
    s2 = float(u.var(ddof=1))
    sigma0 = 1.0 / 12.0
    chi2 = (n - 1) * s2 / sigma0
    return VarianceTestResult(variance=s2, expected=sigma0, chi2_stat=float(chi2), n=n)

def chi_square_uniform(u: np.ndarray, k: int = 10) -> Chi2Result:
    if k < 2:
        raise ValueError("k debe ser >= 2")
    u = np.asarray(u, dtype=float)
    u = u[(u >= 0.0) & (u < 1.0)]
    n = len(u)
    if n == 0:
        raise ValueError("No hay datos válidos.")
    counts, edges = np.histogram(u, bins=k, range=(0.0, 1.0))
    expected = np.full(k, n / k, dtype=float)
    stat = float(((counts - expected) ** 2 / expected).sum())
    return Chi2Result(statistic=stat, k=k, expected=expected, observed=counts, bins=edges)
