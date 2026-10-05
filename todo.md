# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-05

## Promotion main / archivage — terminé
- [x] Snapshot intégral des cinq anciennes mémoires sous `archive/memories/2026-10-04-pre-main-merge/`.
- [x] Fichiers vivants réorganisés et fortement allégés.
- [x] PR #1 fusionnée vers `main`.
- [x] Merge fonctionnel `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- [x] Release `v1.0.15-main` publiée.

## Build candidat actuel — terminé côté CI
- [x] Base fonctionnelle actuelle : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- [x] Build Android #78 (`37245309424`) vert.
- [x] APK candidat récupéré et vérifié : 156445730 octets.
- [x] SHA-256 : `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.

## Validation téléphone active
- [ ] Installer et démarrer l’APK du build #78.
- [ ] Deux nouveaux échanges d’orbes successifs : 10 s complets chacun.
- [ ] Retour d’un pouvoir : chrono restant conservé.
- [ ] Verdict/FIGHT : aucune pose d’orbe bloquée.
- [ ] KO -> nouveau round : ST = 0 et TR = 0.
- [ ] Plusieurs boucles vidéo plage sans effet gameplay à l’EOS.
- [ ] Finishings et pouvoirs jusqu’à EOS réel lorsque requis.

## Après validation téléphone seulement
- [ ] Nettoyer le temporaire devenu inutile.
- [ ] Consolider minimalement les mémoires si un nouveau fait devient canonique.
- [ ] Nouvelle Release uniquement sur ordre explicite de Fab.

## Canon protégé pendant les validations
- KO réel seul = victoire de round.
- Deux rounds gagnés = fin du match.
- Coûts pouvoirs ST 60/40/60 ; TR 60/60/80.
- Disponibilité stricte `energy > cost`.
- Wait canonique = vidéo plage uniquement.

## Maintenance repo non urgente
Les workflows historiques `apply-jt-orbs-presentation-002.yml` et `jt-ko-impl-temp.yml` existent encore. Ne pas les supprimer automatiquement.

## Références
- Dernière Release publiée : `v1.0.15-main`.
- Build candidat : #78 / `37245309424`.
- Base fonctionnelle testée : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- Archive de l’ancien TODO : `archive/memories/2026-10-04-pre-main-merge/todo.md`.
