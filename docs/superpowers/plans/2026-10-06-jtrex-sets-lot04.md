# JTREX — JT-SETS-001 — Lot 04 Storage & ZIP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ajouter un stockage officiel/utilisateur/brouillon et un import/export ZIP auto-contenu, sûr et transactionnel, sans brancher encore l’atelier admin ni modifier le gameplay.

**Architecture:** Conserver `jtrex_sets_runtime.py` comme autorité unique du contrat de manifeste, et créer `tools/jtrex_sets_io.py` pour les racines persistantes, les limites, l’export, le staging d’import et la copie `content://` vers brouillon. Un pack portable contient exactement `manifest.json` et les assets référencés par ce manifeste. Une révision utilisateur s’installe sous `<user_root>/<set_id>/r<revision>/` par renommage final atomique ; une collision n’écrase jamais une révision existante.

**Tech Stack:** Python 3.12, `zipfile`, `hashlib`, `tempfile`, `pathlib`, `shutil`, `os`, `stat`, `unittest`, chaîne Android/Buildozer existante.

**Spec:** `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`

## Global Constraints

- Le gameplay, les phases, KO, rounds, score, coûts, mécanismes, jalons d’impact et politiques EOS restent moteur-owned et inchangés.
- Pack DATA/MEDIA uniquement : aucun script, Python, KV, module natif, pickle, expression ou téléchargement distant.
- Trois racines logiques : officiel embarqué lecture seule, utilisateur persistant, brouillon séparé.
- Le statut officiel vient uniquement du catalogue embarqué.
- Collision d’identifiant/révision : jamais d’écrasement silencieux.
- Installation depuis staging sur le même filesystem ; ancienne révision préservée si erreur/interruption.
- Android `content://` : toujours copié dans le brouillon avant utilisation locale.
- Limites v1 centralisées : ZIP 512 MiB ; total extrait 1 GiB ; 512 fichiers ; 512 MiB par fichier ; manifeste 1 MiB ; chemin 240 caractères.
- Aucun merge `main`, aucune Release, aucun AAB.

## Review Focus

1. Zip-slip/chemins Windows/backslash/drive/`..`/NUL et doublons case-insensitive doivent être refusés avant écriture.
2. Symlink, entrée chiffrée, fichier extra non référencé ou type exécutable doit être refusé.
3. Taille ZIP, taille membre, total annoncé ET octets réellement copiés doivent rester sous limites ; taille/SHA du manifeste doivent correspondre après extraction.
4. Collision ou exception juste avant le renommage final doit laisser l’ancienne révision intacte et aucun dossier final partiel.
5. `content://` doit produire un fichier local dans brouillon, avec copie bornée et nettoyage sur erreur ; aucune URI ne devient chemin CoreVideo.

---

### Task 1: Autorité publique du manifeste et vérification des assets

**Files:**
- Modify: `tools/jtrex_sets_runtime.py`
- Test: `tests/test_sets_runtime.py`
- Test: `tests/test_sets_io.py`

**Interfaces:**
- Produces: `load_set_manifest(resolve_path, manifest_path="manifest.json") -> JTSetSelection`
- Produces: `verify_selection_assets(selection, resolve_path) -> tuple[dict, ...]`
- Produces: `JTSetSelection.manifest() -> dict`
- Consumed by: Task 2/3 import/export and packaging checks.

- [ ] **Step 1: Write failing tests** for portable manifest loading, defensive manifest copy, streamed size/SHA verification, missing asset and forged size/SHA.
- [ ] **Step 2: Run targeted tests**; Expected: FAIL only because the public APIs do not exist.
- [ ] **Step 3: Implement minimal public helpers** by reusing `_safe_path`, `_read_json` and `_validate_manifest`; hash assets in chunks, never duplicate gameplay validation.
- [ ] **Step 4: Run targeted + existing set runtime tests**; Expected: PASS.
- [ ] **Step 5: Commit** `feat: expose validated portable set helpers`.

### Task 2: Racines de stockage, limites et ingress Android

**Files:**
- Create: `tools/jtrex_sets_io.py`
- Test: `tests/test_sets_io_storage.py`
- Test: `tests/test_sets_io_content_uri.py`

**Interfaces:**
- Consumes: Task 1 manifest/asset helpers.
- Produces: `JTSetIOLimits`
- Produces: `JTSetStorage(official_root, user_root, draft_root, limits=None)`
- Produces: `user_revision_path(set_id, revision) -> Path`
- Produces: `draft_path(draft_id) -> Path`
- Produces: `copy_content_uri(uri, open_stream, draft_name) -> Path`

- [ ] **Step 1: Write failing tests** for root separation, official read-only behavior, safe IDs/revisions, exact v1 limits, local draft path, bounded `content://` copy and cleanup on stream failure.
- [ ] **Step 2: Run tests**; Expected: FAIL because `jtrex_sets_io` is absent.
- [ ] **Step 3: Implement storage/limits** with no Kivy/Android dependency; `open_stream` is injected and only `content://` is accepted by the ingress API.
- [ ] **Step 4: Run tests**; Expected: PASS.
- [ ] **Step 5: Commit** `feat: add JTrex set storage roots and ingress`.

