# JTREX JT-SETS-001 Lot 02 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Faire du manifeste canonique la source unique des ressources de set utilisées par le runtime média et le packaging, sans changer le gameplay ni les politiques de scène.

**Architecture:** Ajouter un module pur Python `jtrex_sets_runtime.py` qui charge/valide le catalogue et le manifeste puis expose une sélection immuable en pratique avec résolution asset-id -> chemin logique. `jtrex_media_runtime.py` conserve les états et policies dans des `SCENE_SPECS` moteur-owned, mais obtient chaque fichier depuis la sélection. `prepare_android.py` copie/valide le runtime sets et les JSON, puis dérive les ressources de set depuis le manifeste au lieu d’un second catalogue manuel.

**Tech Stack:** Python 3.12, JSON, pathlib, Kivy `resource_find` fourni par le runtime média, unittest/harness existant, GitHub Actions Android existant.

**Spec:** `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`

**Inputs:**
- `docs/jt-sets-001/lot01-inventory.md`
- `docs/jt-sets-001/format-v1-contract.md`
- `docs/jt-sets-001/lot01-verification.md`

## Global Constraints

- Branche : `feature/dinosaur-sets-v1` ; ne jamais merger `main` ni publier de Release sans Fab.
- Le set canonique doit garder les mêmes états, policies, médias, coûts, effets, chrono, KO et EOS.
- `parameters` reste `{}` ; aucune extraction de formule d’équilibrage dans le manifeste.
- `SCENE_SPECS` peut mapper état -> rôle logique, mais `loop`, `play_to_end`, états, ZeroWin et règles EOS restent engine-owned.
- Aucun script/Python/KV ne peut provenir d’un manifeste.
- Pas de menu, persistance de sélection, import/export ni atelier dans ce lot.
- Pas de déplacement massif des assets ; le provider officiel utilise la racine applicative comme racine de résolution.
- Les images/audio de pouvoir sont validés par le manifeste/packaging dans ce lot, mais le main historique continue de les consommer comme avant ; la bascule dynamique de ces éléments lors d’un changement de set appartient au Lot 03.
- `buildozer.spec` doit inclure `json` afin d’embarquer catalogue/manifeste.
- Un seul build Android complet au jalon final du lot ; TDD local/rapide avant push produit lorsque possible.

## Review Focus

1. **Manifest valide mais asset-id absent :** le chargement doit échouer avec `SetContractError`, jamais retomber silencieusement sur un média d’un autre set. Task 1.
2. **Path traversal / URL dans asset.path :** même pour les sets officiels, le validateur doit refuser absolu, `..`, backslash et schéma URI. Task 1.
3. **ZeroWin global :** construire plusieurs contrôleurs/résolveurs ne doit plus modifier un dictionnaire global partagé dans `jtrex_phase_runtime`. Task 3.
4. **Policy média déplacée dans le manifeste :** aucune clé `loop`, `play_to_end`, `states` ou jalon ne doit être acceptée/nécessaire dans les données du set. Task 1/3.
5. **Source de ressources contradictoire :** le packaging et les tests de tailles/SHA doivent lire le même manifeste canonique, pas une copie manuelle `MEDIA_ASSETS`. Task 2.

---

### Task 1: Contrat runtime + catalogue/manifeste canonique

**Files:**
- Create: `tools/jtrex_sets_runtime.py`
- Create: `assets/sets/catalog.json`
- Create: `assets/sets/trex_vs_steg/manifest.json`
- Create: `tests/test_sets_runtime.py`

**Interfaces:**
- Produces `SetContractError(ValueError)`.
- Produces `load_official_set(resolve_path, set_id="trex_vs_steg") -> JTSetSelection`.
- Produces `JTSetSelection.set_id: str`.
- Produces `JTSetSelection.media_path(role: str) -> str`.
- Produces `JTSetSelection.intro_paths() -> tuple[str, ...]`.
- Produces `JTSetSelection.power(power_key: str) -> dict` returning a defensive copy.
- Produces `JTSetSelection.power_media_path(power_key: str) -> str`.
- Produces `JTSetSelection.asset_path(asset_id: str) -> str`.
- Produces `JTSetSelection.assets() -> tuple[dict, ...]` defensive copies for packaging validation.

- [ ] **Step 1: Write failing contract tests**

