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

### Lots 01 à 04 — TERMINÉS
- Lot 01 : inventaire + contrat DATA-only v1.
- Lot 02 : runtime/catalogue/manifeste canonique + packaging et résolution média centrale.
- Lot 03 : catalogue joueur, sélection persistante au menu, fallback canonique sûr, set figé pendant le match et identités de pouvoirs résolues depuis le set de session.
- Lot 04 : stockage officiel/utilisateur/brouillon, import/export ZIP auto-contenu sûr et transactionnel, contrôle taille/SHA et copie `content://` vers brouillon.

Preuves Lot 04 :
- plan `docs/superpowers/plans/2026-10-06-jtrex-sets-lot04.md` ;
- commit produit `156ee830155bc34c840a83666de20fca43fb72d8` ;
- HEAD validation Android `d0a56cf364f88a677f22f986d04eac5bcbe33054` ;
- préparation canonique + suite complète : 106/106 tests verts ;
- run Android #84 `37477862014`, job `112317924340` : SUCCESS jusqu'à upload APK ;
- artefact `11421465099` ; APK extrait `JuneT-Rex-1.0.15-debug.apk` = 156478186 octets, SHA-256 `759b574f49abd7f08e4607de6117fa856e005a39a0c0c72909432ac17509fedb`.

### Lot actif suivant
Lot 05 : atelier admin caché derrière les 20 touches existantes, assistant par rôle, aperçu indépendant sans callback gameplay et `TESTER CE SET` sur une révision de brouillon figée. Les paramètres de pouvoirs restent non éditables avant Lot 06. Aucun merge `main`, aucune Release ni AAB sans ordre explicite de Fab.

## Baseline publiée précédente
- Build #78 / `37245309424` : CI verte ; validation téléphone complète non enregistrée.
- Dernière Release : `v1.0.15-main`.
