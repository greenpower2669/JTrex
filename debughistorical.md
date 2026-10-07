# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-07

## Baseline
- Archive canonique : 327992765 octets ; SHA-256 `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- `app/main.py` est généré, jamais source versionnée.
- `deg[21..26]=181..186` = jalons, pas dégâts.

## Effets historiques / Lot 06
- 21 STSF, 23 STTA : dégâts droite ; 24 TRFS, 25 TRPH : dégâts gauche ; défaut brut 1/4.
- 22 Lifestream : soin gauche défaut 1/4, plafonné par dégâts subis, sans énergie/lissage au jalon 182.
- 26 Meteor : dégâts gauche défaut 1/3.
- Lot 06 remplace uniquement ces fractions brutes par six valeurs validées du set.
- Bornes : 10–40 % pour les cinq quarts ; Meteor 15–50 %.
- Lissage et énergie dérivée des attaques restent historiques ; coûts/jalons/chrono/KO/EOS inchangés.
- `parameters:{}` reste canonique/rétrocompatible.

## Incident CI Lot 06
- Android #86 `37576071180` : FAIL avant compilation sur le garde texte obsolète `parameters are closed in v1`.
- Cause : validation statique CI restée au contrat Lot 05.
- RED : `37576362322` ; GREEN : `37576423433`.
- Fix : le garde vérifie `POWER_PARAMETER_SPECS` et `power_effect_fraction`.
- Android #89 `37576480368` : SUCCESS ; 174/174 ; BUILD SUCCESSFUL.
- APK SHA-256 `4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`.

## Règle
CI verte != validation téléphone. Aucun merge `main`, Release ou AAB sans ordre Fab.


## 2026-10-07 — dette UI Lot 06 observée téléphone
Le candidat CI était fonctionnel mais le bouton DINOSAURES 520dp et plusieurs BoxLayout non scrollables rendaient la création/édition peu accessible. Correctif JT-SETS-UI-001 limité à l'UI ; ajouter une garde de régression sur compacité et ScrollView.