### Task 3: ZIP export et import transactionnel

**Files:**
- Modify: `tools/jtrex_sets_io.py`
- Test: `tests/test_sets_io_zip.py`
- Test: `tests/test_sets_io_security.py`

**Interfaces:**
- Consumes: `JTSetStorage`, `JTSetIOLimits`, `load_set_manifest`, `verify_selection_assets`.
- Produces: `export_set(selection, resolve_path, destination_zip) -> Path`
- Produces: `import_set_zip(archive_path, official_set_ids=()) -> ImportResult`
- Produces: `load_user_revision(set_id, revision) -> JTSetSelection`
- Produces: `ImportResult(set_id, revision, installed_path)`.

- [ ] **Step 1: Write failing round-trip tests** asserting ZIP contains exactly `manifest.json` + referenced assets and import restores a self-contained revision with identical hashes.
- [ ] **Step 2: Write failing security tests** for traversal, absolute/backslash/colon/NUL, duplicate/casefold collision, symlink, encrypted member, extra file, missing asset, unsupported format, limits, forged size/SHA, official-ID collision and same-revision collision.
- [ ] **Step 3: Write failing transaction test** that raises before final rename and proves prior revision/final path unchanged and staging removed.
- [ ] **Step 4: Run tests**; Expected: FAIL on absent import/export implementation.
- [ ] **Step 5: Implement archive preflight** before extraction, then chunked extraction with real byte accounting, manifest validation, asset verification, and same-filesystem atomic final rename.
- [ ] **Step 6: Implement export** to a temporary sibling ZIP, validate source assets first, write only allowed members, then `os.replace` destination.
- [ ] **Step 7: Run Task 3 + all set tests**; Expected: PASS.
- [ ] **Step 8: Commit** `feat: add transactional JTrex set zip io`.

### Task 4: Packaging Android et non-régression

**Files:**
- Modify: `tools/prepare_android.py`
- Modify: `.github/workflows/android.yml`
- Modify: `tests/test_android_set_workflow_contract.py`
- Create: `tests/test_sets_io_packaging.py`

**Interfaces:**
- Consumes: `tools/jtrex_sets_io.py`.
- Produces: staged `app/jtrex_sets_io.py` and preparation report SHA.

- [ ] **Step 1: Write failing packaging/workflow tests** requiring `jtrex_sets_io.py` in staged app, report SHA and workflow trigger/static compile guard.
- [ ] **Step 2: Run targeted tests**; Expected: FAIL on missing packaging integration.
- [ ] **Step 3: Update preparer/workflow minimally**; do not touch gameplay or media policies.
- [ ] **Step 4: Generate `app` from canonical `JuneTrex.zip` and run complete unittest discovery**; Expected: all historical + Lot 04 tests PASS.
- [ ] **Step 5: `py_compile` runtimes and inspect diff**; Expected: no generated `app/`, archive or cache tracked.
- [ ] **Step 6: Commit** `ci: package transactional JTrex set io`.

### Task 5: Android milestone et clôture Lot 04

**Files:**
- Create: `docs/jt-sets-001/lot04-verification.md`
- Modify: `docs/jt-sets-001/README.md`
- Modify: `ordres-de-mission.md`
- Modify: `brain.md`
- Modify: `brainmap.md`
- Modify: `debughistorical.md`
- Modify: `todo.md`

**Interfaces:**
- Consumes: final Lot 04 HEAD and normal Android workflow.

- [ ] **Step 1: Push Lot 04 product HEAD** to `feature/dinosaur-sets-v1`; normal Android workflow only.
- [ ] **Step 2: Verify workflow through APK upload**; Expected: SUCCESS on exact HEAD.
- [ ] **Step 3: Download APK artifact and compute APK SHA-256**; record exact bytes/SHA.
- [ ] **Step 4: Final review**: round-trip, incomplete pack, forbidden path, collision, incompatible format, interrupted import, URI copy, historical gameplay tests all evidenced.
- [ ] **Step 5: Synchronize verification + five living memories** and mark Lot 05 next.
- [ ] **Step 6: Commit** `docs: close JT-SETS Lot04`.

## Self-review

- Spec coverage: stockage 3 racines, pack auto-contenu, sécurité ZIP, limites, octets réels, staging transactionnel, collisions, `content://`, packaging et non-régression couverts.
- Exclusions respectées: aucune UI atelier, aperçu, mode test brouillon ou paramètre gameplay dans Lot 04.
- Interfaces cohérentes: le contrat manifeste reste dans `jtrex_sets_runtime`; l’I/O dépend de lui, jamais l’inverse.
- Les cinq risques Review Focus ont chacun un test propriétaire dans Tasks 2/3.
