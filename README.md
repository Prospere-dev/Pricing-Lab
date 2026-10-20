# Pricing Lab

Je réalise ce projet en tant qu'étudiant en mathématiques et informatique intéréssé par la finance de marché.

Il calcule le prix d'une option de quatre façons différentes, puis compare les résultats avec la formule exacte de Black-Scholes.

**Démo interactive :** [https://prospere-dev.github.io/Pricing-Lab/lab/] - **Auteur** : Prospere ZANJIO

## D'où viennent les formules

Les formules de ce projet sont des résultats classiques de la finance, qu'on peut retrouver dans la littérature et en ligne. Elles sont reprises telles quelles : la formule de Black et Scholes (1973), l'arbre binomial de Cox, Ross et Rubinstein (1979), la méthode de Monte Carlo et la variable de contrôle. Je ne les ai pas démontrées. Le projet les applique, les compare entre elles et vérifie par des tests qu'elles donnent des résultats cohérents.

## C'est quoi une option ?

Une option est un contrat qui donne le droit, sans l'obligation, d'acheter ou de vendre une action à un prix fixé à l'avance (le **strike**, noté $K$) à une date donnée (l'**échéance**, notée $T$).
- Le **call** donne le droit d'acheter.
- Le **put** donne le droit de vendre.
- Une option **européenne** s'exerce uniquement à l'échéance. Une option **américaine** s'exerce à tout moment avant l'échéance.

Le but du projet est de répondre à une question : combien vaut ce droit aujourd'hui ?

## Les quatre méthodes

| Méthode | Principe en une phrase |
| --- | --- |
| Black-Scholes | Une formule exacte, valable pour l'option européenne. |
| Arbre binomial | À chaque période, le prix de l'action monte ou descend. On calcule le prix de l'option en partant de la fin de l'arbre et en remontant vers aujourd'hui. |
| Monte Carlo | On simule beaucoup d'évolutions possibles du prix de l'action, puis on fait la moyenne des gains, ramenés à aujourd'hui avec le taux $r$. |
| Exercice anticipé | Dans l'arbre, à chaque point on compare "exercer maintenant" et "attendre". On garde la valeur la plus grande. |

En plus, la **variable de contrôle** améliore Monte Carlo. On utilise une quantité dont on connaît la moyenne exacte (ici le prix de l'action à l'échéance) pour corriger l'erreur de la simulation.

## Les variables

| Symbole | Dans le code | Signification |
| --- | --- | --- |
| $S$ | `S` | Prix de l'action aujourd'hui. |
| $K$ | `K` | Strike : prix fixé dans le contrat. |
| $T$ | `T` | Durée jusqu'à l'échéance, en années. |
| $r$ | `r` | Taux d'intérêt sans risque (par exemple 0,05 pour 5 %). |
| $q$ | `q` | Dividende versé en continu par l'action (0 par défaut). |
| $\sigma$ | `sigma` | Volatilité : ampleur des variations du prix de l'action sur un an. |
| $N$ | `N` | Nombre de pas de l'arbre. |
| $\Delta t$ | `dt` | Durée d'un pas : $T/N$. |
| $u$, $d$ | `u`, `d` | Facteurs de hausse et de baisse de l'action sur un pas. |
| $p$ | `p` | Probabilité de hausse utilisée pour le calcul. Elle est choisie pour que l'action rapporte en moyenne le taux $r$ (moins le dividende $q$). |
| $\Phi$ | `phi` | Fonction de répartition de la loi normale $N(0,1)$. |
| $n$ | | Nombre de simulations Monte Carlo. |

## Les formules et leur rôle

