# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-06

## Git
- Base JT-SETS-001 : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Travail : `feature/dinosaur-sets-v1`.
- Lots 01 audit/contrat, 02 runtime/manifeste, 03 sélection/session et 04 stockage/ZIP terminés.
- Produit Lot 04 : `156ee830155bc34c840a83666de20fca43fb72d8`.
- HEAD validation Android Lot 04 : `d0a56cf364f88a677f22f986d04eac5bcbe33054`.
- Dernière Release : `v1.0.15-main`.

## Flux actuel
`JuneTrex.zip` -> `tools/prepare_android.py` -> catalogue/manifeste -> main généré + runtimes sets/phase/media/I-O -> sélection persistée -> session figée -> tests -> Android.

## Frontières
- `main.py` historique : taps, dégâts, soin, énergie, score et jalons d'impact.
- `jtrex_phase_runtime.py` : phases/rounds/KO/chrono.
- `jtrex_media_runtime.py` : lecteurs MP4, menu de sets, session figée, génération et identités de pouvoirs.
- `jtrex_sets_runtime.py` : contrat fermé, catalogue officiel, persistance/fallback, validation portable et session immuable.
- `jtrex_sets_io.py` : racines officiel/utilisateur/brouillon, ingress `content://`, import/export ZIP et installation transactionnelle.
- Set v1 : identités, médias, images, labels/audio et empreintes ; jamais de code ni formule gameplay.

## Sécurité ZIP v1
- ZIP <=512 MiB ; extrait <=1 GiB ; <=512 fichiers ; <=512 MiB/fichier ; manifeste <=1 MiB ; chemin <=240 caractères.
- Traversée, absolu/backslash/drive/NUL, doublon casefold, symlink, entrée chiffrée, extra non référencé et exécutable refusés.
- Taille/SHA contrôlés sur octets réellement copiés ; installation finale par renommage atomique sans écraser une révision existante.

## Mapping canonique
ST gauche : 1->21 STSF, 2->22 STLS, 3->23 STTA.
TR droite : 4->24 TRFS, 5->25 TRPH, 6->26 TRMA.
Coûts : 60/40/60/60/60/80. Jalons : 181/182/183/184/185/186.

## Preuves Lot 04
- 106/106 tests verts après préparation canonique.
- Run Android #84 `37477862014` SUCCESS sur `d0a56cf364f88a677f22f986d04eac5bcbe33054`.
- Artefact `11421465099` ; APK 156478186 octets ; SHA-256 `759b574f49abd7f08e4607de6117fa856e005a39a0c0c72909432ac17509fedb`.

## Couches prévues
Lot 05 atelier 20 touches + assistant par rôle + aperçu indépendant + test brouillon.
Lot 06 paramètres validés explicitement par Fab.
