# JTREX — JT-SETS-001 — Lot 05 Admin Workshop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ajouter l’atelier admin caché, les brouillons/révisions utilisateur, l’assistant par rôle, l’aperçu média indépendant et `TESTER CE SET`, tout en gardant le moteur de combat unique et le gameplay historique inchangé.

**Architecture:** Conserver les 20 touches et le diagnostic actuel dans `jtrex_media_runtime.py`, mais déplacer toute la logique d’atelier dans des modules spécialisés. Un set officiel, utilisateur promu ou brouillon garde un manifeste DATA-only ; chaque `JTSetSelection` connaît aussi son résolveur physique afin que les médias utilisateur hors APK soient lisibles sans mettre de chemin absolu dans le manifeste. Le test d’un brouillon utilise une session temporaire figée du même moteur, ne persiste jamais la sélection et revient à l’atelier au retour MENU.

**Tech Stack:** Python 3.12, Kivy, CoreVideo/ffpyplayer existant, `pathlib`, `hashlib`, `json`, `threading`, Android SAF via `pyjnius`/module `android` déjà fourni par la chaîne p4a, `unittest`, Buildozer existant.

**Spec:** `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`

## Global Constraints

- Le gameplay, les phases, KO, rounds, score, coûts, mécanismes, jalons d’impact et règles EOS restent moteur-owned et inchangés.
- Les coûts restent 60/40/60/60/60/80 et l’activation reste strictement `énergie > coût`.
- Aucun paramètre d’équilibrage n’est éditable au Lot 05 ; `parameters` reste `{}` et les mécanismes restent fermés jusqu’au Lot 06.
- Les 20 touches existantes restent l’unique porte cachée ; le diagnostic média existant reste accessible.
- Le joueur normal ne voit jamais l’atelier.
- Les sets utilisateur restent DATA/MEDIA uniquement ; aucun script, KV, natif, expression ou ressource distante.
- `content://` est copié dans le brouillon avant aperçu/validation ; jamais passé directement à CoreVideo.
- Une seule prévisualisation active ; fermeture/remplacement libère lecteur et callbacks.
- `TESTER CE SET` utilise une révision de brouillon figée, n’écrit pas la préférence joueur et restaure la sélection normale en revenant à l’atelier.
- Un média obligatoire absent refuse le test ; un échec média doit finir de manière bornée sans double impact ni verrou permanent.
- UI admin : texte lisible, grandes commandes, aperçu agrandissable.
- Aucun merge `main`, aucune Release, aucun AAB sans ordre explicite de Fab.

## Review Focus

1. Un set utilisateur hors APK doit résoudre ses médias depuis sa propre révision installée, sans chemin absolu dans le manifeste et sans fallback silencieux vers un asset officiel homonyme.
2. Une révision promue supprimée/corrompue au redémarrage doit disparaître du menu et la préférence doit revenir au canon, sans casser les sets officiels.
3. Un sélecteur Android annulé, une permission URI refusée ou une copie longue interrompue ne doit ni bloquer l’UI ni laisser un candidat partiel utilisable.
4. Un aperçu fermé/remplacé ou un vieux callback de preview ne doit jamais muter le moteur, la session de combat, ni l’aperçu courant.
5. Un test de brouillon interrompu par retour MENU, erreur média ou arrêt applicatif doit restaurer la sélection normale et ne jamais promouvoir/persister implicitement le brouillon.

---

### Task 1: Résolution physique par set et catalogue utilisateur promu

**Files:**
- Modify: `tools/jtrex_sets_runtime.py`
- Modify: `tools/jtrex_sets_io.py`
- Test: `tests/test_sets_user_resolution.py`
- Test: `tests/test_sets_selection.py`

**Interfaces:**
- Produces: `JTSetSelection.resolve_path(relative_path) -> str | None`.
- Produces: `JTSetSelection.resolve_asset(asset_id) -> str | None`.
- Produces: `JTSetStorage.list_user_revisions() -> tuple[tuple[str, int], ...]`.
- Produces: `JTSetStorage.load_promotions() -> dict[str, int]` and `promote(set_id, revision) -> None` with atomic JSON replace.
- Produces: `JTSetStorage.promoted_catalog() -> tuple[JTSetSelection, ...]`.
- Modify: `JTSetSessionManager(..., user_catalog_provider=None)` plus `refresh_catalog()`; official IDs remain authoritative and collisions are rejected.

