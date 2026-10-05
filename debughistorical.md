# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-05

## Rôle
Faits de diagnostic utiles à JT-SETS-001. Historique ancien : `archive/memories/2026-10-04-pre-main-merge/`.

## Baseline JT-SETS-001
- Base : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Archive canonique SHA `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- Main préparé SHA `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.
- Run Lot 01 `37339853652` GREEN ; 38 tests OK.
- Diagnostic temporaire supprimé ; final tree sans diff produit par rapport à la base.

## Lot 01 — faits structurants
1. `app/main.py` n’est pas versionné : toute analyse gameplay doit repartir de l’archive prouvée + préparateur.
2. `deg[21..26]=181..186` sont des jalons de frame, pas des montants de dégâts.
3. Effets bruts actuels : 21 `degd+=pvd/4`; 22 `degg-=pvg/4`; 23 `degd+=pvd/4`; 24 `degg+=pvg/4`; 25 `degg+=pvg/4`; 26 `degg+=pvg/3`.
4. Hors jalon 182, le traitement partagé convertit les deltas en énergie puis lisse les nouveaux dégâts de 1/4 ; modifier les dégâts modifie donc aussi l’énergie.
5. Jalon 182 = soin : pas de calcul/lissage énergie correspondant ; `affpv` borne `degg` à zéro.
6. L’EOS MP4 ne produit aucun nouvel impact ; génération/player guards rejettent les callbacks périmés. `video_complete` ne fait que libérer la phase.
7. ZeroWin est encore installé en mutant le `SCENES` global ; dette ciblée Lot 02.

## Risques suivants
- Lot 02 : équivalence stricte du mapping canonique via résolveur ; aucune fuite globale ZeroWin.
- Futur changement de set : invalider lecteurs, callbacks, textures et reprise vidéo.
- Import : garder les gardes taille/SHA et refuser code/chemins hors racine.
- Lot 06 : aucune valeur d’équilibrage ouverte sans validation Fab et tests PV+énergie.

## Règle
Tests CI != validation téléphone. Aucun bug ou correctif annoncé sans preuve fraîche.
