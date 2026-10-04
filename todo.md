# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-04

## Priorité immédiate
- [ ] Finaliser la consolidation des mémoires vivantes et conserver le snapshot intégral sous `archive/memories/2026-10-04-pre-main-merge/`.
- [ ] Merger la branche Android vers `main` avec historique préservé.
- [ ] Vérifier le build Android déclenché par le `main` fusionné.
- [ ] Publier une Release du `main` fusionné avec un APK dont le SHA-256 est vérifié.

## Validation téléphone post-merge
- [ ] Installer l’APK issu du `main` fusionné.
- [ ] Vérifier deux nouveaux échanges d’orbes successifs : 10 s complets chacun.
- [ ] Vérifier retour d’un pouvoir : chrono restant conservé.
- [ ] Vérifier qu’aucune transition verdict/FIGHT ne bloque la pose des orbes.
- [ ] Vérifier KO -> nouveau round : ST = 0 et TR = 0.
- [ ] Vérifier plusieurs boucles de la vidéo plage sans effet gameplay à l’EOS.
- [ ] Vérifier finishings et pouvoirs jusqu’à EOS réel.

## Canon à ne pas modifier pendant ces validations
- KO réel seul = victoire de round.
- Deux rounds gagnés = fin du match.
- Coûts pouvoirs ST 60/40/60 ; TR 60/60/80.
- Disponibilité stricte `energy > cost`.
- Wait canonique = vidéo plage uniquement.

## Maintenance repo à traiter seulement si elle devient utile
Les workflows temporaires anciens `apply-jt-orbs-presentation-002.yml` et `jt-ko-impl-temp.yml` existent encore. Ne pas les supprimer automatiquement sans vérifier qu’aucune procédure active ne les utilise.

## Terminé récemment
- [x] Correctif KO canonique.
- [x] Correctif nouveau chrono d’orbes à 10 s.
- [x] Préservation du chrono au retour d’un pouvoir.
- [x] Reset énergie à 0 au vrai nouveau round.
- [x] Remplacement du wait historique par la boucle plage.
- [x] Build Android #75 vert.
- [x] Release `v1.0.15` publiée depuis le candidat fonctionnel `ed1842b...`.

## Archive
Ancien TODO complet : `archive/memories/2026-10-04-pre-main-merge/todo.md`.