- [ ] **Step 1: Write failing tests** proving an official selection resolves through the bundled resolver while a loaded user revision resolves only inside its installed root; identical relative names must not cross-resolve.
- [ ] **Step 2: Write failing tests** for promotion index persistence, latest chosen revision, corrupt/missing promoted revision removal, official collision refusal and fallback canonique when a persisted user set disappears.
- [ ] **Step 3: Run targeted tests**; Expected: FAIL only on missing new APIs.
- [ ] **Step 4: Implement resolver ownership + promotion index** without adding physical paths to manifests.
- [ ] **Step 5: Extend session manager refresh** while preserving frozen active sessions and startup intro semantics.
- [ ] **Step 6: Run existing Lot 02–04 set/session/I-O tests + new tests**; Expected: PASS.
- [ ] **Step 7: Commit** `feat: resolve promoted JTrex user sets from installed revisions`.

### Task 2: Brouillon auto-contenu et assistant DATA-only

**Files:**
- Create: `tools/jtrex_sets_admin.py`
- Test: `tests/test_sets_admin_drafts.py`
- Test: `tests/test_sets_admin_roles.py`

**Interfaces:**
- Consumes: `JTSetStorage`, `JTSetSelection`, `load_set_manifest`, `verify_selection_assets`.
- Produces: `JTAdminRole(role_id, label, asset_type, required)`.
- Produces: `JTDraftState(draft_id, set_id, revision, role_index, source_kind)`.
- Produces: `JTSetAdminService(storage, official_set_ids)`.
- Produces methods: `create_from_selection(...)`, `open_draft(draft_id)`, `roles(draft_id)`, `current_role(draft_id)`, `previous_role(draft_id)`, `keep_and_next(draft_id)`, `stage_candidate(draft_id, role_id, local_path)`, `accept_candidate(draft_id, role_id)`, `set_identity(...)`, `validate_complete(draft_id)`, `install_revision(draft_id)`, `export_revision(...)`.

- [ ] **Step 1: Write failing tests** for cloning a full official/user selection into a self-contained draft and resuming `draft-state.json` after service recreation.
- [ ] **Step 2: Write failing role tests** for ordered roles covering current intros, combat media, portraits/thumbnail and six power media/images/audio while never exposing `mechanism`, `parameters`, costs, damage, chrono or EOS.
- [ ] **Step 3: Write failing candidate tests**: replacement stays separate until accepted; wrong type/path/oversize rejected; accept updates manifest asset size/SHA and prunes superseded unreferenced draft asset.
- [ ] **Step 4: Write failing identity tests** for safe new `set_id`, revision >=1, display/dinosaur names, official-ID collision and user revision increment.
- [ ] **Step 5: Implement minimal pure-Python admin service** with atomic manifest/state writes and no Kivy/Android imports.
- [ ] **Step 6: Run tests**; Expected: PASS and `validate_complete()` returns a normal `JTSetSelection` verified against the draft resolver.
- [ ] **Step 7: Commit** `feat: add resumable DATA-only JTrex set drafts`.

### Task 3: Aperçu indépendant et validation légère des médias

**Files:**
- Create: `tools/jtrex_sets_preview.py`
- Test: `tests/test_sets_preview.py`

**Interfaces:**
- Produces: `JTPreviewResult(kind, opened, first_frame, dimensions, duration, warnings)`.
- Produces: `JTSetPreviewController(root, core_video_cls, clock, image_loader=None, sound_loader=None)`.
- Produces methods: `preview(path, kind, expected_role=None)`, `close(reason="close")`.
- Controller receives no engine/global gameplay dict and exposes no gameplay callback.

