# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-07

## Mission
JT-SETS-001 sur `feature/dinosaur-sets-v1` : plusieurs sets DATA + MEDIA autour d'un seul moteur historique.

## Lots acquis
- 01–03 : contrat/manifeste/résolution + sélection persistante/session figée.
- 04 : stockage séparé + ZIP sûr/transactionnel + `content://`.
- 05 : sets utilisateur promus, brouillons/atelier 20 touches, preview, SAF, test temporaire.
- 06 : six coefficients de pouvoirs bornés, approuvés par Fab.

## Lot 06 — faits utiles
- `parameters:{}` = valeurs canoniques.
- STSF/STTA/TRFS/TRPH : dégâts défaut 25 %, bornes 10–40 %.
- Lifestream : soin défaut 25 %, bornes 10–40 %.
- Meteor : dégâts défaut 1/3, bornes 15–50 %.
- Valeurs finies seulement ; bool/NaN/infini/hors-bornes/clé étrangère refusés.
- Le moteur conserve coûts, cibles/mécanismes, jalons, lissage/énergie, chrono, KO, score, EOS et réarmement.
- Lifestream reste plafonné et sans énergie dérivée au jalon 182.
- Produit `8d89c1ed7a70f7e55bac4e6895020a2bbd8995d2`; CI final `d7214bb514e144dfa9191c1d6f3064718b91c570`.
- Android #89 `37576480368` SUCCESS ; 174/174 tests.
- APK : 156528315 octets ; SHA-256 `4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`.

## Canon
3 orbes/camp ; 10 s nouvel échange ; temps restant après pouvoir ; KO réel seul ; 2 rounds = match ; énergie 0 au vrai nouveau round ; coûts 60/40/60/60/60/80 ; `energy > cost`.

## Suite
Validation téléphone du candidat Lot 06 si Fab le souhaite. Aucun merge `main` ni Release sans ordre.


## JT-SETS-UI-001
Correction téléphone autorisée : remplacer le bandeau de set surdimensionné par `SET ▼` compact, ajouter ✎ admin, rendre atelier/création/catalogue/brouillons/assistant scrollables. Gameplay inchangé.


## JT-SETS-UI-002
Finition téléphone : sélecteur centré/compact ASCII, boutons moins larges et plus aérés, aperçu réparé (ancien preview fermé avant démarrage du nouveau), garde MENU du dinosaure visuel droit pour conserver le bord tronqué de l'asset hors écran. Asset et gameplay inchangés.


## JT-SETS-UI-003
Le saut du dinosaure droit venait d'un timer post-rendu. Timer supprimé. `prepare_android.py` injecte désormais la borne dans l'affectation visuelle canonique `self.jb.pos`, avant affichage et seulement en menu (`indexa==0`). Logique `xb/yb`, taille et asset inchangés.


## JT-SETS-UI-004
Le clamp pré-rendu fonctionne sans saut. Ajustement téléphone : le dino droit doit être plus décalé hors écran. Seule la marge visuelle passe à 40 % de sa largeur ; logique, taille et asset inchangés.
