# JTREX JT-SETS-001 Lot 01 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reproduire le `app/main.py` canonique, établir un inventaire prouvé des identités/médias/images/sons/effets des six pouvoirs, puis figer le contrat de format v1 sans modifier le moteur de jeu.

**Architecture:** Lot 01 est un lot d'audit et de contrat, pas un lot de runtime. La source d'autorité reste `JuneTrex.zip` vérifié puis transformé par `tools/prepare_android.py`; les documents produits décrivent ce qui existe réellement et séparent strictement ressource personnalisable, mécanisme moteur et valeur non éditable.

**Tech Stack:** Python 3, Kivy source historique généré, `tools/prepare_android.py`, unittest/pytest existants, shell/Git, SHA-256.

**Spec:** `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`

## Global Constraints

- Branche de travail : `feature/dinosaur-sets-v1`, base de mission `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- `app/main.py` est généré depuis `JuneTrex.zip`; ne jamais l'utiliser comme source versionnée ni le committer.
- Archive canonique : taille `327992765`, SHA-256 `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- Source historique `main.py` attendue par le préparateur : SHA-256 `3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231`.
- Conserver le moteur unique, le gameplay canonique, les phases/KO/EOS/chrono et les coûts `60/40/60/60/60/80` avec activation stricte `énergie > coût`.
- Aucun nouveau runtime de set, manifeste actif, menu, import/export ou atelier n'est implémenté dans ce lot.
- Ne pas interpréter `deg`, `longanim1`, un état `indexa`, une frame ou une durée vidéo comme paramètre d'équilibrage sans preuve du code généré.
- Aucun merge `main`, aucune Release et aucun AAB.
- Synchroniser `ordres-de-mission.md`, `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md` avec les faits utiles seulement.

## Review Focus

1. Archive ou `main.py` non canonique : le lot doit s'arrêter si taille/SHA ne correspondent pas, sans produire d'inventaire présenté comme fiable. Couvert Task 1.
2. Faux paramètre d'équilibrage (`deg`, frame, longueur, état) : chaque candidat doit avoir une preuve lecture/écriture et une unité/semantique explicite, sinon rester non éditable. Couvert Task 3.
3. Mauvais rattachement gauche/droite ou slot : les six slots doivent être reliés explicitement à camp, état 21..26, coût, média et identité visuelle. Couvert Task 2.
4. Confusion événement/dégâts : l'inventaire doit distinguer compteur/indice de l'effet réellement appliqué et sa cible. Couvert Task 3.
5. Jalon d'impact déduit de la durée vidéo : les jalons historiques doivent être relevés dans le moteur, jamais recalculés depuis la durée du MP4. Couvert Task 3.

---

### Task 1: Reproduire et figer la baseline générée

**Files:**
- Read: `tools/prepare_android.py`
- Read: `.github/workflows/android.yml`
- Generate locally only: `JuneTrex.zip`, `app/main.py`
- Create: `docs/jt-sets-001/lot01-inventory.md`

**Interfaces:**
- Consumes: archive historique de la Release `JTrex`, `prepare_android.py` actuel.
- Produces: section `Baseline reproductible` du document d'inventaire avec commit, archive SHA/taille, source SHA attendue, SHA du `app/main.py` généré, commande de génération et résultat des tests de baseline.

- [ ] **Step 1: Vérifier que la branche est toujours basée sur le plan approuvé**

Run: `git status --short && git rev-parse HEAD && git merge-base --is-ancestor ce858fe57b395c2a52967dc0e8acdd92ff6aa81e HEAD`

Expected: arbre propre avant exécution, HEAD sur `feature/dinosaur-sets-v1`, code retour 0 pour l'ascendance.

- [ ] **Step 2: Télécharger l'archive historique sans utiliser un ZIP local non prouvé**

Run: `curl --fail --location --retry 3 -o JuneTrex.zip https://github.com/greenpower2669/JTrex/releases/download/JTrex/JuneTrex.zip`

Expected: fichier non vide.

- [ ] **Step 3: Vérifier taille et SHA-256 avant extraction**

Run: `test "$(stat -c%s JuneTrex.zip)" = 327992765 && echo 'f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647  JuneTrex.zip' | sha256sum -c -`

Expected: `JuneTrex.zip: OK`; sinon STOP Lot 01.

- [ ] **Step 4: Générer le vrai `app/main.py` par la chaîne canonique**

Run: `rm -rf app && python3 tools/prepare_android.py --archive JuneTrex.zip --output app --spec buildozer.spec 2>&1 | tee diagnostics/jt-sets-001-lot01-prepare.log`

Expected: préparation terminée sans `RuntimeError`; le préparateur vérifie lui-même le SHA du main historique avant adaptation.

