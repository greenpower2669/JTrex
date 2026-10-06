# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-06

## Mission active
JT-SETS-001 sur `feature/dinosaur-sets-v1` ; base `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.  
But : plusieurs sets DATA + MEDIA, un seul moteur de combat, set canonique équivalent.

## Lots acquis
- Lot 01 : inventaire + contrat v1.
- Lot 02 : runtime/catalogue/manifeste canonique + résolution centrale.
- Lot 03 : sélection persistante, session figée, identités pouvoirs set-aware.
- Lot 04 : stockage séparé, ZIP auto-contenu sûr/transactionnel, copie `content://`.
- Lot 05 : sets utilisateur promus + résolveur propre, brouillons autonomes/reprenables, atelier caché 20 touches, assistant DATA/MEDIA, preview isolée, Android SAF/egress asynchrone, test temporaire du brouillon et promotion explicite.

## Lot 05 — faits utiles
- L'import n'est jamais promu automatiquement.
- Un set utilisateur lit ses ressources dans sa révision installée ; pas de fallback homonyme vers l'officiel.
- Le joueur voit uniquement officiel + révisions utilisateur explicitement promues.
- Preview : un lecteur, génération anti-stale, aucune surface gameplay.
- `TESTER CE SET` = session temporaire mémoire ; aucune préférence/promotion écrite ; retour MENU restaure le normal.
- Six libellés de pouvoirs sont éditables ; mécanismes, `parameters`, coûts, dégâts, chrono, KO, EOS et jalons restent fermés.
- HEAD produit `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17`.
- CI : 152/152 tests ; Android #85 `37515396288` SUCCESS.
- APK : 156521694 octets ; SHA-256 `fd08bc534da84fc8753cbc30bb7e8200eda2fcd3a3cbe0a6ea98147867673cc2`.

## Canon gameplay
- 3 orbes/camp ; nouvel échange 10 s ; retour pouvoir conserve le temps.
- KO réel seul ; 2 rounds = match ; vrai nouveau round énergie 0/0.
- Vie 500000000/camp ; score historique inchangé.
- Coûts 60/40/60/60/60/80 ; disponibilité `energy > cost`.
- Impacts au jalon historique ; EOS n'applique aucun effet supplémentaire.

## Prochain geste
Lot 06 seulement après validation explicite par Fab des paramètres de pouvoirs éditables et de leurs bornes. Pas de merge `main` ni Release sans Fab.
