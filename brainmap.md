# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-05

## Git
- Canon : `main` @ `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e` au démarrage JT-SETS-001.
- Travail : `feature/dinosaur-sets-v1`.
- Design : `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`.
- Plan Lot 01 : `docs/superpowers/plans/2026-10-05-jtrex-sets-lot01.md` ; attente validation Fab.
- Dernière Release : `v1.0.15-main`.
- Build #78 / `37245309424` : CI verte ; validation téléphone complète non enregistrée.

## Flux existant
`JuneTrex.zip` -> `tools/prepare_android.py` -> `app/main.py` généré -> runtime phase + runtime média -> tests -> Buildozer/p4a -> APK.

## Composants actuels
- `tools/prepare_android.py` : adaptation Android, coûts, ressources/tailles.
- `tools/jtrex_phase_runtime.py` : phases, KO, rounds, chrono, ZeroWin actuellement injecté dans le catalogue média global.
- `tools/jtrex_media_runtime.py` : `INTRO_FILES`, `SCENES`, résolution, lecteurs, EOS, reprise wait, admin 20 touches.
- `tests/runtime_harness.py` + tests phase/KO/orbes/média : canon de non-régression.

## Lot 01
`JuneTrex.zip` prouvé -> `app/main.py` généré -> inventaire identité/média/slots -> inventaire mécanismes/paramètres -> contrat format v1. Aucun code produit de sets dans ce lot.

## Couches JT-SETS-001 prévues après Lot 01
- `jtrex_sets_runtime` : contrat + catalogue + validation + résolution + sélection figée.
- `jtrex_sets_io` : stockage officiel/utilisateur/brouillon + import/export transactionnel.
- `jtrex_sets_admin` : atelier 20 touches + aperçu indépendant + test brouillon.
- `assets/sets/catalog.json` + manifeste canonique.

## Frontières
SET -> données/médias/paramètres autorisés.
MOTEUR -> états, transitions, KO, rounds, chrono, coûts, jalons d’impact, EOS, protections.
APERÇU -> décodeur média uniquement, aucun callback gameplay.
IMPORT -> aucun code exécutable, aucun accès libre au système de fichiers.

## Ordre
Lot 01 inventaire/contrat -> Lot 02 manifeste/résolution -> Lot 03 menu/sélection -> Lot 04 I/O -> Lot 05 atelier/test -> Lot 06 paramètres validés par Fab.
