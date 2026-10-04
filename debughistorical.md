# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-04

## Rôle
Incidents encore utiles au diagnostic courant et dernières résolutions structurantes seulement. Historique intégral : `archive/memories/2026-10-04-pre-main-merge/debughistorical.md`.

## Promotion vers main — résolue
- PR #1 fusionnée.
- Merge fonctionnel : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Inspection média #24 : succès.
- Build Android #76 (`37203568079`) : succès complet.
- Release `v1.0.15-main` publiée depuis ce merge.
- APK `JuneT-Rex-1.0.15-debug.apk` : 156791394 octets.
- SHA-256 APK : `2fbad1d19084fa7ad2c00ac81156ef0c5db0c933b679075df3ddf7fbb5f330b1`.
- Les anciens médias racine propres à l’ancien `main` restent dans l’historique Git mais n’ont pas été réintroduits dans l’arbre canonique final.

## Résolus — ne pas rouvrir sans preuve
### Bootstrap Android / zlib
Ancien crash `zlib.cpython-312.so` / `PyExc_MemoryError` résolu dans la chaîne native. Ne pas restaurer les anciens contournements sans reproduction actuelle.

### KO / rounds
- Verdicts de jauges ≠ victoire de round.
- Seul un KO réel incrémente la victoire.
- Deux rounds gagnés terminent le match.

### Orbes / chrono
Tout nouvel échange prépare :
- `car2 = 10` ;
- `stopg/stopd = False` ;
- `colstop` effacé ;
- causes d’arrêt périmées supprimées.

Retour d’un pouvoir : pas un nouvel échange ; conserver `car2` restant.

### Énergie
Vrai nouveau round après KO : `stamg = 0` et `stamd = 0`.

### Média d’attente
Wait canonique : `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4`. L’ancien `StegVsTrexvaetviensremolace*` ne doit pas revenir dans runtime/manifest.

## Preuves plage
- H.264 852x480, 24 fps, AAC 44.1 kHz, durée ~44.916667 s.
- SHA-256 : `71b1abe5498d7e9f5dfd61cccede099759c49ec0a82324e8dd76b8c054dccd9d`.
- Git blob : `908d0f2ba5ef9a9da4b1316ff28ec21e7bce04ee`.

## Si régression téléphone
Capturer avant correction : phase, média actif, `car2`, `stamg/stamd`, états stop, cause de transition. Puis vérifier :
1. deux nouveaux échanges = 10 s chacun ;
2. retour pouvoir = temps restant ;
3. verdict/FIGHT ne bloque pas les orbes ;
4. KO -> round suivant = énergie 0/0 ;
5. plusieurs EOS plage sans conséquence gameplay ;
6. finishings/pouvoirs jusqu’à EOS réel lorsque requis.

## Règle
Reproduire et mesurer avant correctif. Une ancienne hypothèse archivée n’est jamais une preuve du bug courant.
