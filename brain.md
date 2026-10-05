# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-05

## Mission active
JT-SETS-001 sur `feature/dinosaur-sets-v1` ; base `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.

But : plusieurs sets DATA + MEDIA, un seul moteur, set canonique équivalent.

## Lot 01 — acquis
- Inventaire : `docs/jt-sets-001/lot01-inventory.md`.
- Contrat v1 : `docs/jt-sets-001/format-v1-contract.md`.
- Vérification : `docs/jt-sets-001/lot01-verification.md`.
- Run frais `37339853652` : GREEN, 38 tests OK.
- Archive : 327992765 octets, SHA `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- Main préparé SHA `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.
- Aucun code produit/asset/workflow ne diffère de la base après retrait du diagnostic temporaire.

## Canon gameplay
- 3 orbes/camp ; nouvel échange 10 s ; retour pouvoir conserve le temps.
- KO réel seul ; 2 rounds = match ; vrai nouveau round énergie 0/0.
- Vie 500000000/camp ; score historique inchangé.
- Coûts 60/40/60/60/60/80 ; disponibilité `energy > cost`.

## Pouvoirs prouvés
- ST gauche : slot1 état21 STSF cible droite 1/4 ; slot2 état22 STLS soin gauche 1/4 ; slot3 état23 STTA cible droite 1/4.
- TR droite : slot4 état24 TRFS cible gauche 1/4 ; slot5 état25 TRPH cible gauche 1/4 ; slot6 état26 TRMA cible gauche 1/3.
- `deg[21..26]=181..186` = jalons d’animation.
- Les dégâts alimentent aussi l’énergie et passent par le traitement partagé ; STLS/182 est le cas soin exclu de ce calcul/lissage.
- EOS vidéo ne réapplique aucun effet ; il libère la présentation/KO.

## Format v1 initial
- manifeste fermé/versionné, DATA-ONLY ;
- 2 dinos explicites left/right ; 9 rôles média ; 6 pouvoirs ; assets id/path/type/size/SHA-256 ;
- aucun Python/KV/script/formule ;
- paramètres d’équilibrage `parameters:{}` jusqu’au Lot 06 ;
- coûts, états, jalons, EOS, phases et mécanismes restent moteur-owned.

## Prochain geste
Lot 02 : créer manifeste canonique/catalogue/résolveur, faire passer le runtime média par la résolution centrale, sortir ZeroWin de la mutation globale, et prouver l’équivalence canonique. Pas de merge `main` ni Release sans Fab.