**Black-Scholes** (donne directement le prix d'une option européenne)

$$d_1 = \frac{\ln(S/K) + (r - q + \sigma^2/2)\,T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

$$C = S\,e^{-qT}\,\Phi(d_1) - K\,e^{-rT}\,\Phi(d_2)$$

$$P = K\,e^{-rT}\,\Phi(-d_2) - S\,e^{-qT}\,\Phi(-d_1)$$

Rôle : c'est la valeur exacte de référence. Les autres méthodes sont comparées à elle.

**Parité call-put**

$$C - P = S\,e^{-qT} - K\,e^{-rT}$$

Rôle : relation qui doit toujours être vraie entre le prix du call et celui du put. Elle sert à vérifier les calculs.

**Arbre binomial** (prix d'une option européenne ou américaine)

$$\Delta t = \frac{T}{N}, \qquad u = e^{\sigma\sqrt{\Delta t}}, \qquad d = \frac{1}{u}, \qquad p = \frac{e^{(r-q)\Delta t} - d}{u - d}$$

Valeur d'un point de l'arbre :

$$V = e^{-r\Delta t}\,\Bigl[\,p\,V_{\text{haut}} + (1-p)\,V_{\text{bas}}\,\Bigr]$$

Option américaine : à chaque point,

$$V = \max\bigl(V,\ \text{gain si on exerce maintenant}\bigr)$$

Rôle : on part des gains à l'échéance et on remonte vers aujourd'hui. À chaque pas, la valeur est la moyenne pondérée des deux valeurs suivantes, ramenée à aujourd'hui avec le taux $r$. Le max permet d'ajouter la possibilité d'exercer avant l'échéance.

**Monte Carlo** (prix d'une option européenne)

Prix de l'action à l'échéance, avec $Z$ tirée dans $N(0,1)$ :

$$S_T = S\,\exp\Bigl((r - q - \sigma^2/2)\,T + \sigma\sqrt{T}\,Z\Bigr)$$

Gain d'une simulation, ramené à aujourd'hui (cas d'un put) :

$$Y = e^{-rT}\max(K - S_T,\ 0)$$

Prix estimé et intervalle d'erreur, avec $s$ l'écart-type des $Y_i$ :

$$\bar{Y} = \frac{1}{n}\sum_{i=1}^{n} Y_i, \qquad \bar{Y} \pm 1{,}96\,\frac{s}{\sqrt{n}}$$

Rôle : on simule beaucoup d'avenirs possibles et on moyenne les gains. Plus $n$ est grand, plus l'estimation est précise.

**Variable de contrôle** (rend Monte Carlo plus précis)

$$X = e^{-rT}\,S_T, \qquad \mathbb{E}[X] = S\,e^{-qT}$$

$$\beta = \frac{\mathrm{Cov}(X,Y)}{\mathrm{Var}(X)}$$

Estimation corrigée :

$$\hat{Y} = \bar{Y} - \beta\,\bigl(\bar{X} - S\,e^{-qT}\bigr)$$

Rôle : si les simulations donnent un $\bar{X}$ trop haut ou trop bas par rapport à sa vraie valeur, on corrige $\bar{Y}$ dans le même sens. Cela marche parce que $X$ et $Y$ varient ensemble.

**Sensibilités** (calculées dans la page interactive)

- Delta : de combien le prix de l'option change quand l'action monte de 1.
- Gamma : de combien le delta change quand l'action monte de 1.
- Vega : effet d'une hausse de la volatilité.
- Theta : effet du passage du temps.
- Rho : effet d'une hausse du taux $r$.

## Contenu du dépôt

| Fichier | Rôle |
| --- | --- |
| `src/pricing/black_scholes.py` | La formule de Black-Scholes, avec dividende continu. |
| `src/pricing/crr.py` | L'arbre binomial (européen et américain). |
| `tests/test_crr_vs_bs.py` | 9 tests automatiques. |
| `lab/index.html` | La page interactive : prix, sensibilités, convergence de l'arbre, Monte Carlo, exercice anticipé. |

Monte Carlo, les sensibilités et l'exercice anticipé existent pour l'instant dans la page interactive seulement. La formule exacte et l'arbre donnent les mêmes résultats en Python et dans la page (écart de l'ordre de $10^{-14}$).

## Hypothèses du modèle

Le taux d'intérêt $r$, le dividende $q$ et la volatilité $\sigma$ restent constants. Le prix de l'action suit un modèle aléatoire classique en finance : ses variations sont aléatoires, avec une volatilité fixe (c'est le mouvement brownien géométrique). Aucune donnée de marché n'est utilisée.

## Résultats

Paramètres : prix de l'action 100, strike 100, volatilité 20 %, taux 5 %, échéance 1 an.

| Grandeur | Valeur |
| --- | --- |
| Call européen (Black-Scholes) | 10,4506 |
| Put européen (Black-Scholes) | 5,5735 |
| Put américain (arbre, 3 000 pas) | 6,0901 |
| Valeur du droit d'exercer le put avant l'échéance (arbre à 800 pas) | 0,52, soit 9,3 % du prix européen |
| Erreur de l'arbre multipliée par $N$ (call) | environ 2 : l'erreur est divisée par 2 quand on double le nombre de pas |
| Monte Carlo, 10 000 simulations, put | $5{,}741 \pm 0{,}171$ |
| Monte Carlo avec variable de contrôle, mêmes simulations | $5{,}644 \pm 0{,}111$ |

Lecture des résultats :
- L'erreur de l'arbre diminue comme $1/N$. Elle ne baisse pas de façon régulière : elle monte et descend selon la position du strike par rapport aux points de l'arbre. D'un $N$ au suivant, elle varie d'un facteur 1,5 environ.
- La variable de contrôle divise la variance du résultat par 2,4 (la variance mesure la dispersion des estimations). L'intervalle d'erreur est donc plus étroit avec les mêmes simulations.
- Le put américain vaut plus que le put européen, car le droit d'exercer plus tôt a une valeur.
- Le seuil d'exercice du put américain (le prix de l'action en dessous duquel il vaut mieux exercer) monte de 81 (vers $t = 0{,}05$ an) jusqu'à 100 à l'échéance.

## Tests

Chaque test compare un résultat à une valeur exacte ou à une propriété connue :
- le call de référence vaut 10,4506 ;
- la relation entre le call et le put (la parité) est vérifiée dans la formule et dans l'arbre ;
- la pente de l'erreur de l'arbre est $-1$, à 0,1 près ;
- un call américain sans dividende vaut le call européen ;
- un put américain vaut au moins 0,1 de plus que le put européen ;
- les paramètres impossibles sont refusés avec un message d'erreur.

## Lancer le projet

```
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

La page interactive s'ouvre en double-cliquant sur `lab/index.html`.

## Limites

- La volatilité est constante, alors que celle du marché varie.
- Les paramètres ne sont pas ajustés sur des prix réels.
- Monte Carlo calcule seulement le prix de l'option européenne.
- Monte Carlo, les sensibilités et l'exercice anticipé n'ont pas encore de tests en Python.

## Ce que je n'ai pas approfondi

- Je n'ai pas redémontré les formules utilisées : je les applique telles qu'elles sont établies.
- Je mesure que l'erreur de l'arbre est en $1/N$, mais je n'en ai pas démontré la cause.
- J'utilise la formule de $\beta$ de la littérature pour la variable de contrôle, sans démontrer qu'elle est optimale.
- Je n'ai pas testé le modèle sur des prix de marché réels.
