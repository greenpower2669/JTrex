# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-07

## Git
- Base JT-SETS : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Branche : `feature/dinosaur-sets-v1`.
- Lots 01–06 terminés code/CI.
- Produit Lot 06 : `8d89c1ed7a70f7e55bac4e6895020a2bbd8995d2`.
- HEAD CI final : `d7214bb514e144dfa9191c1d6f3064718b91c570`.
- Dernière Release : `v1.0.15-main`.

## Flux
`JuneTrex.zip` → `prepare_android.py` → manifeste/catalogue → runtimes sets/I-O/admin/preview/Android/media/phase → set figé → paramètres normalisés → moteur historique → tests → Android.

## Frontières
- `main.py` généré : effets réels, coûts, énergie, score, jalons.
- `jtrex_sets_runtime.py` : schéma + normalisation des six coefficients.
- `jtrex_sets_admin.py` : édition bornée dans brouillon.
- `jtrex_media_runtime.py` : applique au moteur les valeurs du set figé + UI atelier.
- Les autres runtimes Lot 05 gardent leurs responsabilités stockage/preview/SAF/phases.

## Preuves Lot 06
- validation patch : 173/173.
- Android #89 `37576480368` : 174/174 + BUILD SUCCESSFUL.
- APK artifact `11462494872` : 156528315 octets ; SHA-256 `4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`.
- #86 a échoué uniquement sur un garde CI Lot 05 obsolète ; régression RED→GREEN enregistrée.

## Suite
Validation téléphone réelle du candidat. Pas de merge/main Release/AAB automatique.


## UI téléphone — JT-SETS-UI-001
`jtrex_media_runtime.py` : contrôles SET compacts, ScrollView atelier/création/catalogue/brouillons/assistant, navigation précédent/étape/suivant, ✎ admin vers copie officielle ou édition utilisateur.


## UI téléphone — JT-SETS-UI-002
`jtrex_media_runtime.py` : `SET v` + `MOD` centrés, contrôles plus compacts, preview lifetime corrigé, garde périodique MENU sur le rectangle dinosaure visible le plus à droite (`jh/jb`) sans changement d'asset.


## UI téléphone — JT-SETS-UI-003
`prepare_android.py` repère l'unique `self.jb.pos` historique et remplace son rendu par `_jt_jb_render_pos` + minimum X menu. `jtrex_media_runtime.py` ne possède plus de timer de rattrapage du dinosaure.


## UI téléphone — JT-SETS-UI-004
`prepare_android.py` : `_jt_jb_safety=max(24.0,self.jb.size[0]*0.40)`. Même point d'injection pré-rendu, seulement plus à droite.


## UI téléphone — JT-SETS-UI-005
`prepare_android.py` injecte deux constantes : `JT_SELECTION_RIGHT_VISUAL_EDGE_RATIO=174/320` et `JT_SELECTION_RIGHT_OVERHANG_RATIO=0.02`. `self.jb.pos` est borné avant rendu à partir de `self.x+self.width`, pas depuis le centre ni depuis un pourcentage de la largeur du dinosaure.

## UI téléphone — JT-SETS-UI-006
Deux bornages en MENU : `jh` MAX depuis bord gauche parent, `jb` MIN depuis bord droit parent. Les affectations historiques restent les sources du Y et du mouvement vers l'extérieur. Modifications `prepare_android.py` + gardes CI.
