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
- Médias et identités des 6 pouvoirs utilisent le même set figé ; coûts/mécanismes/jalons restent moteur-owned.
- 77/77 tests verts ; run #83 GREEN.

### Lot 04
- `tools/jtrex_sets_io.py` porte trois racines séparées : officiel lecture seule, utilisateur persistant, brouillon.
- Pack portable v1 = exactement `manifest.json` + assets référencés ; aucun code exécutable ni ressource extra.
- Import : prévalidation archive, confinement des chemins, refus symlink/chiffrement/doublons, limites centralisées, comptage des octets réels, validation taille/SHA, staging même filesystem puis renommage atomique final.
- Export : validation des assets source, ZIP temporaire frère puis `os.replace` ; collision de révision jamais écrasée.
- `content://` Android est copié vers brouillon avec limite réelle et nettoyage partiel sur erreur.
- Limites v1 : ZIP 512 MiB ; extrait 1 GiB ; 512 fichiers ; 512 MiB/fichier ; manifeste 1 MiB ; chemin 240 caractères.
- Produit `156ee830155bc34c840a83666de20fca43fb72d8` ; validation Android `d0a56cf364f88a677f22f986d04eac5bcbe33054`.
- Préparation canonique + suite : 106/106 tests verts. Run #84 `37477862014` SUCCESS.
- APK : 156478186 octets, SHA-256 `759b574f49abd7f08e4607de6117fa856e005a39a0c0c72909432ac17509fedb`.

## Canon gameplay
- 3 orbes/camp ; nouvel échange 10 s ; retour pouvoir conserve le temps.
- KO réel seul ; 2 rounds = match ; vrai nouveau round énergie 0/0.
- Vie 500000000/camp ; score historique inchangé.
- Coûts 60/40/60/60/60/80 ; disponibilité `energy > cost`.
- Impacts au jalon historique ; EOS n'applique aucun effet supplémentaire.

## Prochain geste
Lot 05 : atelier admin 20 touches + assistant par rôle + aperçu indépendant + test d'un brouillon figé. Paramètres gameplay non éditables avant Lot 06. Pas de merge `main` ni Release sans Fab.
