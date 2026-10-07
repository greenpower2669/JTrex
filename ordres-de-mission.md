# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-07

## Contrat permanent
1. Ne jamais recoder de mémoire : relire code, tests et preuves Git avant modification.
2. `ordres-de-mission.md` définit le contrat actif ; les autres mémoires restent spécialisées et courtes.
3. Ne pas modifier les règles canoniques historiques sans ordre explicite de Fab.
4. Avant toute annonce de succès : preuve fraîche adaptée.
5. Aucun merge `main`, Release ou AAB sans ordre explicite de Fab.

## Canon gameplay protégé
- 3 orbes/camp ; nouvel échange 10 s ; retour pouvoir = temps restant.
- KO réel seul = round ; deux rounds = match ; vrai nouveau round = énergie 0/0.
- Vie 500000000/camp ; score historique.
- Coûts 60/40/60/60/60/80 ; activation stricte `energy > cost`.
- États 21..26 et jalons 181..186 moteur-owned.
- EOS média n'applique aucun effet gameplay.

## JT-SETS-001 — LOTS 01 À 06 TERMINÉS CODE/CI
Branche : `feature/dinosaur-sets-v1`. Base : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.

- Lots 01–05 : contrat DATA/MEDIA, runtime/catalogue, sélection/session, stockage ZIP sûr, atelier admin, preview/SAF/test brouillon.
- Lot 06 : six coefficients seulement, approuvés par Fab et bornés :
  - STSF/STTA/TRFS/TRPH : dégâts 0.10..0.40, défaut 0.25 ;
  - Lifestream : soin 0.10..0.40, défaut 0.25 ;
  - Meteor : dégâts 0.15..0.50, défaut 1/3.
- `parameters:{}` reste rétrocompatible = défaut canonique.
- Aucun coût, mécanisme, jalon, chrono, KO, score, énergie dérivée ou EOS éditable.

Preuves Lot 06 :
- produit `8d89c1ed7a70f7e55bac4e6895020a2bbd8995d2` ;
- HEAD CI `d7214bb514e144dfa9191c1d6f3064718b91c570` ;
- validation produit : 173/173 tests ;
- Android #89 `37576480368`, job `112646411728` : SUCCESS, 174/174 tests ;
- APK 156528315 octets, SHA-256 `4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`.

## État
JT-SETS-001 est techniquement complet côté code/CI. Validation téléphone du candidat Lot 06 reste distincte et non enregistrée.
Dernière Release : `v1.0.15-main`.


## JT-SETS-UI-001 — correction téléphone (2026-10-07)
- Autorisé par Fab après validation visuelle du candidat Lot 06.
- Portée UI uniquement : sélecteur compact, atelier/création/catalogue/brouillons/assistant scrollables, raccourci admin ✎.
- Set officiel via ✎ = création d'un brouillon depuis le set ; set utilisateur = modification directe.
- Aucun changement gameplay, coûts, coefficients, phases, KO, score, jalons ou EOS.
- Branche : `feature/dinosaur-sets-v1`.
