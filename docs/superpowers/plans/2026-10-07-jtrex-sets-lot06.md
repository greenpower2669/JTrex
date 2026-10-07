# JTREX — JT-SETS-001 — Lot 06 Power Parameters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Exposer uniquement les six coefficients de pouvoirs approuvés par Fab, avec bornes strictes, tout en conservant le moteur historique comme unique autorité des coûts, jalons, énergie dérivée, KO, chrono et EOS.

**Architecture:** Le manifeste v1 reste rétrocompatible : `parameters:{}` normalise vers la valeur canonique, sinon chaque slot accepte exactement sa clé bornée. Le runtime de set fournit les valeurs normalisées ; le générateur injecte une table de coefficients dans le main historique et remplace uniquement les six littéraux `/4` ou `/3` aux jalons 181..186. L'atelier modifie ces données dans le brouillon et le contrôleur applique les paramètres du set figé comme il applique déjà les identités de pouvoirs.

**Tech Stack:** Python 3.12, JSON, Kivy existant, unittest, chaîne `prepare_android.py`/Buildozer existante.

**Spec:** `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`
**Approved contract:** `docs/jt-sets-001/lot06-parameter-contract.md`

## Global Constraints

- Champs autorisés uniquement :
  - left_1/raw_damage_fraction : défaut 0.25, bornes 0.10..0.40 ;
  - left_2/heal_fraction : défaut 0.25, bornes 0.10..0.40 ;
  - left_3/raw_damage_fraction : défaut 0.25, bornes 0.10..0.40 ;
  - right_1/raw_damage_fraction : défaut 0.25, bornes 0.10..0.40 ;
  - right_2/raw_damage_fraction : défaut 0.25, bornes 0.10..0.40 ;
  - right_3/raw_damage_fraction : défaut 1/3, bornes 0.15..0.50.
- `parameters:{}` reste valide et signifie défaut canonique.
- Valeurs finies uniquement ; bool/NaN/infini/refus hors bornes.
- Aucun mécanisme, coût, cible, état, jalon, chrono, KO, EOS, score ou formule d'énergie n'est éditable.
- Coûts 60/40/60/60/60/80 et activation stricte `energy > cost` inchangés.
- Aucun merge `main`, aucune Release, aucun AAB.

## Review Focus

1. Un ancien pack Lot 05 à `parameters:{}` doit rester importable et produire exactement les effets canoniques.
2. Le moteur ne doit jamais lire une formule du pack : seulement un float validé pour le slot courant.
3. Un paramètre d'un slot ne doit pas contaminer un autre slot ni une session suivante.
4. Lifestream doit rester exclu de l'énergie dérivée/lissage au jalon 182 et rester plafonné par les dégâts subis.
5. La valeur Meteor par défaut doit rester exactement équivalente au `pvg/3` historique malgré la représentation float.

---

### Task 1: Contrat manifeste et normalisation des coefficients

**Files:**
- Modify: `tools/jtrex_sets_runtime.py`
- Create: `tests/test_sets_power_parameters.py`
- Modify: `tests/test_sets_runtime.py`

**Interfaces:**
- Produces: `POWER_PARAMETER_SPECS`.
- Produces: `JTSetSelection.power_parameters(power_key) -> dict`.
- Produces: `JTSetSelection.power_effect_fraction(power_key) -> float`.

- [ ] Write RED tests for defaults from `{}`, explicit min/max, wrong key, bool, NaN/infini and out-of-range values.
- [ ] Run targeted tests; Expected: FAIL because parameters are currently closed.
- [ ] Implement exact per-slot schema and normalization; no generic expression support.
- [ ] Run runtime + ZIP round-trip/import tests; Expected: PASS, including old `{}` fixtures.
- [ ] Commit `feat: validate approved JTrex power parameters`.

### Task 2: Brouillon et édition atelier DATA-only

**Files:**
- Modify: `tools/jtrex_sets_admin.py`
- Create: `tests/test_sets_admin_power_parameters.py`

