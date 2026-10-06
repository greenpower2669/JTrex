# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-06

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
- [x] Runtime contrat/catalogue/résolution.
- [x] Catalogue officiel + manifeste `trex_vs_steg` à 41 assets vérifiés.
- [x] Intros/scènes/pouvoirs/finishings/ZeroWin résolus par rôle logique.
- [x] Packaging Android dérivé du manifeste.
- [x] Run Android #80 GREEN et APK vérifié.

## Lot 03 — TERMINÉ
- [x] Catalogue officiel exposé au joueur au MENU.
- [x] Sélection persistante avec écriture atomique et fallback canonique sûr.
- [x] Intro de démarrage sur le dernier set valide.
- [x] Set figé pendant tout le match ; sélection refusée en session active.
- [x] Retour MENU termine la session et autorise le set du match suivant.
- [x] Changement au menu invalide lecteur/reprise/génération de l'ancien set.
- [x] Identités des six pouvoirs (images + sons + fallbacks) alimentées par le set figé.
- [x] Deux sessions synthétiques successives sans identité/callback résiduel.
- [x] Vieux EOS/frame de session A sans effet sur session B.
- [x] Suite complète 77/77 verte.
- [x] Run Android #83 `37417205571` GREEN sur `c5330f29814430944500839aa3bcd29afbc3ff8b`.
- [x] APK `JuneT-Rex-1.0.15-debug.apk` = 156468471 octets ; SHA-256 `612af2912050c392c63ec2054b03fc875b3a7a4c8f915c3a40d074cb077dec20`.
- [ ] Validation téléphone du candidat si Fab souhaite tester ce jalon.

## Lots suivants
- [ ] Lot 04 : stockage officiel/utilisateur/brouillon + import/export ZIP sûr et transactionnel.
- [ ] Lot 05 : atelier 20 touches + aperçu indépendant + test brouillon.
- [ ] Lot 06 : exposer uniquement les paramètres validés par Fab avec bornes approuvées.

## Non-régression globale JT-SETS-001
- [x] Set canonique strictement équivalent sur tests/intégration.
- [x] Deux sets successifs sans lecteur/texture/callback résiduel.
- [x] Un vieux EOS ne peut pas agir sur une nouvelle session.
- [ ] Import/export round-trip avec empreintes et installation sans set source.
- [ ] Aucun code exécutable accepté dans un pack.

## Interdictions
- Pas de merge `main`.
- Pas de Release automatique.
- Pas d'AAB sauf demande/nécessité de livraison.
- Pas de gameplay dupliqué par set.
