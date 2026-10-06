# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-06

## Contrat permanent
1. Ne jamais recoder de mémoire : relire code, tests et preuves Git avant modification.
2. `ordres-de-mission.md` définit le contrat actif ; `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md` sont les mémoires vivantes spécialisées.
3. Les mémoires vivantes restent courtes ; détails et preuves longues vont dans `docs/` ou `archive/`.
4. Ne pas modifier les règles canoniques historiques sans ordre explicite de Fab.
5. Avant toute annonce de succès : preuve fraîche adaptée.

## Canon gameplay protégé
- 3 orbes par camp ; nouvel échange = 10 s complets ; retour pouvoir = temps restant.
- KO réel seul = victoire de round ; deux rounds = match ; vrai nouveau round = énergie ST/TR à 0.
- Vie = 500000000 par camp.
- Coûts slots 1..6 = 60/40/60/60/60/80 ; activation stricte `énergie > coût`.
- Effets historiques au jalon moteur ; EOS média sans nouvel effet gameplay.

## JT-SETS-001 — ACTIF
Branche : `feature/dinosaur-sets-v1`, issue de `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
Design : `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`.

### Lots 01 à 03 — TERMINÉS
- Lot 01 : inventaire + contrat DATA-only v1.
- Lot 02 : runtime/catalogue/manifeste canonique + packaging et résolution média centrale.
- Lot 03 : catalogue joueur, sélection persistante au menu, fallback canonique sûr, set figé pendant le match et identités de pouvoirs résolues depuis le set de session.

Preuves Lot 03 :
- base `9efad3d0dfaf480aa46e715442d104357969abef` ;
- commit produit `dfad8fbc5ae4678fb5bd704ea38a858116966a5b` ;
- HEAD validation Android `c5330f29814430944500839aa3bcd29afbc3ff8b` ;
- TDD/suite complète : 77/77 tests verts ; deux sessions synthétiques successives et vieux EOS/callback A→B couverts ;
- run Android #83 `37417205571` : GREEN jusqu'au build et upload APK ;
- artefact APK `11391049002` ; `JuneT-Rex-1.0.15-debug.apk` = 156468471 octets, SHA-256 `612af2912050c392c63ec2054b03fc875b3a7a4c8f915c3a40d074cb077dec20`.

### Prochain lot contractuel
Lot 04 : stockage officiel/utilisateur/brouillon + import/export ZIP sûr et transactionnel. Aucun atelier 20 touches avant Lot 05 ; aucun paramètre d'équilibrage avant Lot 06. Aucun merge `main`, aucune Release ni AAB sans ordre explicite de Fab.

## Baseline publiée précédente
- Build #78 / `37245309424` : CI verte ; validation téléphone complète non enregistrée.
- Dernière Release : `v1.0.15-main`.
