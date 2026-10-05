# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-05

## JT-SETS-001 — ACTIF
- [x] Feu vert Fab reçu.
- [x] Vérifier `main` : `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- [x] Lire `ordres-de-mission.md`, `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md`.
- [x] Créer `feature/dinosaur-sets-v1` depuis le HEAD vérifié.
- [x] Formaliser le design versionné.
- [ ] Lot 01 : générer le vrai `app/main.py` depuis `JuneTrex.zip`.
- [ ] Inventorier identités, images de pouvoirs, sons, six effets, bases/cibles/réductions/plafonds/jalons.
- [ ] Produire le contrat de format v1 avec valeur canonique + conséquences + tests pour chaque paramètre candidat.
- [ ] Lot 02 : manifeste canonique + résolution centrale + équivalence du set actuel.
- [ ] Lot 03 : catalogue/menu + sélection persistante figée par match.
- [ ] Lot 04 : stockage officiel/utilisateur/brouillon + import/export ZIP sûr.
- [ ] Lot 05 : atelier 20 touches + aperçu indépendant + test brouillon.
- [ ] Lot 06 : exposer uniquement les paramètres validés par Fab avec bornes approuvées.

## Non-régression obligatoire
- [ ] Tous les tests historiques chrono/KO/EOS/HUD/pouvoirs restent verts.
- [ ] Deux sets successifs sans lecteur/texture/callback résiduel.
- [ ] Un vieux EOS ne peut pas agir sur une nouvelle session.
- [ ] Import/export round-trip avec empreintes et installation sans set source.
- [ ] Aucun code exécutable dans un pack.
- [ ] Set canonique strictement équivalent à la référence.

## Baseline Android
- Build #78 / `37245309424` : CI verte.
- APK candidat SHA-256 : `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.
- Validation téléphone complète non enregistrée au démarrage JT-SETS-001.
- Dernière Release : `v1.0.15-main`.

## Interdictions
- Pas de merge `main`.
- Pas de Release automatique.
- Pas d’AAB sauf demande/nécessité de livraison.
- Pas de refonte générale ni de gameplay dupliqué par set.