- [ ] **Step 1: Write failing fake-player tests** proving one preview active, replacement closes/unbinds previous player, stale frame/EOS ignored by generation, and close releases callbacks/widgets.
- [ ] **Step 2: Write failing probe tests** for video open + first frame + dimensions/duration, image decode, audio open, zero/invalid dimensions and decoder failure with bounded completion/warnings.
- [ ] **Step 3: Write a guard test** asserting preview controller has no engine/phase/KO/energy callback surface and fake preview events cannot mutate a supplied gameplay sentinel.
- [ ] **Step 4: Implement preview controller** reusing the same CoreVideo provider class as combat but separate player/generation state; aspect-fit preview, no combat scene policy.
- [ ] **Step 5: Run tests**; Expected: PASS.
- [ ] **Step 6: Commit** `feat: add isolated JTrex set media preview`.

### Task 4: Android document picker and non-blocking ingress

**Files:**
- Create: `tools/jtrex_sets_android.py`
- Test: `tests/test_sets_android_picker.py`
- Test: `tests/test_sets_async_copy.py`

**Interfaces:**
- Produces: `AndroidDocumentPicker(on_pause=None, on_resume=None)` with `choose(mime_type, callback)` and `close()`.
- Produces: `open_content_stream(uri) -> BinaryIO` using `ContentResolver.openFileDescriptor(...).detachFd()` + `os.fdopen`.
- Produces: `JTAsyncIngress(storage, clock, thread_factory=None)` with `copy(uri, draft_name, on_done)`; worker does I/O, callback returns on Kivy clock/main thread.

- [ ] **Step 1: Write failing picker tests** for success, cancel, duplicate/stale activity result, close/unbind and permission/open failure.
- [ ] **Step 2: Write failing async ingress tests** proving `copy()` returns immediately, only worker performs the long read, completion is marshalled onto the injected clock, and partial copy is cleaned on error.
- [ ] **Step 3: Implement Android bridge with imports deferred until use** so desktop/CI can import the module.
- [ ] **Step 4: Run tests**; Expected: PASS.
- [ ] **Step 5: Commit** `feat: add Android SAF ingress for JTrex set workshop`.

### Task 5: Session temporaire TESTER CE SET

**Files:**
- Modify: `tools/jtrex_sets_runtime.py`
- Modify: `tools/jtrex_media_runtime.py`
- Test: `tests/test_sets_draft_test_session.py`
- Test: `tests/test_sets_session_isolation.py`

**Interfaces:**
- Produces: `JTSetSessionManager.begin_temporary_session(selection) -> JTSetSelection` ; never persists/changes normal selected set.
- Produces: `JTSetSessionManager.session_temporary -> bool`.
- Produces: `JTMediaController.start_draft_test(selection, return_callback=None)`; MENU-only, verifies no active session, freezes temp set, applies power identity, sets engine `indexa=4`, synchronizes phases.
- On next MENU, ends temp session, restores selected normal set and invokes `return_callback` once.

- [ ] **Step 1: Write failing tests** proving temporary session cannot start over an active session, keeps official/user menu preference untouched, and uses only draft media/power identities.
- [ ] **Step 2: Write failing lifecycle tests** for MENU return, media failure, stale EOS/frame from test session and second normal match after test; all must restore normal selection and generation isolation.
- [ ] **Step 3: Implement session override** as an in-memory selection only; no state-file write and no promotion side effect.
- [ ] **Step 4: Implement controller launch/return hook** using existing phase sync and existing bounded media failure behavior; do not duplicate gameplay start logic.
- [ ] **Step 5: Run historical phase/KO/power/session tests + new tests**; Expected: PASS.
- [ ] **Step 6: Commit** `feat: add isolated draft test sessions`.

### Task 6: Atelier 20 touches et assistant lisible

**Files:**
- Modify: `tools/jtrex_media_runtime.py`
- Modify: `tools/prepare_android.py`
- Test: `tests/test_sets_admin_ui_contract.py`
- Test: `tests/test_sets_player_catalog.py`

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: diagnostic popup actuel + bouton `ATELIER SETS` visible uniquement quand mode 20 touches actif.
- Produces workshop flows: créer depuis set courant, reprendre brouillon, modifier set utilisateur promu, importer ZIP, exporter révision, assistant par rôle, `TESTER CE SET`, installer/promouvoir.
- Player selector displays official/user distinction and only official + user revisions explicitly promoted.