- [ ] **Step 5: Enregistrer uniquement les preuves reproductibles, pas le `app/` généré**

Create `docs/jt-sets-001/lot01-inventory.md` avec une section `Baseline reproductible` contenant : branche/HEAD, archive taille+SHA, `MAIN_SHA256`, SHA-256 du `app/main.py` généré, commandes utilisées, et mention explicite `app/ non versionné`.

- [ ] **Step 6: Lancer la baseline de tests avant tout inventaire**

Run: `python3 -m unittest discover -s tests -v`

Expected: suite existante PASS. Toute régression préexistante est consignée et le lot s'arrête avant de modifier un contrat.

- [ ] **Step 7: Commit de preuve baseline**

Commit files: `docs/jt-sets-001/lot01-inventory.md` et, seulement si utile et compact, `diagnostics/jt-sets-001-lot01-prepare.log`; ne jamais ajouter `JuneTrex.zip` ni `app/`.

Commit message: `docs: record JT-SETS-001 generated baseline`

---

### Task 2: Inventorier identités, médias, images et six slots

**Files:**
- Read generated: `app/main.py`
- Read: `tools/jtrex_media_runtime.py`
- Read: `tools/prepare_android.py`
- Modify: `docs/jt-sets-001/lot01-inventory.md`

**Interfaces:**
- Consumes: baseline générée Task 1.
- Produces: tables `Identités`, `Rôles média`, `Pouvoirs slots 1..6`, `Images/variantes`, `Audio/replis` avec preuves de source.

- [ ] **Step 1: Extraire les catalogues historiques réels du main généré**

Run a read-only Python/grep probe over `app/main.py` for `namea`, `longanim1`, `genrea`, `sona`, `affbt`, `b1..b6`, `b1s..b6s`, states `21..26`, and all `.source` assignments touching power widgets.

Expected: six slots distincts et catalogues localisés avec numéros de lignes générés.

- [ ] **Step 2: Relever le mapping moteur/media actuel**

Record from `jtrex_media_runtime.py` the logical roles and files for intros, wait/orbs, red-blue, yellow, left/right/draw verdicts, six power scenes and two finishings; record `play_to_end`/loop policy as engine-owned, not manifest-editable.

- [ ] **Step 3: Construire la matrice des six pouvoirs**

For each slot 1..6 record exactly: camp, state 21..26, canonical cost, historical/internal name if proven, displayed label if proven, video role/path, icon source(s), pressed/rest/available variants actually used, and audio fallback if present.

- [ ] **Step 4: Vérifier le rattachement droite/gauche**

Run a probe asserting slot→state mapping `{1:21,2:22,3:23,4:24,5:25,6:26}` and compare the right-side visual correction in `prepare_android.py` (`slot 4=TRFS`, `slot 6=TRMA`) against the generated `affbt` assignments.

Expected: no slot ambiguity; any discrepancy is a blocker, not silently normalized in the document.

- [ ] **Step 5: Vérifier que les médias canoniques existants sont tous couverts**

Run existing `tests/test_orb_media_manifest.py` and `tests/test_media_asset_size_guards.py`.

Expected: PASS; every media role recorded in the inventory points to a repository asset guarded by current preparation/tests or is explicitly identified as historical fallback.

- [ ] **Step 6: Commit de l'inventaire identité/média**

Commit message: `docs: inventory JTrex set identities and media`

---

### Task 3: Inventorier les six mécanismes et les vrais paramètres

**Files:**
- Read generated: `app/main.py`
- Read: `tools/jtrex_phase_runtime.py`
- Read: `tools/prepare_android.py`
- Modify: `docs/jt-sets-001/lot01-inventory.md`

**Interfaces:**
- Consumes: matrice six slots Task 2.
- Produces: une fiche d'effet par slot et une table `Candidats de personnalisation` / `Non-paramètres`, utilisables par le contrat v1.

- [ ] **Step 1: Localiser les branches d'effet 21..26 dans le vrai main généré**

For each state, capture the containing method/function, conditions d'entrée, variables lues/écrites, et le moment historique de l'effet par rapport à `anim1`, `longanim1`, transitions et callbacks.

- [ ] **Step 2: Décrire chaque effet sans renommer sa sémantique**

For each slot record: cible, base de calcul, opération (dégâts/soin/réduction/autre), valeur/coefficient canonique, plafonnement, variables de dégâts cumulés, interaction énergie, et condition d'unicité.

- [ ] **Step 3: Classer chaque valeur candidate**

Every candidate row must include: source location, read/write semantics, exact unit/base, canonical value, consequence of change, and regression test that would preserve canonical behavior.

If one of those six columns cannot be proven, mark `NON ÉDITABLE v1`.

- [ ] **Step 4: Établir la liste négative obligatoire**

