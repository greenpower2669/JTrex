# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-06

## Git
- Base JT-SETS-001 : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Travail : `feature/dinosaur-sets-v1`.
- Lots 01 audit/contrat, 02 runtime/manifeste et 03 sélection/session terminés.
- Produit Lot 03 : `dfad8fbc5ae4678fb5bd704ea38a858116966a5b`.
- HEAD validation Android Lot 03 : `c5330f29814430944500839aa3bcd29afbc3ff8b`.
- Dernière Release : `v1.0.15-main`.

## Flux actuel
`JuneTrex.zip` -> `tools/prepare_android.py` -> catalogue/manifeste -> main généré + runtimes sets/phase/media -> sélection persistée au menu -> session figée -> tests -> Android.

## Frontières
- `main.py` historique : taps, dégâts, soin, énergie, score et jalons d'impact.
- `jtrex_phase_runtime.py` : phases/rounds/KO/chrono et notification du changement de phase au média.
- `jtrex_media_runtime.py` : lecteurs MP4, menu de sets, gel de session, invalidation de génération et application des identités de pouvoirs.
- `jtrex_sets_runtime.py` : contrat fermé, catalogue officiel, persistance, fallback canonique et session immuable.
- Set v1 : identités, médias, images, labels/audio et empreintes ; jamais de code ni formule gameplay.

## Mapping canonique
ST gauche : 1->21 STSF, 2->22 STLS, 3->23 STTA.
TR droite : 4->24 TRFS, 5->25 TRPH, 6->26 TRMA.
Coûts : 60/40/60/60/60/80. Jalons : 181/182/183/184/185/186.

## Preuves Lot 03
- 77/77 tests verts, dont deux sessions synthétiques successives et stale EOS/frame A→B.
- Run Android #83 `37417205571` GREEN.
- Artefact APK `11391049002` ; APK 156468471 octets ; SHA-256 `612af2912050c392c63ec2054b03fc875b3a7a4c8f915c3a40d074cb077dec20`.

## Couches prévues
Lot 04 stockage officiel/utilisateur/brouillon + import/export ZIP sûr.
Lot 05 atelier 20 touches + aperçu indépendant + test brouillon.
Lot 06 paramètres validés par Fab.
