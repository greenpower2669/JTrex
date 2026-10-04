# JTREX — BRAINMAP VIVANTE

Dernière consolidation : 2026-10-04

## But
Carte courte du système actuel. Pour l’historique complet : `archive/memories/2026-10-04-pre-main-merge/brainmap.md`.

## Flux de build
`JuneTrex.zip` historique -> `tools/prepare_android.py` -> `app/main.py` généré -> injection runtime phase + média -> validations -> Buildozer / p4a -> APK.

## Composants
- `tools/prepare_android.py` : adaptation du source historique Android.
- `tools/jtrex_phase_runtime.py` : phases, rounds, KO, transitions, chrono orbes.
- `tools/jtrex_media_runtime.py` : catalogues MP4, boucle attente, EOS, reprise, audio.
- `tests/runtime_harness.py` : environnement de test du runtime généré.
- `tests/test_round_ko_contract.py` : contrat KO / rounds.
- `tests/test_orb_presentation.py` : contrat chrono et transitions orbes.
- `tests/test_orb_media_manifest.py` : média plage obligatoire et ancien wait interdit.
- `tests/test_phase_integration.py` : intégration des phases.

## Phases essentielles
- Intro / présentation : gameplay gelé.
- Orbes actifs : saisie + chrono `car2`.
- Pouvoir : verrou cinématique jusqu’à EOS ; retour vers orbes avec chrono restant.
- Verdict/jauges : présentation, jamais victoire de round à elle seule.
- KO réel : incrémente la victoire de round.
- Nouveau round : nettoie état combat et remet l’énergie ST/TR à 0.
- Fin de match : après deux rounds gagnés.

## État orbes canonique
Nouvel échange :
- `car2 = 10` ;
- `stopg = False`, `stopd = False` ;
- `colstop[1..6] = False` ;
- causes d’arrêt périmées supprimées.

Retour de pouvoir :
- ne passe pas par la préparation d’un nouvel échange ;
- conserve donc `car2` restant.

## Carte médias
- attente/orbes : `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` ; boucle continue ; non cinématique.
- charge / verdicts : `assets/combat/*.mp4`.
- pouvoirs : `assets/powers/*.mp4`.
- finishings : `assets/finishing/*.mp4`.
- intros : `assets/intro/*.mp4`.

## Coûts pouvoirs
`POWER_COSTS={1:60,2:40,3:60,4:60,5:60,6:80}` avec disponibilité stricte `energy > cost`.

## Preuves de référence
- candidat fonctionnel : `ed1842bae1176ffb08d76905b597a548c7ecf382` ;
- build #75 : succès ;
- release `v1.0.15` ;
- APK SHA-256 : `54f5490ccf346b3e80e3117b4cf020b24898ad89cb44e6a2bd6bf73051d99c11` ;
- vidéo plage Git blob : `908d0f2ba5ef9a9da4b1316ff28ec21e7bce04ee`.

## Règle de maintenance
Quand une règle est remplacée : conserver seulement le canon ici et déplacer le détail historique dans `archive/`.