**Interfaces:**
- Produces: `power_parameter_fields(draft_id)`.
- Produces: `set_power_parameter(draft_id, power_key, value)`.
- Produces: `reset_power_parameter(draft_id, power_key)`.

- [ ] Write RED tests proving six fields only, defaults visible, bounded edits persisted/resumed, reset to canonical, and forbidden gameplay fields absent.
- [ ] Run targeted tests; Expected: FAIL on missing admin APIs.
- [ ] Implement atomic manifest updates through the existing runtime validator.
- [ ] Run admin/ZIP/install/export tests; Expected: PASS.
- [ ] Commit `feat: edit bounded JTrex power parameters in drafts`.

### Task 3: Application moteur historique par session figée

**Files:**
- Modify: `tools/prepare_android.py`
- Modify: `tools/jtrex_media_runtime.py`
- Create: `tests/test_power_parameter_integration.py`
- Modify existing generated-main/phase/power tests as needed.

**Interfaces:**
- Generated main exposes `JT_POWER_EFFECT_FRACTIONS` and `jt_apply_power_parameters(values)`.
- `JTMediaController` applies both power identity and normalized coefficients from the frozen session set.

- [ ] Write RED generated-main tests for canonical equivalence and one modified value per slot.
- [ ] Write RED behavior tests for attack PV + historical energy/lissage, Lifestream cap/no-energy, session isolation and reset.
- [ ] Implement exact-count replacements for the six historical `pvd/4`, `pvg/4`, `pvg/3` effect writes only.
- [ ] Apply normalized session values from the controller; no persistence or gameplay formula duplication in media runtime.
- [ ] Run phase/KO/power/full-match/session tests; Expected: PASS with costs/jalons/chrono/EOS unchanged.
- [ ] Commit `feat: apply set power coefficients in JTrex engine`.

### Task 4: UI paramètres dans l'atelier 20 touches

**Files:**
- Modify: `tools/jtrex_media_runtime.py`
- Modify: `tests/test_sets_admin_ui_contract.py`
- Create: `tests/test_sets_power_parameter_ui.py`

**Interfaces:**
- Workshop adds `PARAMÈTRES POUVOIRS`.
- Six rows show label + percentage + large decrement/increment controls + reset default.
- UI delegates all validation/writes to `JTSetAdminService`.

- [ ] Write RED UI-harness tests: admin-only, MENU-only, six fields, readable controls, inclusive bounds, reset, no cost/jalon/mechanism controls.
- [ ] Implement minimal scrollable popup with 1 percentage-point increments clamped to approved bounds.
- [ ] Ensure TESTER CE SET immediately uses draft values without promotion.
- [ ] Run workshop/player/session tests; Expected: PASS.
- [ ] Commit `feat: add JTrex workshop power parameter controls`.

### Task 5: Packaging, Android milestone et clôture Lot 06

**Files:**
- Modify: tests/workflow contracts only if integration requires guards.
- Create: `docs/jt-sets-001/lot06-verification.md`
- Modify: `docs/jt-sets-001/README.md`, `ordres-de-mission.md`, `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md`.

- [ ] Generate `app/` from SHA-proved `JuneTrex.zip`; run complete unittest discovery + `py_compile`.
- [ ] Run focused canonical-vs-explicit-default comparisons and min/max tests for all six slots.
- [ ] Inspect diff: no generated app/archive/cache tracked and no unrelated gameplay edits.
- [ ] Push exact product HEAD to `feature/dinosaur-sets-v1`; run normal Android workflow.
- [ ] Download APK artifact and record exact APK bytes + SHA-256.
- [ ] Close docs/memories only after exact Android HEAD is green.
- [ ] Commit `docs: close JT-SETS Lot06`.

## Self-review

- Coverage: approved six fields, backward compatibility, admin edit, session freeze, engine integration, UI, ZIP and Android proof all owned by explicit tasks.
- No schema path permits script/expression/formula input.
- Canonical default equivalence is tested at generated-main behavior level, not only manifest parsing.
- Meteor default equivalence is explicitly covered.
- Lot 06 does not open costs, mechanisms, timing, KO, EOS, energy formulas or jalons.
