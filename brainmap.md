# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-05

## Git
- Canon au démarrage JT-SETS-001 : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Travail : `feature/dinosaur-sets-v1`.
- Lot 01 audit/contrat terminé ; prochain lot = Lot 02.
- Dernière Release : `v1.0.15-main`.

## Flux existant
`JuneTrex.zip` -> `tools/prepare_android.py` -> `app/main.py` généré -> `jtrex_phase_runtime` + `jtrex_media_runtime` -> tests -> Android.

## Frontières prouvées
- Historique `main.py` : taps, dégâts, soin, énergie, animation-frame impacts.
- `jtrex_phase_runtime.py` : phases/rounds/KO/chrono ; ajoute encore ZeroWin dans `SCENES` global (à retirer Lot 02).
- `jtrex_media_runtime.py` : lecteurs MP4, policies, première frame/audio, EOS ; EOS ne produit aucun nouvel effet gameplay.
- Set v1 : identités, médias, images, labels/audio, assets vérifiés ; pas de code.

## Mapping pouvoirs
ST gauche : 1->21 STSF, 2->22 STLS, 3->23 STTA.
TR droite : 4->24 TRFS, 5->25 TRPH, 6->26 TRMA.
Coûts : 60/40/60/60/60/80.
Jalons : 181/182/183/184/185/186.

## Documents
- Spec : `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`.
- Inventaire : `docs/jt-sets-001/lot01-inventory.md`.
- Contrat : `docs/jt-sets-001/format-v1-contract.md`.
- Vérification : `docs/jt-sets-001/lot01-verification.md`.

## Couches prévues
Lot 02 `jtrex_sets_runtime` + catalogue/manifeste + résolveur.
Lot 03 sélection joueur persistante/figée.
Lot 04 I/O officiel-utilisateur-brouillon et ZIP sûr.
Lot 05 atelier/admin/aperçu/test brouillon.
Lot 06 paramètres validés par Fab.
