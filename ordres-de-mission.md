# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-04

## Contrat permanent
1. Ne jamais recoder de mémoire : relire code, tests et preuves Git avant modification.
2. `ordres-de-mission.md` définit le contrat actif ; `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md` sont les mémoires vivantes spécialisées.
3. Les mémoires vivantes restent courtes. Chronologies, preuves anciennes, hypothèses dépassées et missions closes vont dans `archive/`.
4. Séparer faits vérifiés, retours téléphone, hypothèses et tâches restantes.
5. Ne pas modifier les règles canoniques historiques sans ordre explicite de Fab.
6. Avant toute annonce de succès : preuve fraîche par CI, test ou inspection Git adaptée.

## Canon gameplay protégé
- 3 orbes par camp.
- Nouvel échange d’orbes = 10 s complets.
- Retour d’un pouvoir = temps restant conservé.
- KO réel seul = victoire de round.
- Deux rounds gagnés = fin du match.
- Nouveau vrai round = énergie ST/TR remise à 0.
- Pouvoirs ST 60/40/60 ; TR 60/60/80 ; condition stricte `énergie > coût`.
- Wait canonique = `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` en boucle, EOS sans conséquence gameplay.

## JT-MEMORY-ARCHIVE-MAIN-001 — CLOSE
Autorisation explicite de Fab reçue pour réorganiser les mémoires, archiver l’historique, merger vers `main` et publier une Release.

### Exécution vérifiée
- Snapshot intégral des cinq mémoires pré-consolidation : `archive/memories/2026-10-04-pre-main-merge/`.
- Les blobs archivés sont identiques aux originaux du commit `5ac6962fac48f654075aacba286ddbbbf7749dbb`.
- Mémoires vivantes compactées et spécialisées.
- PR #1 fusionnée vers `main`.
- Merge fonctionnel : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Inspection média #24 : succès.
- Build Android #76 (`37203568079`) : succès complet.
- Release : `v1.0.15-main`, cible `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- APK : `JuneT-Rex-1.0.15-debug.apk`, 156791394 octets.
- SHA-256 APK : `2fbad1d19084fa7ad2c00ac81156ef0c5db0c933b679075df3ddf7fbb5f330b1`.
- Workflow temporaire de publication retiré après succès.

## Mission suivante
Aucune correction code ouverte par cette consolidation. La prochaine action utile est le test téléphone de `v1.0.15-main`, selon `todo.md`.

## Archive
Ancien contrat/chronologie complet : `archive/memories/2026-10-04-pre-main-merge/ordres-de-mission.md`.
