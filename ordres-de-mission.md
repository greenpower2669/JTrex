# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-05

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

### Lots 01 et 02 — TERMINÉS
Lot 01 : inventaire + contrat DATA-only v1.
Lot 02 : runtime/catalogue/manifeste canonique + packaging et résolution média centrale, sans sélection joueur.

Preuves Lot 02 :
- commit produit `017d611cf798d4713af8039ee6962d1fe6729fd2` ;
- runtime `tools/jtrex_sets_runtime.py`, catalogue officiel et manifeste `trex_vs_steg` à 41 assets vérifiés ;
- ZeroWin est une scène moteur normale, sans mutation globale de `SCENES` ;
- run intégration `37378554085` : 56/56 tests OK ;
- workflow Android exact : blob `c22bcf40038889318a3cab7c25d6c8c78dd87c49`, SHA-256 `3f4a83e9a0c35f7f361917fdbacfe6cadf3c41369519e0dcfc6a2a764bf00b13`, commit `ee8cf297830e1f40d984ab6b1706733eff22e5d7` ;
- preuve APK finale : run #80 `37379193862` GREEN ; artefact APK `11375685200` ; `JuneT-Rex-1.0.15-debug.apk` = 156461520 octets, SHA-256 `182e1b8f72f269a7e3f3f24895e37fe23a1b3ade9e77949d14500827c13c320c`.

### Prochain lot contractuel
Lot 03 : catalogue/menu joueur, sélection persistante du set, gel du set pendant un match et fallback canonique sûr. Aucun import ZIP, atelier admin ou paramètre d'équilibrage avant leurs lots dédiés. Aucun merge `main`, aucune Release sans ordre explicite de Fab.

## Baseline publiée précédente
- Build #78 / `37245309424` : CI verte ; validation téléphone complète non enregistrée.
- Dernière Release : `v1.0.15-main`.