Tests must assert:
- canonical catalog loads `trex_vs_steg`;
- format_version=1 and engine_contract=`jtrex-combat-v1`;
- exactly left/right + nine media groups/roles + six power entries;
- canonical `orbs_background` resolves to `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4`;
- `left_1` resolves STSF MP4 and `right_3` resolves TRMA MP4;
- all six `parameters == {}`;
- missing referenced asset-id raises `SetContractError`;
- unknown required power/media role raises `SetContractError`;
- absolute path, `..`, backslash and `https://` path each raise `SetContractError`;
- manifest containing gameplay policy fields such as `loop`, `play_to_end` or `states` inside `media`/power data is rejected as unknown schema data.

- [ ] **Step 2: Run the tests and verify RED**

Run: `python3 -m unittest tests.test_sets_runtime -v`
Expected: FAIL because `jtrex_sets_runtime` / canonical JSON do not exist.

- [ ] **Step 3: Implement the minimal pure-Python runtime**

`load_official_set(resolve_path, set_id)` uses only JSON/path validation; no Kivy imports. `resolve_path(relative_path)` is supplied by the caller and returns a filesystem path/string or `None`.

Validation must be closed for the structures defined by `format-v1-contract.md`; asset metadata validates id uniqueness, path confinement, type enum, nonnegative size and lowercase 64-char SHA-256.

- [ ] **Step 4: Add canonical catalog and manifest from Lot 01 values**

Catalog membership is the only source of `official` status. Manifest contains all current set-specific MP4, power ready/used images and activation/fallback audio with exact sizes/SHA from the inventory. `set_id` does not determine side order: left=`st`, right=`tr`.

- [ ] **Step 5: Run Task 1 tests GREEN**

Run: `python3 -m unittest tests.test_sets_runtime -v`
Expected: PASS.

---

### Task 2: Packaging dérivé du manifeste

**Files:**
- Modify: `tools/prepare_android.py`
- Modify: `buildozer.spec`
- Modify: `tests/test_media_asset_size_guards.py`
- Modify: `tests/test_orb_media_manifest.py`
- Create: `tests/test_sets_packaging.py`

**Interfaces:**
- Consumes `load_official_set` and `JTSetSelection.assets()`.
- Keeps app-owned icon validation separate from set-owned assets.
- Copies `tools/jtrex_sets_runtime.py` to `app/jtrex_sets_runtime.py`.
- Copies `assets/sets/catalog.json` and `assets/sets/trex_vs_steg/manifest.json` into the prepared app.

- [ ] **Step 1: Write failing packaging tests**

Assert:
- `json` is present in `source.include_exts`;
- prepare code no longer defines a manual set-media `MEDIA_ASSETS` dictionary;
- canonical manifest is the source used to verify size+SHA for set assets;
- repo-backed `assets/...` resources are copied to stage;
- archive-backed root assets (`stsf*.png`, `sth*.png`, power wavs) are validated in stage without recopy from another set;
- set runtime + catalog + manifest are required in prepared app;
- report includes canonical `set_id`, manifest SHA and set asset count.

- [ ] **Step 2: Run Task 2 tests RED**

Run: `python3 -m unittest tests.test_sets_packaging tests.test_media_asset_size_guards tests.test_orb_media_manifest -v`
Expected: FAIL on old `MEDIA_ASSETS`/missing JSON packaging.

- [ ] **Step 3: Refactor preparation minimally**

Keep `APP_ASSETS` only for application-owned resources such as `assets/icon/JtrexIcon.png`. Load canonical selection from repo paths. For every manifest asset:
- if path starts `assets/`, source is repository/app media root and is copied into stage;
- otherwise it must already exist in stage from verified `JuneTrex.zip` extraction;
- in both cases compare exact size and SHA from manifest after bytes are in stage.

Do not change gameplay adaptation code.

- [ ] **Step 4: Copy/compile set runtime and JSON resources**

Require `jtrex_sets_runtime.py`, compile it, copy canonical catalog/manifest, and extend `android-preparation.json` with `canonical_set_id`, `canonical_manifest_sha256`, `canonical_set_asset_count`.

- [ ] **Step 5: Run packaging tests GREEN**

Run the Task 2 command again. Expected: PASS.

---

### Task 3: Runtime média résolu par rôles + ZeroWin sans mutation globale

**Files:**
- Modify: `tools/jtrex_media_runtime.py`
- Modify: `tools/jtrex_phase_runtime.py`
- Modify: `tests/runtime_harness.py` only if needed to expose real resolver path cleanly
- Create: `tests/test_sets_media_resolution.py`
- Modify: existing phase/media tests only where assertions must move from hardcoded runtime filenames to canonical manifest resolution

