# JTREX — JT-SETS-001 — Contrat paramètres Lot 06

Date : 2026-10-07
Statut : approuvé explicitement par Fab
Branche : `feature/dinosaur-sets-v1`

## But

Ouvrir uniquement les six coefficients d'effet déjà audités, sans déplacer les règles de combat hors du moteur.

## Champs autorisés

| Slot | Clé | Défaut canonique | Bornes inclusives |
| --- | --- | ---: | ---: |
| `left_1` | `raw_damage_fraction` | 0.25 | 0.10 .. 0.40 |
| `left_2` | `heal_fraction` | 0.25 | 0.10 .. 0.40 |
| `left_3` | `raw_damage_fraction` | 0.25 | 0.10 .. 0.40 |
| `right_1` | `raw_damage_fraction` | 0.25 | 0.10 .. 0.40 |
| `right_2` | `raw_damage_fraction` | 0.25 | 0.10 .. 0.40 |
| `right_3` | `raw_damage_fraction` | 1/3 | 0.15 .. 0.50 |

Les valeurs doivent être numériques finies ; `bool`, NaN et infinis sont refusés.

## Rétrocompatibilité

Le format v1 reste lisible :
- `parameters: {}` signifie « valeur canonique par défaut » ;
- un manifeste Lot 06 peut utiliser exactement l'unique clé autorisée du slot ;
- aucune autre clé n'est acceptée ;
- aucun script, expression ou formule ne peut être fourni par le pack.

Le runtime expose toujours une valeur normalisée au moteur, même si le manifeste utilise `{}`.

## Sémantique moteur

Les coefficients modifient seulement l'écriture brute historique au jalon moteur existant :
- états 21/23 : dégâts bruts droite = vie max droite × coefficient ;
- état 22 : soin gauche = vie max gauche × coefficient, toujours plafonné par les dégâts réellement subis ;
- états 24/25/26 : dégâts bruts gauche = vie max gauche × coefficient.

Tout le traitement historique qui suit reste identique, notamment lissage et énergie dérivée pour les attaques.

## Valeurs qui restent moteur-owned

Ne sont jamais éditables au Lot 06 :
- coûts 60/40/60/60/60/80 ;
- condition stricte `énergie > coût` ;
- mécanismes et camps/cibles ;
- états 21..26 ;
- jalons 181..186 ;
- chrono des orbes et reprise après pouvoir ;
- KO, rounds, victoire match ;
- vie initiale, score ;
- formules de lissage et d'énergie dérivée ;
- EOS, durée MP4, `play_to_end`, `loop` ;
- réarmement `selected`.

## UI atelier

L'atelier 20 touches affiche six réglages lisibles en pourcentage.
- pas de champ de formule ;
- pas de coût d'énergie ;
- pas de jalon ;
- changement borné immédiatement ;
- remise au défaut canonique disponible ;
- le brouillon reste testable avant installation/promotion.

## Preuves obligatoires

- défauts Lot 06 = comportement canonique exact ;
- bornes min/max acceptées, hors bornes refusé ;
- NaN/infini/bool/clé étrangère refusés ;
- round-trip ZIP conserve les paramètres ;
- import Lot 05 avec `{}` reste valide ;
- chaque slot modifié change uniquement son coefficient brut ;
- Lifestream reste plafonné et sans gain énergie au jalon 182 ;
- attaques conservent l'énergie dérivée/lissage historiques ;
- coûts, chrono, KO, EOS et jalons inchangés ;
- test brouillon et session promue utilisent le même paramétrage figé.
