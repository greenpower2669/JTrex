# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-04

## Rôle de ce fichier
Ce fichier contient uniquement le canon opérationnel actuel. Les historiques complets antérieurs à cette consolidation sont conservés sous `archive/memories/2026-10-04-pre-main-merge/`.

## Dépôt et branche de référence
- Dépôt : `greenpower2669/JTrex`
- Branche de travail historique Android : `port/android-first-apk`
- Candidat fonctionnel validé : `ed1842bae1176ffb08d76905b597a548c7ecf382`
- Build Android validé : workflow `Build June T-Rex APK`, run #75, succès.
- Release Android publiée avant merge main : `v1.0.15`.
- APK : `JuneT-Rex-1.0.15-debug.apk`
- SHA-256 APK : `54f5490ccf346b3e80e3117b4cf020b24898ad89cb44e6a2bd6bf73051d99c11`

## Règles de gameplay canoniques
- 3 orbes par camp.
- Nouvelle séquence d’orbes : fenêtre pleine de 10 s.
- Retour d’un pouvoir vers les orbes : conserver le temps restant, ne pas réinitialiser à 10 s.
- Un KO réel seul compte comme victoire de round.
- Deux rounds gagnés déclenchent la fin du match.
- Nouveau vrai round après KO : énergie ST = 0 et TR = 0.
- Vie historique : `pvg = pvd = 500000000`.
- Score : `S=max(0,150000000-Σe³)` ; seuil d’égalité 20000 ; lettres S..F.

## Pouvoirs — coûts canoniques
- ST : 60 / 40 / 60.
- TR : 60 / 60 / 80.
- Condition stricte : `énergie > coût`, jamais `>=`.
- Énergie fractionnaire conservée.
- Un seul usage par slot et par combat.

## Médias canoniques
- Fond d’attente/orbes : `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4`.
- L’ancien média `StegVsTrexvaetviensremolace*` est retiré du runtime canonique.
- La vidéo plage boucle sans verrou cinématique ; l’EOS n’a aucune conséquence gameplay.
- Les pouvoirs et finishings MP4 conservent leurs verrous jusqu’à l’EOS réel.

## Runtime Android actuel
- `tools/prepare_android.py` prépare le source historique dans `app/` au build.
- `tools/jtrex_phase_runtime.py` porte le modèle de phases/rounds.
- `tools/jtrex_media_runtime.py` porte la lecture média, les verrous et la reprise de la boucle d’attente.
- Python Android : 3.12.14.
- FFmpeg : 6.1.2.
- ffpyplayer : 4.5.1.
- ABI : arm64-v8a + armeabi-v7a.
- Package : `com.junedady.junetrex`.

## Contrat de méthode
- Ne jamais recoder depuis la mémoire : toujours relire le code et les preuves.
- `ordres-de-mission.md` est le contrat de travail.
- Les fichiers vivants doivent rester courts : état actuel, preuves, actions restantes.
- Tout détail ancien ou supersédé va en archive, pas en append infini.
- Séparer faits vérifiés, retours téléphone et hypothèses.

## Validation téléphone encore utile
Après chaque candidat majeur, vérifier au minimum :
1. deux échanges d’orbes successifs démarrent chacun avec 10 s ;
2. retour d’un pouvoir conserve le chrono restant ;
3. aucune saisie d’orbe n’est refusée après une transition normale ;
4. KO -> nouveau round remet bien les deux énergies à 0 ;
5. plusieurs boucles successives de la vidéo plage restent continues.

## Archive
Snapshot complet pré-consolidation : `archive/memories/2026-10-04-pre-main-merge/brain.md`.