**Interfaces:**
- `JTMediaController` owns one `JTSetSelection` created during controller initialization.
- Engine-owned `SCENE_SPECS` maps scene keys to states + policy + either `media_role` or `power_key`.
- `JTMediaController._scene_config(key) -> dict` returns a fresh config including resolved logical `file` but never mutates `SCENE_SPECS`.
- `zero-win` is a normal engine scene spec for `JTPhaseController.ZERO_WIN_STATE` / role `verdict_draw`.

- [ ] **Step 1: Write failing resolver integration tests**

Assert:
- controller intro choices come from `selection.intro_paths()`;
- states 1/2-4/5-7/8/9/10/11/21-26 resolve to exactly the same canonical paths as before;
- state `-7` resolves `verdict_draw` without phase runtime modifying media globals;
- two controllers created successively keep independent selection objects and identical engine-owned scene specs;
- `SCENE_SPECS` contains policies but no canonical file paths;
- stale generation callback protection tests continue to pass.

- [ ] **Step 2: Run integration tests RED**

Run: `python3 -m unittest tests.test_sets_media_resolution -v`
Expected: FAIL while runtime still uses `INTRO_FILES`/`SCENES[file]` and phase mutates global scenes.

- [ ] **Step 3: Replace file catalog with engine scene specs**

Keep scene keys and state families stable. Move only `file` lookup to the set selection. All calls that previously read `SCENES[key]` use `_scene_config(key)` or the engine spec as appropriate.

- [ ] **Step 4: Remove `_install_zero_win_scene` mutation**

Delete the initialization call and mutation helper from phase runtime. Gauge hooks keep using `_key_for_state(-7)` supplied by the media runtime scene specs.

- [ ] **Step 5: Run Task 3 tests + canonical phase regressions GREEN**

Run:
`python3 -m unittest tests.test_sets_media_resolution tests.test_phase_integration tests.test_round_ko_contract tests.test_round_model tests.test_orb_presentation -v`
Expected: PASS.

---

### Task 4: CI/static checks + full canonical preparation

**Files:**
- Modify: `.github/workflows/android.yml`
- Modify/add tests only as required by the new source of truth

**Interfaces:**
- CI validates canonical filenames/roles from manifest rather than requiring them as literals inside `jtrex_media_runtime.py`.
- Existing gameplay assertions remain intact.

- [ ] **Step 1: Update stale static assertions**

Remove checks that demand every media filename in runtime source or `MEDIA_ASSETS` literal. Replace with JSON/runtime checks that verify the canonical manifest is complete, all assets pass size+SHA, and scene specs cover all canonical state families.

- [ ] **Step 2: Run full unit suite locally**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 3: Run full canonical prepare locally**

Using the already verified `JuneTrex.zip`:
`rm -rf app && python3 tools/prepare_android.py --archive JuneTrex.zip --output app --spec buildozer.spec`
Expected: PASS and report contains set metadata.

- [ ] **Step 4: Verify generated runtime/package contents**

Check `app/jtrex_sets_runtime.py`, `app/assets/sets/catalog.json`, canonical manifest, all referenced assets, and generated `main.py`; never commit `app/`.

- [ ] **Step 5: Push the integrated product/test changes once and let the normal Android workflow run**

One Android build at this milestone only. Do not publish Release/AAB manually.

---

### Task 5: Verification, memories and handoff to Lot 03

**Files:**
- Create: `docs/jt-sets-001/lot02-verification.md`
- Modify: `docs/jt-sets-001/README.md`
- Modify: `ordres-de-mission.md`
- Modify: `brain.md`
- Modify: `brainmap.md`
- Modify: `debughistorical.md`
- Modify: `todo.md`

- [ ] **Step 1: Inspect final diff against Lot 01 head `3908a0fe4163a692261ca470552bdfd08ad8f99c`**

Expected product changes limited to set runtime, canonical JSON, preparation/packaging, media/phase adaptation, tests and required CI validation.

- [ ] **Step 2: Confirm Android workflow conclusion**

Record run id, commit, unit/preparation result and Android build result. CI GREEN is not phone validation.

- [ ] **Step 3: Verify Review Focus 1..5 explicitly**

Document PASS/FAIL with evidence; no silent fallback, no path escape, no global ZeroWin mutation, policies engine-owned, one manifest source of truth.

- [ ] **Step 4: Synchronize the five living memories**

Keep them short. Lot 02 becomes fact; next planned work is Lot 03 selection/menu/freeze. Do not claim user-set switching exists yet.

- [ ] **Step 5: Commit Lot 02 verification/docs**

No merge `main`, no Release.
