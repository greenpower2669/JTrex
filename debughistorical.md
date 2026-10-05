# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-05

## Baseline JT-SETS-001
- Base : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Archive canonique SHA `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- Main préparé SHA `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.

## Faits structurants
1. `app/main.py` n'est pas versionné : repartir de l'archive prouvée + préparateur.
2. `deg[21..26]=181..186` sont des jalons de frame, pas des dégâts.
3. Effets bruts : 21 cible 1/4 ; 22 soin propre 1/4 ; 23/24/25 cible 1/4 ; 26 cible 1/3.
4. Hors soin 182, le traitement partagé relie aussi dégâts et énergie ; ne pas exposer ces valeurs sans Lot 06.
5. EOS MP4 ne produit aucun nouvel impact ; les guards de génération rejettent les callbacks périmés.

## Lot 02 — dette supprimée
- ZeroWin est une scène moteur normale liée au rôle `verdict_draw`; aucune mutation de `SCENES` via `__globals__`.
- Les chemins intros/combat/pouvoirs/finishings viennent du manifeste canonique ; les policies moteur restent hors manifeste.
- Le préparateur vérifie catalogue, manifeste et 41 assets avec taille+SHA.
- Run intégration `37378554085` : 56/56 OK.
- Workflow exact : commit `ee8cf297830e1f40d984ab6b1706733eff22e5d7`, blob `c22bcf40038889318a3cab7c25d6c8c78dd87c49`.
- APK final : run #80 `37379193862` GREEN ; artefact APK `11375685200` ; `JuneT-Rex-1.0.15-debug.apk` = 156461520 octets, SHA-256 `182e1b8f72f269a7e3f3f24895e37fe23a1b3ade9e77949d14500827c13c320c`.

## Risques suivants
- Lot 03 : figer le set au démarrage du match ; invalider proprement lecteurs/callbacks lors d'un futur changement de session.
- Lot 04 : import transactionnel, chemins confinés, tailles/SHA, aucun exécutable.
- Lot 06 : aucun équilibrage ouvert sans validation Fab + tests PV/énergie.

## Règle
Tests CI != validation téléphone. Aucun bug ou correctif annoncé sans preuve fraîche.
