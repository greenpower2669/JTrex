# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-06

## Git
- Base JT-SETS-001 : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Travail : `feature/dinosaur-sets-v1`.
- Lots 01 à 05 terminés.
- Produit Lot 05 : `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17`.
- Run Android Lot 05 : #85 `37515396288` SUCCESS.
- Dernière Release : `v1.0.15-main`.

## Flux
`JuneTrex.zip` -> `prepare_android.py` -> manifeste/catalogue -> runtimes sets/I-O/admin/preview/Android/media/phase -> catalogue officiel+promu -> session figée -> tests -> Android.

## Frontières
- `main.py` historique : taps, dégâts, soin, énergie, score, jalons.
- `jtrex_phase_runtime.py` : phases/rounds/KO/chrono.
- `jtrex_media_runtime.py` : médias combat, menu joueur, porte admin 20 touches et orchestration atelier.
- `jtrex_sets_runtime.py` : contrat, catalogue, sélection/session et résolveur propre à chaque set.
- `jtrex_sets_io.py` : stockage, promotions, ZIP, transactions.
- `jtrex_sets_admin.py` : brouillons, progression, rôles et validation DATA/MEDIA.
- `jtrex_sets_preview.py` : aperçu isolé, sans gameplay.
- `jtrex_sets_android.py` : SAF/ingress/egress asynchrones.

## Lot 05
- Officiel et utilisateur distingués dans le menu.
- Import != promotion ; promotion toujours explicite.
- Brouillon auto-contenu et reprenable.
- Aperçu grand format aspect-fit ; vieux callbacks rejetés.
- `TESTER CE SET` gèle un brouillon temporaire sans toucher à la préférence.
- Paramètres gameplay toujours fermés.

## Preuves
- 152/152 tests CI verts.
- Run Android #85 `37515396288` SUCCESS sur `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17`.
- Artefact APK `11437986330` ; 156521694 octets ; SHA-256 `fd08bc534da84fc8753cbc30bb7e8200eda2fcd3a3cbe0a6ea98147867673cc2`.

## Suite
Lot 06 = paramètres de pouvoirs uniquement après validation explicite par Fab des champs et bornes. Aucun merge `main`, Release ou AAB automatique.
