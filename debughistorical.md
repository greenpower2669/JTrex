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

## Lot 02 — dette supprimée
- ZeroWin est une scène moteur normale ; chemins média résolus depuis le manifeste ; policies hors manifeste.
- Packaging vérifie catalogue, manifeste et 41 assets taille+SHA.

## Lot 03 — dette supprimée
- La sélection officielle est persistée hors match ; JSON/ID invalide => réparation vers `trex_vs_steg`.
- Le set est gelé pendant une session et ne peut pas changer avant le retour MENU.
- Un changement au menu stoppe/invalide l'ancien lecteur, la reprise et la génération ; vieux EOS/frame d'une session A ignorés après session B.
- Les six couples d'images ready/used, sons d'activation et fallbacks audio sont résolus depuis le set figé ; les règles de pouvoirs restent historiques.
- Non-régression : 77/77 tests verts.
- Run Android #83 `37417205571` GREEN sur `c5330f29814430944500839aa3bcd29afbc3ff8b`.
- APK : artefact `11391049002`, 156468471 octets, SHA-256 `612af2912050c392c63ec2054b03fc875b3a7a4c8f915c3a40d074cb077dec20`.

## Risques suivants
- Lot 04 : import transactionnel, confinement des chemins, limites taille/nombre, empreintes obligatoires, aucun exécutable, rollback complet si erreur.
- Lot 05 : ne jamais laisser un brouillon modifier une session officielle active.
- Lot 06 : aucun équilibrage ouvert sans validation Fab + tests PV/énergie.

## Règle
CI verte != validation téléphone. Aucun bug ou correctif annoncé sans preuve fraîche adaptée.
