# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-04

## Contrat permanent
1. Ne jamais recoder de mémoire : relire code, tests et preuves Git avant toute modification.
2. `ordres-de-mission.md` définit le contrat actif ; `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md` servent de mémoires vivantes spécialisées.
3. Les mémoires vivantes restent courtes. Les chronologies, preuves anciennes, hypothèses dépassées et missions closes vont dans `archive/`.
4. Séparer explicitement faits vérifiés, retours téléphone, hypothèses et tâches restantes.
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
- Wait canonique = `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` en boucle, sans conséquence gameplay à l’EOS.

## Mission active — JT-MEMORY-ARCHIVE-MAIN-001
Autorisation explicite de Fab :
- réorganiser les mémoires vivantes ;
- archiver les éléments historiques/supersédés sans perte ;
- merger vers `main` ;
- publier une Release issue du `main` fusionné.

### Procédure
1. Snapshot intégral des cinq mémoires avant réduction.
2. Réécriture des cinq fichiers vivants selon leur rôle.
3. Vérification de l’état Git et du contenu archivé.
4. Merge avec `main` en conservant les deux historiques de branche.
5. Build Android depuis le `main` fusionné.
6. Vérification de l’APK et de son SHA-256.
7. Publication d’une Release traçable vers le `main` fusionné.
8. Mise à jour finale des mémoires avec les preuves de merge/build/release.

## Références avant merge
- Branche Android : `port/android-first-apk`.
- Candidat fonctionnel : `ed1842bae1176ffb08d76905b597a548c7ecf382`.
- Build #75 : succès.
- Release existante avant merge : `v1.0.15`.
- APK SHA-256 : `54f5490ccf346b3e80e3117b4cf020b24898ad89cb44e6a2bd6bf73051d99c11`.

## Archive
Ancien contrat/chronologie complet : `archive/memories/2026-10-04-pre-main-merge/ordres-de-mission.md`.
