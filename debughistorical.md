# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-04

## Rôle
Ce fichier ne garde que les incidents encore utiles au diagnostic courant et les dernières résolutions structurantes. L’historique intégral est archivé dans `archive/memories/2026-10-04-pre-main-merge/debughistorical.md`.

## Résolus et à ne pas rouvrir sans preuve
### Bootstrap Android / zlib
L’ancien crash Android où `zlib.cpython-312.so` échouait sur `PyExc_MemoryError` a été corrigé dans la chaîne native. Ne pas revenir aux anciens contournements sans reproduire le défaut sur un build récent.

### KO et rounds
- Les verdicts de jauges ne comptent pas comme victoire de round.
- Seul un KO réel incrémente le score de round.
- Deux rounds gagnés terminent le match.
- Préserver ce contrat lors de toute modification de phase.

### Orbes / chrono
Le correctif canonique de `JT-ORBS-PRESENTATION-002` prépare chaque véritable nouvel échange avec :
- `car2 = 10` ;
- arrêts gauche/droite effacés ;
- `colstop` effacé ;
- causes d’arrêt obsolètes retirées.

Le retour d’un pouvoir n’est pas un nouvel échange et ne doit pas réinitialiser `car2`.

### Énergie entre rounds
Un vrai nouveau round après KO remet `stamg` et `stamd` à 0.

### Média d’attente
Le wait canonique est `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4`. L’ancien `StegVsTrexvaetviensremolace*` ne doit plus être référencé par le runtime ni requis par le manifest.

## Preuves récentes
- Commit fonctionnel : `ed1842bae1176ffb08d76905b597a548c7ecf382`.
- Build Android #75 : succès.
- Inspection média plage : H.264 852x480, 24 fps, AAC 44.1 kHz, durée ~44.916667 s.
- SHA-256 vidéo plage : `71b1abe5498d7e9f5dfd61cccede099759c49ec0a82324e8dd76b8c054dccd9d`.
- Git blob vidéo plage : `908d0f2ba5ef9a9da4b1316ff28ec21e7bce04ee`.
- Release `v1.0.15` APK SHA-256 : `54f5490ccf346b3e80e3117b4cf020b24898ad89cb44e6a2bd6bf73051d99c11`.

## Vérifications téléphone à refaire si régression signalée
1. deux échanges d’orbes successifs : 10 s chacun ;
2. retour pouvoir : temps restant conservé ;
3. transition verdict/FIGHT : aucune saisie orbe bloquée ;
4. KO -> round suivant : énergie ST/TR = 0 ;
5. boucle plage : au moins plusieurs EOS sans saut de logique gameplay ;
6. finishing : lecture complète lorsque le canon exige un finishing.

## Règle de diagnostic
Avant de corriger : reproduire, identifier la phase, le média actif, `car2`, `stamg/stamd`, états stop et cause de transition. Ne jamais déduire un correctif uniquement d’une mémoire historique.
