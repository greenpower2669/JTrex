# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-05

## But
Carte courte du système courant. Historique complet : `archive/memories/2026-10-04-pre-main-merge/brainmap.md`.

## Référence Git actuelle
- Branche : `main`.
- Merge fonctionnel historique : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Base fonctionnelle actuellement testée : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- Build Android #78 (`37245309424`) : succès.
- APK candidat téléphone : `JuneT-Rex-1.0.15-debug.apk`, SHA-256 `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.
- Validation téléphone : en cours.
- Dernière Release publiée : `v1.0.15-main`.

## Flux de build
`JuneTrex.zip` historique -> `tools/prepare_android.py` -> `app/main.py` généré -> runtime phase + média -> validations -> Buildozer/p4a -> APK.

## Composants
- `tools/prepare_android.py` : adaptation Android du source historique.
- `tools/jtrex_phase_runtime.py` : phases, rounds, KO, transitions, chrono orbes.
- `tools/jtrex_media_runtime.py` : MP4, boucle attente, EOS, reprise, audio.
- `tests/runtime_harness.py` : environnement de test.
- `tests/test_round_ko_contract.py` : contrat KO/rounds.
- `tests/test_orb_presentation.py` : chrono/transitions orbes.
- `tests/test_orb_media_manifest.py` : média d’attente canonique.
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

Retour de pouvoir : conserve `car2` restant.

## Média attente/orbes
`assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` ; boucle non cinématique, EOS sans effet gameplay.

## Coûts pouvoirs
`POWER_COSTS={1:60,2:40,3:60,4:60,5:60,6:80}` ; disponibilité stricte `energy > cost`.

## Étape active
Test téléphone du build #78. Après validation seulement : nettoyage temporaire et éventuelle publication sur ordre explicite de Fab.

## Maintenance
Une règle remplacée quitte le vivant et va dans `archive/`. Le canon actif ne doit pas redevenir un journal chronologique.
