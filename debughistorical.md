# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-06

## Baseline JT-SETS-001
- Base : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Archive canonique SHA `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- `app/main.py` n'est jamais une source versionnée : repartir de l'archive prouvée + préparateur.

## Faits structurants
1. `deg[21..26]=181..186` sont des jalons de frame, pas des dégâts.
2. Effets bruts : 21 cible 1/4 ; 22 soin propre 1/4 ; 23/24/25 cible 1/4 ; 26 cible 1/3.
3. Hors soin 182, le traitement partagé relie aussi dégâts et énergie ; ne pas exposer ces valeurs sans Lot 06.
4. EOS MP4 ne produit aucun nouvel impact ; les guards de génération rejettent les callbacks périmés.

## Lots 02 à 04 — dettes supprimées
- Lot 02 : manifeste/résolution centrale ; ZeroWin sans mutation globale.
- Lot 03 : sélection/session figée et identités de pouvoirs set-aware.
- Lot 04 : ZIP confiné/transactionnel, octets réels + taille/SHA, `content://` copié vers brouillon.

## Lot 05 — dettes supprimées
- Les sets utilisateur ne dépendent pas d'un chemin officiel homonyme : leur résolveur reste attaché à la révision installée.
- Promotions persistées séparément ; import seul ne rend jamais le set visible au joueur.
- Brouillon auto-contenu : source supprimée après clonage n'invalide pas le brouillon.
- Preview isolée : aucun engine/phase/KO/energy callback ; remplacement/close libère le player ; stale frame/EOS ignorés.
- SAF : picker/annulation/stale result, ingress worker et egress async couverts.
- Session test temporaire : aucune persistance, restauration au MENU, stale callbacks neutralisés, decoder failure borné.
- Atelier : 20 touches/diagnostic conservés, gros contrôles, création/reprise/modification/import/export/test/promotion.
- Gameplay v1 reste fermé : pas d'édition coûts/mécanismes/parameters/impacts/chrono/KO/EOS.
- CI : 152/152 tests verts.
- Run Android #85 `37515396288` SUCCESS sur `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17`.
- APK : 156521694 octets ; SHA-256 `fd08bc534da84fc8753cbc30bb7e8200eda2fcd3a3cbe0a6ea98147867673cc2`.

## Risque suivant
Lot 06 ne doit exposer aucun paramètre d'équilibrage sans validation explicite Fab + bornes approuvées + tests PV/énergie.

## Règle
CI verte != validation téléphone. Aucun bug ou correctif annoncé sans preuve fraîche adaptée.
