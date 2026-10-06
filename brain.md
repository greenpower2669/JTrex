# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-06

## Mission active
JT-SETS-001 sur `feature/dinosaur-sets-v1` ; base `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
But : plusieurs sets DATA + MEDIA, un seul moteur de combat, set canonique équivalent.

## Lots acquis
### Lot 01
- Inventaire, contrat v1 et preuves dans `docs/jt-sets-001/`.
- Archive canonique : 327992765 octets, SHA `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.

### Lot 02
- `tools/jtrex_sets_runtime.py` = contrat/résolveur DATA-only fermé.
- Catalogue officiel + manifeste `trex_vs_steg` à 41 assets vérifiés.
- Packaging et runtime média consomment la même source de vérité ; ZeroWin sans mutation globale.
- Preuve Android : run #80 `37379193862` GREEN.

### Lot 03
- `JTSetSessionManager` charge le catalogue officiel, persiste la sélection et répare vers `trex_vs_steg` si l'état devient invalide.
- Le menu peut changer de set uniquement hors session ; le set est figé du premier vrai round jusqu'au retour MENU.
- Intro de lancement = dernier set persisté valide ; un changement au menu ne rejoue pas l'intro.
- Changement de set invalide lecteur/reprise/génération ; vieux frame/EOS d'une session A ne peut pas muter une session B.
- Médias et identités des 6 pouvoirs utilisent le même set figé ; 12 icônes ready/used du main généré sont data-driven.
- Coûts, mécanismes, jalons, dégâts, soin, chrono, KO et score restent moteur-owned et inchangés.
- Produit `dfad8fbc5ae4678fb5bd704ea38a858116966a5b` ; validation `c5330f29814430944500839aa3bcd29afbc3ff8b`.
- Suite : 77/77 tests verts. Run Android #83 `37417205571` GREEN.
- APK : 156468471 octets, SHA-256 `612af2912050c392c63ec2054b03fc875b3a7a4c8f915c3a40d074cb077dec20`.

## Canon gameplay
- 3 orbes/camp ; nouvel échange 10 s ; retour pouvoir conserve le temps.
- KO réel seul ; 2 rounds = match ; vrai nouveau round énergie 0/0.
- Vie 500000000/camp ; score historique inchangé.
- Coûts 60/40/60/60/60/80 ; disponibilité `energy > cost`.
- Impacts au jalon historique ; EOS n'applique aucun effet supplémentaire.

## Prochain geste
Lot 04 : stockage officiel/utilisateur/brouillon + import/export ZIP sûr et transactionnel. Pas de merge `main` ni Release sans Fab.
