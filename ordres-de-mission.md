# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-05

## Contrat permanent
1. Ne jamais recoder de mémoire : relire code, tests et preuves Git avant modification.
2. `ordres-de-mission.md` définit le contrat actif ; `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md` sont les mémoires vivantes spécialisées.
3. Les mémoires vivantes restent courtes ; détails et preuves longues vont dans `docs/` ou `archive/`.
4. Ne pas modifier les règles canoniques historiques sans ordre explicite de Fab.
5. Avant toute annonce de succès : preuve fraîche adaptée.

## Canon gameplay protégé
- 3 orbes par camp ; nouvel échange = 10 s complets.
- Retour pouvoir = temps restant.
- KO réel seul = victoire de round ; deux rounds = match.
- Nouveau vrai round = énergie ST/TR remise à 0.
- Vie = 500000000 par camp.
- Coûts slots 1..6 = 60/40/60/60/60/80 ; activation stricte `énergie > coût`.
- Effets historiques au jalon moteur ; EOS média sans nouvel effet gameplay.

## JT-SETS-001 — ACTIF
Branche : `feature/dinosaur-sets-v1`, issue de `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.

Design : `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`.

### Lot 01 — TERMINÉ CÔTÉ CODE/AUDIT
Livrables :
- `docs/jt-sets-001/lot01-inventory.md` ;
- `docs/jt-sets-001/format-v1-contract.md` ;
- `docs/jt-sets-001/lot01-verification.md`.

Preuve fraîche : run diagnostic `37339853652` GREEN ; archive canonique et main généré vérifiés ; 38 tests / 38 OK. Le workflow diagnostic temporaire a été supprimé. Comparaison finale : aucun changement `tools/`, `assets/`, `.github/` ou `buildozer.spec` par rapport à la base.

Constats canoniques utiles :
- gauche = ST, slots 1..3 / états 21..23 ; droite = TR, slots 4..6 / états 24..26 ;
- `deg[21..26]=181..186` = jalons d’animation, pas dégâts ;
- effets bruts : STSF 1/4 cible, STLS soin 1/4 propre, STTA 1/4 cible, TRFS 1/4 cible, TRPH 1/4 cible, TRMA 1/3 cible ;
- dégâts influencent aussi l’énergie via le traitement partagé ;
- durée MP4/EOS ne déplace jamais le jalon d’impact ;
- paramètres d’équilibrage fermés dans v1 initial (`parameters:{}`) jusqu’à validation Fab au Lot 06.

### Prochain lot contractuel
Lot 02 : manifeste canonique + résolution centrale + équivalence du set actuel ; supprimer la mutation globale ZeroWin. Aucun merge `main`, aucune Release sans ordre explicite de Fab.

## Baseline publiée précédente
- Build #78 / `37245309424` : CI verte ; validation téléphone complète non enregistrée.
- Dernière Release : `v1.0.15-main`.
