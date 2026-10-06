# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-06

## JT-SETS-001 — ACTIF
- [x] Feu vert Fab reçu.
- [x] Base `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e` vérifiée.
- [x] Branche `feature/dinosaur-sets-v1` créée.
- [x] Design approuvé.

## Lots 01 à 04 — TERMINÉS
- [x] Lot 01 : inventaire + contrat DATA-only.
- [x] Lot 02 : manifeste/runtime/résolution centrale.
- [x] Lot 03 : catalogue joueur + sélection/session figée.
- [x] Lot 04 : stockage + ZIP sûr/transactionnel + `content://`.

## Lot 05 — TERMINÉ
- [x] Résolution physique propre aux sets utilisateur + promotions persistantes.
- [x] Brouillons autonomes, reprenables et DATA/MEDIA-only.
- [x] Assistant par rôle + six libellés de pouvoirs ; aucun paramètre gameplay ouvert.
- [x] Preview indépendante, un seul lecteur, stale callbacks neutralisés.
- [x] Android SAF picker + ingress/egress asynchrones.
- [x] 20 touches historiques conservées ; diagnostic toujours accessible.
- [x] Atelier : créer, reprendre, modifier utilisateur, importer, exporter, tester, promouvoir.
- [x] Import sans promotion automatique ; promotion explicite rafraîchit le menu joueur.
- [x] Menu distingue OFFICIEL / UTILISATEUR.
- [x] `TESTER CE SET` temporaire sans persistance + restauration MENU.
- [x] Média obligatoire absent refusé ; décodeur en erreur borné.
- [x] Packaging des runtimes admin/preview/Android + SHA de préparation.
- [x] 152/152 tests CI verts.
- [x] Run inspection `37515396279` SUCCESS.
- [x] Run Android #85 `37515396288` SUCCESS sur `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17`.
- [x] APK 156521694 octets ; SHA-256 `fd08bc534da84fc8753cbc30bb7e8200eda2fcd3a3cbe0a6ea98147867673cc2`.
- [ ] Validation téléphone du candidat si Fab souhaite tester ce jalon.

## Lot 06 — BLOQUÉ AVANT VALIDATION FAB
- [ ] Présenter la liste auditée des paramètres de pouvoirs candidats et les bornes proposées.
- [ ] Obtenir validation explicite de Fab.
- [ ] Ensuite seulement : exposer les champs approuvés avec tests PV/énergie et non-régression.

## Non-régression globale JT-SETS-001
- [x] Set canonique équivalent sur tests/intégration.
- [x] Deux sessions successives sans lecteur/texture/callback résiduel.
- [x] Vieux EOS/frame neutralisés.
- [x] Import/export round-trip avec empreintes.
- [x] Aucun code exécutable accepté dans un pack.
- [x] Brouillon testable sans modifier la préférence joueur.

## Interdictions
- Pas de merge `main`.
- Pas de Release automatique.
- Pas d'AAB sauf demande/nécessité de livraison.
- Pas de gameplay dupliqué par set.
