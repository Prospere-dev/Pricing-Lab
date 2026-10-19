# Formule de Black-Scholes pour une option européenne (avec dividende continu q)
from math import erf, exp, log, sqrt


def phi(x):
    # fonction de répartition de la loi normale N(0,1)
    return 0.5 * (1 + erf(x / sqrt(2)))


def bs_price(S, K, r, sigma, T, kind="call", q=0.0):
    if kind not in ("call", "put"):
        raise ValueError("kind doit valoir 'call' ou 'put'")
    if min(S, K, sigma, T) <= 0:
        raise ValueError("S, K, sigma et T doivent être strictement positifs")
    sd = sigma * sqrt(T)
    d1 = (log(S / K) + (r - q + sigma ** 2 / 2) * T) / sd
    d2 = d1 - sd
    if kind == "call":
        return S * exp(-q * T) * phi(d1) - K * exp(-r * T) * phi(d2)
    return K * exp(-r * T) * phi(-d2) - S * exp(-q * T) * phi(-d1)
