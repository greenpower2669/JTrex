# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-05

## Git
- Base JT-SETS-001 : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Travail : `feature/dinosaur-sets-v1`.
- Lot 01 audit/contrat terminé ; Lot 02 runtime/manifeste terminé ; prochain = Lot 03.
- Produit Lot 02 : `017d611cf798d4713af8039ee6962d1fe6729fd2`.
- Workflow Android exact : `ee8cf297830e1f40d984ab6b1706733eff22e5d7`, blob `c22bcf40038889318a3cab7c25d6c8c78dd87c49`.
- Dernière Release : `v1.0.15-main`.

## Flux actuel
`JuneTrex.zip` -> `tools/prepare_android.py` -> validation catalogue/manifeste -> `app/main.py` + `jtrex_sets_runtime` + `jtrex_phase_runtime` + `jtrex_media_runtime` -> tests -> Android.

## Frontières
- `main.py` historique : taps, dégâts, soin, énergie et jalons d'impact.
- `jtrex_phase_runtime.py` : phases/rounds/KO/chrono ; ZeroWin sans mutation globale.
- `jtrex_media_runtime.py` : policies moteur + lecteurs MP4 ; fichiers résolus depuis la sélection du set.
- `jtrex_sets_runtime.py` : charge/valide catalogue+manifeste et confine les chemins.
- Set v1 : identités, médias, images, labels/audio et empreintes ; jamais de code.

## Mapping canonique
ST gauche : 1->21 STSF, 2->22 STLS, 3->23 STTA.
TR droite : 4->24 TRFS, 5->25 TRPH, 6->26 TRMA.
Coûts : 60/40/60/60/60/80. Jalons : 181/182/183/184/185/186.

## Preuves
- Run Lot 02 `37378554085` : 56/56 tests OK.
- Run Android exact #80 : run #80 `37379193862` GREEN ; artefact APK `11375685200` ; `JuneT-Rex-1.0.15-debug.apk` = 156461520 octets, SHA-256 `182e1b8f72f269a7e3f3f24895e37fe23a1b3ade9e77949d14500827c13c320c`.

## Couches prévues
Lot 03 sélection joueur persistante/figée.
Lot 04 I/O officiel-utilisateur-brouillon et ZIP sûr.
Lot 05 atelier/admin/aperçu/test brouillon.
Lot 06 paramètres validés par Fab.
