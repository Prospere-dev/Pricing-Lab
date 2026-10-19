# Arbre binomial de Cox-Ross-Rubinstein, option européenne ou américaine
import numpy as np


def crr_price(S, K, r, sigma, T, N, kind="call", american=False, q=0.0):
    if kind not in ("call", "put"):
        raise ValueError("kind doit valoir 'call' ou 'put'")
    if N < 1:
        raise ValueError("N doit valoir au moins 1")
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))   # facteur de hausse
    d = 1 / u                         # facteur de baisse
    p = (np.exp((r - q) * dt) - d) / (u - d)   # probabilité de hausse
    if not 0 < p < 1:
        raise ValueError(f"p = {p:.4f} n'est pas entre 0 et 1 : augmenter N")
    actu = np.exp(-r * dt)
    signe = 1 if kind == "call" else -1       # +1 pour un call, -1 pour un put

    # prix de l'action à l'échéance (j = nombre de hausses) et gain de l'option
    j = np.arange(N + 1)
    S_final = S * u ** (2 * j - N)
    V = np.maximum(signe * (S_final - K), 0)

    # on remonte l'arbre d'une étape à la fois
    for n in range(N - 1, -1, -1):
        V = actu * (p * V[1:] + (1 - p) * V[:-1])
        if american:
            S_n = S * u ** (2 * np.arange(n + 1) - n)
            V = np.maximum(V, np.maximum(signe * (S_n - K), 0))   # exercer maintenant ou attendre
    return float(V[0])
