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
- Sélection officielle persistée hors match ; état invalide => réparation vers `trex_vs_steg`.
- Set gelé pendant la session ; changement au menu invalide lecteur/reprise/génération.
- Six identités de pouvoirs résolues depuis le set figé ; règles gameplay historiques conservées.
- Non-régression : 77/77 tests ; run Android #83 GREEN.

## Lot 04 — dette supprimée
- Import/export ne dépend plus de chemins externes après installation : une révision utilisateur est auto-contenue.
- Archive prévalidée avant écriture ; zip-slip, chemins Windows/absolus, doublons casefold, symlink, chiffrement, extra non référencé et exécutable refusés.
- Limites v1 centralisées ; total annoncé ET octets réellement extraits contrôlés.
- Taille/SHA de chaque asset vérifiés après extraction.
- Staging sur le même filesystem ; exception/collision avant renommage final laisse l'ancienne révision intacte et nettoie le staging.
- `content://` est copié vers brouillon avec limite réelle et nettoyage partiel ; jamais utilisé directement comme chemin CoreVideo.
- Non-régression : 106/106 tests verts après préparation canonique.
- Run Android #84 `37477862014` SUCCESS sur `d0a56cf364f88a677f22f986d04eac5bcbe33054`.
- APK : 156478186 octets, SHA-256 `759b574f49abd7f08e4607de6117fa856e005a39a0c0c72909432ac17509fedb`.

## Risques suivants
- Lot 05 : l'aperçu admin ne doit posséder aucun callback gameplay ; un brouillon ne doit jamais muter une session officielle active ; le mode TEST doit restaurer la sélection normale.
- Lot 06 : aucun équilibrage ouvert sans validation Fab + tests PV/énergie.

## Règle
CI verte != validation téléphone. Aucun bug ou correctif annoncé sans preuve fraîche adaptée.
