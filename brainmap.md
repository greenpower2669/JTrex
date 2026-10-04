# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-04

## But
Carte courte du système courant. Historique complet : `archive/memories/2026-10-04-pre-main-merge/brainmap.md`.

## Référence Git actuelle
`main` contient désormais le port Android fusionné.
- PR #1 : fusionnée.
- Merge fonctionnel : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Inspection média #24 : succès.
- Build Android #76 : succès.
- Release : `v1.0.15-main`.
- APK SHA-256 : `2fbad1d19084fa7ad2c00ac81156ef0c5db0c933b679075df3ddf7fbb5f330b1`.

## Flux de build
`JuneTrex.zip` historique -> `tools/prepare_android.py` -> `app/main.py` généré -> runtime phase + média -> validations -> Buildozer/p4a -> APK.

## Composants
- `tools/prepare_android.py` : adaptation Android du source historique.
- `tools/jtrex_phase_runtime.py` : phases, rounds, KO, transitions, chrono orbes.
- `tools/jtrex_media_runtime.py` : MP4, boucle attente, EOS, reprise, audio.
- `tests/runtime_harness.py` : environnement de test.
- `tests/test_round_ko_contract.py` : contrat KO/rounds.
- `tests/test_orb_presentation.py` : chrono/transitions orbes.
- `tests/test_orb_media_manifest.py` : plage requise, ancien wait interdit.
- `tests/test_phase_integration.py` : intégration phases.

## Phases essentielles
- Intro / présentation : gameplay gelé.
- Orbes actifs : saisie + `car2`.
- Pouvoir : verrou jusqu’à EOS ; retour vers orbes avec chrono restant.
- Verdict/jauges : présentation seulement.
- KO réel : victoire de round.
- Nouveau round : nettoie l’état et remet ST/TR à 0.
- Deux rounds gagnés : fin du match.

## Nouvel échange d’orbes
- `car2 = 10` ;
- `stopg = False`, `stopd = False` ;
- `colstop[1..6] = False` ;
- causes d’arrêt périmées retirées.

Retour de pouvoir : ne déclenche pas cette préparation et conserve `car2` restant.

## Carte médias
- attente/orbes : `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` ; boucle non cinématique.
- charges / verdicts : `assets/combat/*.mp4`.
- pouvoirs : `assets/powers/*.mp4`.
- finishings : `assets/finishing/*.mp4`.
- intros : `assets/intro/*.mp4`.

## Coûts pouvoirs
`POWER_COSTS={1:60,2:40,3:60,4:60,5:60,6:80}` ; disponibilité stricte `energy > cost`.

## Preuves média plage
- Git blob : `908d0f2ba5ef9a9da4b1316ff28ec21e7bce04ee`.
- SHA-256 : `71b1abe5498d7e9f5dfd61cccede099759c49ec0a82324e8dd76b8c054dccd9d`.

## Maintenance
Une règle remplacée quitte le vivant et va dans `archive/`. Le canon actif ne doit pas redevenir un journal chronologique.