- [ ] **Step 1: Write failing static/UI-harness tests** proving 20 taps still enable the existing diagnostic, normal player menu has no workshop action, workshop actions are disabled outside MENU/while session active, and controls use readable labels/large heights.
- [ ] **Step 2: Write failing assistant flow tests** for current preview, choose replacement, replacement preview, keep, validate/continue, previous, progress, resume draft and final validation.
- [ ] **Step 3: Write failing import/export/promotion UI tests**: imported revision is not automatically promoted; promotion refreshes player catalogue; deleting/corrupting promotion falls back safely.
- [ ] **Step 4: Integrate workshop popup** without embedding storage/model logic into widget callbacks; callbacks delegate to `JTSetAdminService`, preview, picker/ingress and session APIs.
- [ ] **Step 5: Adapt generated main only for the existing controller hooks required by test launch if necessary**; exact-count replacements and tests mandatory, no gameplay formula edits.
- [ ] **Step 6: Run all admin/player/session tests**; Expected: PASS.
- [ ] **Step 7: Commit** `feat: add hidden JTrex dinosaur set workshop`.

### Task 7: Packaging, non-régression et Android milestone

**Files:**
- Modify: `tools/prepare_android.py`
- Modify: `.github/workflows/android.yml`
- Modify: `tests/test_android_set_workflow_contract.py`
- Create: `tests/test_sets_admin_packaging.py`
- Create: `docs/jt-sets-001/lot05-verification.md`
- Modify: `docs/jt-sets-001/README.md`
- Modify: `ordres-de-mission.md`
- Modify: `brain.md`
- Modify: `brainmap.md`
- Modify: `debughistorical.md`
- Modify: `todo.md`

**Interfaces:**
- Packages: `jtrex_sets_admin.py`, `jtrex_sets_preview.py`, `jtrex_sets_android.py` plus existing runtimes.

- [ ] **Step 1: Write failing packaging/workflow tests** requiring all Lot 05 runtimes staged/compiled and their SHA values reported by preparation.
- [ ] **Step 2: Update preparer/workflow minimally** and generate `app` from the SHA-proved historical `JuneTrex.zip`.
- [ ] **Step 3: Run complete unittest discovery + `py_compile`**; Expected: all historical + Lots 01–05 PASS, with no generated `app/`, archive, draft or cache tracked.
- [ ] **Step 4: Run focused full-match/session tests** proving 10 s exchange, return-power remaining time, KO-only rounds, 2-win match, one impact, energy reset, stale callbacks and canonical media equivalence unchanged.
- [ ] **Step 5: Push exact product HEAD and run the normal Android workflow once**; Expected: SUCCESS through APK upload.
- [ ] **Step 6: Download APK artifact, record exact bytes + SHA-256 and note phone validation still distinct from CI.
- [ ] **Step 7: Synchronize verification + five living memories** and mark Lot 06 next only after Lot 05 evidence is green.
- [ ] **Step 8: Commit** `docs: close JT-SETS Lot05`.

## Self-review

- Spec coverage: 20 touches/diagnostic, création/modification/import/export, assistant par rôle et reprise, preview indépendante, validation média, Android SAF, copie non bloquante, promotion menu joueur et test brouillon sont tous attribués à une tâche.
- Frontière gameplay : aucun mécanisme, coût, dégât, soin, chrono, KO, score, transition ou jalon n’est rendu éditable.
- Résolution utilisateur : le plan traite explicitement le fait que les ressources installées vivent hors APK ; le résolveur reste runtime-only et n’entre jamais dans le manifeste.
- Transaction : Lot 05 réutilise le stockage/I-O Lot 04 pour installation/export et n’invente pas une seconde logique ZIP.
- Test brouillon : sélection temporaire purement mémoire, session figée, restauration MENU, aucun effet de persistance/promotion.
- Review Focus : chaque risque a un test propriétaire dans Tasks 1, 3, 4 ou 5.
