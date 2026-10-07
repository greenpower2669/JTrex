# JT-SETS-001 — Vérification Lot 06

Date : 2026-10-07  
Branche : `feature/dinosaur-sets-v1`

## Résultat

Lot 06 validé côté code et CI Android.

Le lot ouvre uniquement les six coefficients approuvés par Fab, avec bornes fermées et rétrocompatibilité `parameters:{}`. Les règles de combat historiques restent moteur-owned.

## Références Git

- Base Lot 06 : clôture Lot 05 `9b3a7d58f5c73c1080b8a804814868de45d18f70`.
- Contrat approuvé : `docs/jt-sets-001/lot06-parameter-contract.md`.
- Commit contrat : `30155c4dadf62c4f5d244d7775a66bd629de1740`.
- Plan : `docs/superpowers/plans/2026-10-07-jtrex-sets-lot06.md`.
- Commit plan : `54f6e6f94160a451c12017820d37b3c0c6a73ba3`.
- Produit Lot 06 : `8d89c1ed7a70f7e55bac4e6895020a2bbd8995d2` — `feat: add bounded JTrex power parameters`.
- HEAD CI final : `d7214bb514e144dfa9191c1d6f3064718b91c570`.

## Paramètres ouverts

- left_1 `raw_damage_fraction` : défaut 0.25, bornes 0.10..0.40.
- left_2 `heal_fraction` : défaut 0.25, bornes 0.10..0.40.
- left_3 `raw_damage_fraction` : défaut 0.25, bornes 0.10..0.40.
- right_1 `raw_damage_fraction` : défaut 0.25, bornes 0.10..0.40.
- right_2 `raw_damage_fraction` : défaut 0.25, bornes 0.10..0.40.
- right_3 `raw_damage_fraction` : défaut 1/3, bornes 0.15..0.50.

`parameters:{}` reste valide et normalise vers la valeur canonique. Bool, NaN, infini, hors-bornes et clés étrangères sont refusés.

## Invariants conservés

- coûts 60/40/60/60/60/80 ;
- activation stricte `energy > cost` ;
- états 21..26 et jalons 181..186 ;
- 3 orbes/camp, nouvel échange 10 s, retour pouvoir avec temps restant ;
- KO réel seul, deux rounds gagnés = match ;
- vie initiale et score historiques ;
- lissage et énergie dérivée historiques pour les attaques ;
- Lifestream plafonné par dégâts subis et sans énergie dérivée au jalon 182 ;
- EOS média sans effet gameplay supplémentaire ;
- réarmement et protections de génération historiques.

## TDD / suite

Validation produit temporaire :
- run `37558668957` : SUCCESS ;
- archive historique vérifiée : 327992765 octets, SHA-256 `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647` ;
- préparation canonique + `py_compile` ;
- **173/173 tests PASS** ;
- patch exact ensuite fast-forwardé vers la feature.

Le premier Android #86 `37576071180` a échoué sur un garde CI obsolète exigeant le texte Lot 05 `parameters are closed in v1`, pas sur le produit.

Correction du garde CI en TDD :
- RED ciblé : run `37576362322` — échec attendu du nouveau test de contrat ;
- GREEN ciblé : run `37576423433` — SUCCESS ;
- le garde exige désormais `POWER_PARAMETER_SPECS` + `power_effect_fraction`.

## Preuve Android finale

Run Android #89 :
- run `37576480368` ;
- job `112646411728` ;
- HEAD `d7214bb514e144dfa9191c1d6f3064718b91c570` ;
- préparation historique : SUCCESS ;
- garde média/pouvoirs/score : SUCCESS ;
- compilation runtimes : SUCCESS ;
- moteur généré : **174/174 tests PASS** ;
- Buildozer / Gradle : **BUILD SUCCESSFUL** ;
- collecte et upload APK : SUCCESS.

Artefacts :
- APK artifact ID `11462494872` ;
- diagnostics ID `11462834476`.

APK extrait :
- `JuneT-Rex-1.0.15-debug.apk` ;
- taille : **156528315 octets** ;
- SHA-256 : **`4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`** ;
- empreinte recalculée indépendamment et identique à `SHA256SUMS.txt`.

## État

- Aucun merge `main`.
- Aucune Release.
- Aucun AAB.
- Validation téléphone réelle distincte de la CI et encore à faire si Fab veut valider ce candidat.
