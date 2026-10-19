"""Tests de l'arbre CRR contre la formule fermée de Black-Scholes.

Lancer : python -m unittest discover -s tests -v   (ou : python -m pytest -v)
"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np

from pricing.black_scholes import bs_price
from pricing.crr import crr_price

S, K, R, SIGMA, T = 100.0, 100.0, 0.05, 0.2, 1.0


class TestBlackScholes(unittest.TestCase):
    def test_valeur_de_reference(self):
        # Valeur classique (Hull) : call ATM, r=5 %, sigma=20 %, T=1 -> 10,4506
        self.assertAlmostEqual(bs_price(S, K, R, SIGMA, T), 10.4506, places=4)

    def test_parite_call_put(self):
        c = bs_price(S, 110.0, R, SIGMA, T, "call")
        p = bs_price(S, 110.0, R, SIGMA, T, "put")
        self.assertAlmostEqual(c - p, S - 110.0 * math.exp(-R * T), places=12)

    def test_entrees_invalides(self):
        with self.assertRaises(ValueError):
            bs_price(S, K, R, 0.0, T)
        with self.assertRaises(ValueError):
            bs_price(S, K, R, SIGMA, T, "straddle")


class TestCRR(unittest.TestCase):
    def test_parite_call_put_exacte_dans_l_arbre(self):
        # La parité est exacte dans l'arbre, quel que soit N.
        for N in (5, 50, 500):
            c = crr_price(S, 95.0, R, SIGMA, T, N, "call")
            p = crr_price(S, 95.0, R, SIGMA, T, N, "put")
            self.assertAlmostEqual(c - p, S - 95.0 * math.exp(-R * T), places=9)

    def test_ordre_de_convergence_un_sur_N(self):
        """L'erreur de CRR oscille (effet pair/impair, position du strike sur le
        réseau). On travaille donc sur l'enveloppe : max des erreurs sur 20 valeurs
        consécutives de N, puis régression log-log. Pente attendue : -1."""
        exact = bs_price(S, K, R, SIGMA, T)
        centres = [50, 100, 200, 400, 800, 1600, 3200]
        env = [max(abs(crr_price(S, K, R, SIGMA, T, n) - exact) for n in range(c, c + 20))
               for c in centres]
        pente = np.polyfit(np.log(centres), np.log(env), 1)[0]
        self.assertAlmostEqual(pente, -1.0, delta=0.1)

    def test_erreur_bornee_par_C_sur_N(self):
        exact = bs_price(S, K, R, SIGMA, T)
        for n in (100, 400, 1600):
            self.assertLess(n * abs(crr_price(S, K, R, SIGMA, T, n) - exact), 3.0)

    def test_call_americain_sans_dividende_egal_europeen(self):
        eu = crr_price(S, K, R, SIGMA, T, 400, "call")
        am = crr_price(S, K, R, SIGMA, T, 400, "call", american=True)
        self.assertAlmostEqual(am, eu, places=10)

    def test_put_americain_a_une_prime_d_exercice_anticipe(self):
        eu = crr_price(S, K, R, SIGMA, T, 400, "put")
        am = crr_price(S, K, R, SIGMA, T, 400, "put", american=True)
        self.assertGreater(am - eu, 0.1)   # ~0,5 pour ces paramètres

    def test_proba_risque_neutre_hors_de_0_1_leve_une_erreur(self):
        with self.assertRaises(ValueError):
            crr_price(S, K, 0.5, 0.01, 10.0, 1)


if __name__ == "__main__":
    unittest.main()
