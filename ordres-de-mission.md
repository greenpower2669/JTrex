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

## JT-SETS-001 — ACTIF — FEU VERT FAB 2026-10-05
Objectif : sets complets de confrontations de dinosaures DATA + MEDIA autour d’un seul moteur de gameplay.

Branche dédiée : `feature/dinosaur-sets-v1` issue du `main` vérifié `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.

Design approuvé : `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`.
Plan Lot 01 prêt : `docs/superpowers/plans/2026-10-05-jtrex-sets-lot01.md`.
Statut : plan en attente de validation Fab avant exécution. Exécution prévue native par Sol, sans sous-agent imposé.

Ordre des lots :
1. inventaire du vrai `app/main.py` généré + contrat de format v1 ;
2. manifeste canonique + résolution centrale ;
3. catalogue/menu joueur + sélection figée ;
4. stockage/import/export sûr ;
5. atelier admin 20 touches + aperçus + test brouillon ;
6. paramètres des pouvoirs uniquement après validation Fab des champs/bornes.

Règles :
- aucun `main.py` par set ;
- aucun Python/KV/script/code provenant d’un pack ;
- le moteur garde phases, KO, rounds, EOS, verrouillages, jalons d’impact et coûts canoniques ;
- le set canonique doit rester strictement équivalent ;
- aucun merge `main`, aucune Release sans ordre explicite de Fab.

Le précédent verrou « attendre le retour téléphone du build #78 » est levé uniquement pour démarrer JT-SETS-001 par ordre explicite de Fab. Le build #78 reste CI-vert mais ne doit pas être présenté rétroactivement comme totalement validé téléphone.

## Baseline précédente
- Base fonctionnelle : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- Build #78 / `37245309424` : CI verte.
- APK candidat : `JuneT-Rex-1.0.15-debug.apk`, SHA-256 `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.
- Dernière Release publiée : `v1.0.15-main`.
- Validation téléphone complète non enregistrée dans les mémoires au moment du démarrage JT-SETS-001.

## Archive
Ancien contrat/chronologie complet : `archive/memories/2026-10-04-pre-main-merge/ordres-de-mission.md`.
