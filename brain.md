# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-04

## Rôle
Canon opérationnel actuel uniquement. L’historique complet pré-consolidation est conservé bit pour bit sous `archive/memories/2026-10-04-pre-main-merge/`.

## État Git / Android actuel
- Branche canonique : `main`.
- Merge Android vers `main` : PR #1, fusionnée.
- Merge commit fonctionnel : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Inspection média sur `main` : run #24, succès.
- Build Android sur `main` : run #76 (`37203568079`), succès complet.
- Release canonique issue du `main` fusionné : `v1.0.15-main`.
- APK : `JuneT-Rex-1.0.15-debug.apk`.
- Taille APK : 156791394 octets.
- SHA-256 APK : `2fbad1d19084fa7ad2c00ac81156ef0c5db0c933b679075df3ddf7fbb5f330b1`.
- Ancienne Release candidat pré-merge : `v1.0.15` ; elle reste historique.

## Règles gameplay canoniques
- 3 orbes par camp.
- Tout nouvel échange d’orbes démarre avec 10 s complets.
- Retour d’un pouvoir : conserver le temps restant, ne pas réinitialiser à 10 s.
- Seul un KO réel compte comme victoire de round.
- Deux rounds gagnés terminent le match.
- Nouveau vrai round après KO : énergie ST = 0 et TR = 0.
- Vie historique : `pvg = pvd = 500000000`.
- Score : `S=max(0,150000000-Σe³)` ; seuil égalité 20000 ; lettres S..F.

## Pouvoirs — coûts canoniques
- ST : 60 / 40 / 60.
- TR : 60 / 60 / 80.
- Condition stricte : `énergie > coût`, jamais `>=`.
- Énergie fractionnaire conservée.
- Un seul usage par slot et par combat.

## Médias canoniques
- Fond attente/orbes : `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4`.
- L’ancien média `StegVsTrexvaetviensremolace*` est retiré du runtime canonique et n’a pas été réintroduit au merge.
- La vidéo plage boucle sans verrou cinématique ; EOS sans conséquence gameplay.
- Pouvoirs et finishings MP4 conservent leur verrou jusqu’à EOS réel.

## Runtime Android
- `tools/prepare_android.py` : préparation du source historique.
- `tools/jtrex_phase_runtime.py` : phases, rounds, KO, chrono orbes.
- `tools/jtrex_media_runtime.py` : médias, EOS, boucle/reprise attente.
- Python Android 3.12.14 ; FFmpeg 6.1.2 ; ffpyplayer 4.5.1.
- ABI : arm64-v8a + armeabi-v7a.
- Package : `com.junedady.junetrex`.

## Méthode
- Ne jamais recoder depuis la mémoire : relire code, tests et preuves.
- `ordres-de-mission.md` = contrat actif.
- Fichiers vivants courts ; historique et règles supersédées en archive.
- Séparer faits vérifiés, retours téléphone et hypothèses.

## Validation téléphone encore utile
1. deux nouveaux échanges d’orbes successifs démarrent chacun à 10 s ;
2. retour d’un pouvoir conserve le chrono restant ;
3. aucune saisie orbe bloquée après transition normale ;
4. KO -> nouveau round remet ST/TR à 0 ;
5. plusieurs boucles plage restent continues ;
6. finishings/pouvoirs vont jusqu’à EOS lorsque requis.

## Archive
Snapshot complet pré-consolidation : `archive/memories/2026-10-04-pre-main-merge/brain.md`.
