# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-05

## JT-SETS-001 — ACTIF
- [x] Feu vert Fab reçu.
- [x] Base `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e` vérifiée.
- [x] Branche `feature/dinosaur-sets-v1` créée.
- [x] Design approuvé.

## Lot 01 — TERMINÉ
- [x] Inventaire identité/médias/pouvoirs/mécanismes.
- [x] Contrat format v1 DATA-only fermé.
- [x] Preuves archive/main/tests et mémoires synchronisées.

## Lot 02 — TERMINÉ
- [x] Runtime minimal contrat/catalogue/résolution.
- [x] Catalogue officiel + manifeste `trex_vs_steg` à 41 assets vérifiés.
- [x] Intros/scènes/pouvoirs/finishings/ZeroWin résolus par rôle logique.
- [x] Mutation globale `SCENES` de ZeroWin supprimée.
- [x] Packaging Android dérivé du manifeste ; JSON embarqués.
- [x] TDD : 18 nouveaux tests ; suite complète 56/56 OK (`37378554085`).
- [x] Workflow Android exact restauré (`ee8cf297...`, blob `c22bcf400...`).
- [x] APK final : run #80 `37379193862` GREEN ; artefact APK `11375685200` ; `JuneT-Rex-1.0.15-debug.apk` = 156461520 octets, SHA-256 `182e1b8f72f269a7e3f3f24895e37fe23a1b3ade9e77949d14500827c13c320c`.
- [ ] Validation téléphone du candidat si Fab souhaite tester ce jalon avant Lot 03.

## Lots suivants
- [ ] Lot 03 : catalogue/menu + sélection persistante figée par match + fallback canonique sûr.
- [ ] Lot 04 : stockage officiel/utilisateur/brouillon + import/export ZIP sûr.
- [ ] Lot 05 : atelier 20 touches + aperçu indépendant + test brouillon.
- [ ] Lot 06 : exposer uniquement les paramètres validés par Fab avec bornes approuvées.

## Non-régression globale JT-SETS-001
- [x] Set canonique strictement équivalent via le résolveur sur tests/intégration.
- [ ] Deux sets successifs sans lecteur/texture/callback résiduel.
- [ ] Un vieux EOS ne peut pas agir sur une nouvelle session.
- [ ] Import/export round-trip avec empreintes et installation sans set source.
- [ ] Aucun code exécutable accepté dans un pack.

## Interdictions
- Pas de merge `main`.
- Pas de Release automatique.
- Pas d'AAB sauf demande/nécessité de livraison.
- Pas de gameplay dupliqué par set.
