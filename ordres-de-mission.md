# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-05

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
- Snapshot intégral : `archive/memories/2026-10-04-pre-main-merge/`.
- PR #1 fusionnée vers `main`.
- Merge fonctionnel historique : `a2efd10a8f508c301156879ac1ab534f1a9d06ca`.
- Release publiée : `v1.0.15-main`.

## JT-ASSETS-LIGHT-001 — VALIDATION TÉLÉPHONE EN COURS
La phase de préparation et de remplacement est terminée. Ne pas rouvrir un chantier code ou gameplay autour de cette mission sans nouveau besoin explicite de Fab.

### État vérifié
- Branche canonique : `main`.
- Base fonctionnelle actuellement testée : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- Build Android #78 (`37245309424`) : succès complet.
- APK candidat : `JuneT-Rex-1.0.15-debug.apk`.
- Taille : 156445730 octets.
- SHA-256 : `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.
- Dernière Release publiée : `v1.0.15-main` ; aucune nouvelle Release n’est considérée publiée à ce stade.

### Ordre actif
1. Fab teste l’APK du build #78 sur téléphone.
2. Pendant ce test : aucun changement gameplay, architecture ou nettoyage massif.
3. Si un défaut est observé : reproduire, mesurer et relire les fichiers Git concernés avant correction.
4. Si le test est validé : nettoyer le temporaire devenu inutile et consolider les mémoires au strict nécessaire.
5. Merge supplémentaire ou nouvelle Release uniquement sur ordre explicite de Fab.

### VERROU ACTIF
**ATTENDRE LE RETOUR TÉLÉPHONE DE FAB AVANT LA SUITE.**

## Archive
Ancien contrat/chronologie complet : `archive/memories/2026-10-04-pre-main-merge/ordres-de-mission.md`.