Explicitly document why `deg` when used as event/index, `longanim1`, `anim1`, `indexa`, frame numbers, video duration and EOS are not balancing parameters unless a separate proven numeric effect exists.

- [ ] **Step 5: Vérifier les jalons contre les runtimes de phase/media**

Cross-check that `jtrex_phase_runtime.py` and media EOS handling do not create a second application of damage/heal/energy. Record historical impact point separately from presentation completion.

- [ ] **Step 6: Exécuter les tests gameplay ciblés**

Run: `python3 -m unittest tests.test_phase_integration tests.test_round_ko_contract tests.test_round_model tests.test_orb_presentation -v`

Expected: PASS; this proves the audit did not require altering current phase/KO/orb behavior.

- [ ] **Step 7: Commit de l'inventaire mécanismes/paramètres**

Commit message: `docs: inventory JTrex power mechanisms`

---

### Task 4: Figer le contrat de format v1 à partir des preuves

**Files:**
- Create: `docs/jt-sets-001/format-v1-contract.md`
- Read: `docs/jt-sets-001/lot01-inventory.md`
- Read: `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`

**Interfaces:**
- Consumes: inventaire prouvé Tasks 1-3.
- Produces: contrat de format v1 utilisable directement par le plan du Lot 02.

- [ ] **Step 1: Définir les champs obligatoires et leur autorité**

Document exactly: `format_version`, `set_id`, `revision`, `display_name`, `engine_contract`, `dinosaurs.left/right`, media roles, six power entries, and asset metadata `{id,path,type,size,sha256}`.

- [ ] **Step 2: Définir la frontière engine-owned / set-owned**

Set-owned v1: identités, ressources, labels/images/médias des slots et seulement les paramètres explicitement prouvés puis autorisés.

Engine-owned: states/transitions, loop/play-to-end policy, locks, EOS semantics, impact timing, round/KO rules, costs v1, strict energy condition.

- [ ] **Step 3: Écrire le profil canonique v1**

Map every current logical role and six slots to the canonical values from the inventory without moving/renaming assets. Do not yet create an installed `manifest.json`; this section is the source contract for Lot 02.

- [ ] **Step 4: Marquer les paramètres de pouvoirs comme fermés tant que Fab ne les a pas validés**

The contract may list proven candidates and proposed bounds, but must state that editable balancing fields remain disabled until Fab approves the list/bounds in Lot 06.

- [ ] **Step 5: Faire un contrôle de complétude**

Verify the contract has exactly two dinosaur sides, nine required combat/presentation media roles (`orbs_background`, red/blue, yellow, draw, left, right, finishing left/right plus intros collection), six power entries, and explicit asset hash/size metadata requirements.

Expected: no role from the design spec is absent and no engine rule is exposed as pack data.

- [ ] **Step 6: Commit du contrat v1**

Commit message: `docs: define JTrex set format v1 contract`

---

### Task 5: Vérification Lot 01 et synchronisation des mémoires

**Files:**
- Modify: `ordres-de-mission.md`
- Modify: `brain.md`
- Modify: `brainmap.md`
- Modify: `debughistorical.md`
- Modify: `todo.md`
- Read: all Lot 01 documents and existing tests

**Interfaces:**
- Consumes: Tasks 1-4 completed.
- Produces: Lot 01 closed with evidence and a single explicit next action: plan Lot 02.

- [ ] **Step 1: Vérifier qu'aucun code produit ou asset n'a changé pendant Lot 01**

Run: `git diff --exit-code ce858fe57b395c2a52967dc0e8acdd92ff6aa81e -- tools assets buildozer.spec .github`

Expected: no diff attributable to Lot 01 product implementation. Documentation/memory changes are allowed.

- [ ] **Step 2: Relancer toute la suite de tests**

Run: `python3 -m unittest discover -s tests -v`

Expected: PASS.

- [ ] **Step 3: Vérifier les documents contre les cinq Review Focus**

Manual review with explicit yes/no evidence for archive identity, six-slot side mapping, event-vs-damage distinction, non-parameters, and impact timing independent from video duration.

Expected: five YES; otherwise Lot 01 remains open.

- [ ] **Step 4: Synchroniser les cinq mémoires vivantes**

Record only: baseline generated SHA, links to inventory/contract, proven six-slot mapping, which fields remain closed, test result, blockers if any, and `Lot 02 plan` as next action. Archive no new chronology in living memories.

- [ ] **Step 5: Commit de clôture Lot 01**

Commit message: `docs: close JT-SETS-001 lot 01`

- [ ] **Step 6: Retour à Fab**

Report branch, HEAD, documents, exact tests run/results, facts proven, candidates still requiring Fab validation, and explicitly state that no runtime set implementation has started.
