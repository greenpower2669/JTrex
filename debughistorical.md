# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-05

## Rôle
Incidents encore utiles au diagnostic courant et dernières résolutions structurantes seulement. Historique intégral : `archive/memories/2026-10-04-pre-main-merge/debughistorical.md`.

## État vérifié actuel
- Branche canonique : `main`.
- Merge fonctionnel historique : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Base fonctionnelle actuellement testée : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- Build Android #78 (`37245309424`) : succès complet.
- APK candidat : `JuneT-Rex-1.0.15-debug.apk`, 156445730 octets.
- SHA-256 : `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.
- Validation téléphone : en cours ; aucun nouveau bug runtime ne doit être déclaré sans retour téléphone ou preuve fraîche.
- Dernière Release publiée : `v1.0.15-main`.

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
Wait canonique : `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4`. EOS sans conséquence gameplay.

## Validation téléphone actuelle
En cas de régression, capturer avant correction : phase, média actif, `car2`, `stamg/stamd`, états stop et cause de transition. Vérifier en priorité :
1. deux nouveaux échanges = 10 s chacun ;
2. retour pouvoir = temps restant ;
3. verdict/FIGHT ne bloque pas les orbes ;
4. KO -> round suivant = énergie 0/0 ;
5. boucle attente sans conséquence gameplay ;
6. finishings/pouvoirs jusqu’à EOS réel lorsque requis.

## Règle
Reproduire et mesurer avant correctif. Une ancienne hypothèse archivée n’est jamais une preuve du bug courant.
