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

### Lots 01 à 05 — TERMINÉS
- Lot 01 : inventaire + contrat DATA-only v1.
- Lot 02 : runtime/catalogue/manifeste canonique + résolution média centrale.
- Lot 03 : sélection joueur persistante + session figée + identités de pouvoirs set-aware.
- Lot 04 : stockage officiel/utilisateur/brouillon + ZIP sûr/transactionnel + ingress `content://`.
- Lot 05 : catalogue utilisateur promu, brouillons autonomes, atelier admin 20 touches, assistant par rôle, aperçu indépendant, SAF asynchrone, export, promotion explicite et `TESTER CE SET`.

Preuves Lot 05 :
- plan `docs/superpowers/plans/2026-10-06-jtrex-sets-lot05.md` ;
- HEAD produit `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17` ;
- run inspection `37515396279` : SUCCESS ;
- run Android #85 `37515396288`, job `112446897658` : SUCCESS ;
- 152/152 tests CI verts sur l'app générée ;
- APK artefact `11437986330` : 156521694 octets, SHA-256 `fd08bc534da84fc8753cbc30bb7e8200eda2fcd3a3cbe0a6ea98147867673cc2`.

### Prochain lot contractuel
Lot 06 : paramètres de pouvoirs. **Ne rien coder tant que Fab n'a pas validé explicitement la liste des champs éditables et leurs bornes.** Les mécanismes, coûts, impacts, chrono, KO et EOS restent moteur-owned par défaut.

Aucun merge `main`, aucune Release ni AAB sans ordre explicite de Fab.

## Baseline publiée précédente
- Build #78 / `37245309424` : CI verte ; validation téléphone complète non enregistrée.
- Dernière Release : `v1.0.15-main`.
