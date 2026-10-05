# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-05

## JT-SETS-001 — ACTIF
- [x] Feu vert Fab reçu.
- [x] Base `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e` vérifiée.
- [x] Branche `feature/dinosaur-sets-v1` créée.
- [x] Design approuvé.
- [x] Plan Lot 01 approuvé.

## Lot 01 — TERMINÉ
- [x] Reproduire le vrai `app/main.py` depuis `JuneTrex.zip` prouvé taille + SHA.
- [x] Baseline fraîche : run `37339853652`, 38 tests OK.
- [x] Inventorier identités, médias, images, sons et mapping six slots.
- [x] Inventorier mécanismes, cibles, bases, traitement énergie/lissage et jalons.
- [x] Classer `deg`, `longanim1`, `anim1`, `indexa`, durée MP4 et EOS comme non-paramètres.
- [x] Produire `docs/jt-sets-001/format-v1-contract.md`.
- [x] Retirer le workflow diagnostic temporaire.
- [x] Vérifier le diff final : aucun changement produit/assets/workflows par rapport à la base.
- [x] Synchroniser les cinq mémoires.

## Lot 02 — PROCHAIN
- [ ] Écrire le plan Lot 02 à partir du contrat v1.
- [ ] Introduire le runtime minimal contrat/catalogue/résolution.
- [ ] Créer catalogue officiel + manifeste canonique sans déplacement massif d’assets.
- [ ] Faire résoudre intros/scènes/pouvoirs/finishings/ZeroWin par rôle logique.
- [ ] Supprimer la mutation globale de `SCENES` pour ZeroWin.
- [ ] Prouver que le set canonique garde mapping/policies/coûts/effets/chrono/KO/EOS identiques.

## Lots suivants
- [ ] Lot 03 : catalogue/menu + sélection persistante figée par match.
- [ ] Lot 04 : stockage officiel/utilisateur/brouillon + import/export ZIP sûr.
- [ ] Lot 05 : atelier 20 touches + aperçu indépendant + test brouillon.
- [ ] Lot 06 : exposer uniquement les paramètres validés par Fab avec bornes approuvées.

## Non-régression globale JT-SETS-001
- [x] Lot 01 : tests historiques restent verts, sans code produit modifié.
- [ ] Deux sets successifs sans lecteur/texture/callback résiduel.
- [ ] Un vieux EOS ne peut pas agir sur une nouvelle session.
- [ ] Import/export round-trip avec empreintes et installation sans set source.
- [ ] Aucun code exécutable accepté dans un pack.
- [ ] Set canonique strictement équivalent via le nouveau résolveur.

## Interdictions
- Pas de merge `main`.
- Pas de Release automatique.
- Pas d’AAB sauf demande/nécessité de livraison.
- Pas de gameplay dupliqué par set.
