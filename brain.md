# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-05

## Rôle
Canon opérationnel actuel uniquement. L’historique complet pré-consolidation reste archivé sous `archive/memories/2026-10-04-pre-main-merge/`.

## État Git / Android actuel
- Branche canonique : `main`.
- Merge Android fonctionnel historique : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Dernière base fonctionnelle avant consolidation mémoire : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- Build Android #78 (`37245309424`) : succès complet.
- APK candidat téléphone : `JuneT-Rex-1.0.15-debug.apk`.
- Taille : 156445730 octets.
- SHA-256 : `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.
- Validation téléphone : en cours.
- Dernière Release publiée : `v1.0.15-main` ; elle reste la référence publiée tant que Fab n’ordonne pas une nouvelle Release.

## Règles gameplay canoniques
- 3 orbes par camp.
- Tout nouvel échange d’orbes démarre avec 10 s complets.
- Retour d’un pouvoir : conserver le temps restant.
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

## Média d’attente canonique
- `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4`.
- Boucle pendant attente/orbes ; EOS sans conséquence gameplay.
- Pouvoirs et finishings restent verrouillés jusqu’à EOS réel lorsque requis.

## Runtime Android
- `tools/prepare_android.py` : préparation du source historique.
- `tools/jtrex_phase_runtime.py` : phases, rounds, KO, chrono orbes.
- `tools/jtrex_media_runtime.py` : médias, EOS, boucle/reprise attente.
- Python Android 3.12.14 ; FFmpeg 6.1.2 ; ffpyplayer 4.5.1.
- ABI : arm64-v8a + armeabi-v7a.
- Package : `com.junedady.junetrex`.

## Méthode
- Ne jamais recoder depuis la mémoire : relire code, tests et preuves Git.
- `ordres-de-mission.md` = contrat actif.
- Garder les mémoires vivantes courtes ; archiver le reste.
- Séparer faits vérifiés, retours téléphone et hypothèses.

## Validation téléphone active
1. installation et démarrage du candidat build #78 ;
2. deux nouveaux échanges d’orbes successifs à 10 s ;
3. retour d’un pouvoir avec chrono restant conservé ;
4. aucune saisie orbe bloquée après transition normale ;
5. KO -> nouveau round avec ST/TR à 0 ;
6. boucles plage sans effet gameplay à l’EOS ;
7. finishings/pouvoirs jusqu’à EOS réel lorsque requis.

## Archive
Snapshot complet pré-consolidation : `archive/memories/2026-10-04-pre-main-merge/brain.md`.
