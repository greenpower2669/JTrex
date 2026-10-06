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

## Lot 02 — TERMINÉ
- [x] Runtime contrat/catalogue/résolution.
- [x] Catalogue officiel + manifeste `trex_vs_steg` à 41 assets vérifiés.
- [x] Packaging Android dérivé du manifeste.
- [x] Run Android #80 GREEN et APK vérifié.

## Lot 03 — TERMINÉ
- [x] Catalogue officiel exposé au joueur au MENU.
- [x] Sélection persistante + fallback canonique.
- [x] Intro du dernier set valide.
- [x] Set figé pendant le match ; retour MENU autorise le set suivant.
- [x] Identités des six pouvoirs alimentées par le set figé.
- [x] Isolation de sessions + vieux EOS/frame neutralisés.
- [x] 77/77 tests ; run Android #83 GREEN ; APK vérifié.
- [ ] Validation téléphone du candidat si Fab souhaite tester ce jalon.

## Lot 04 — TERMINÉ
- [x] Trois racines séparées officiel/utilisateur/brouillon.
- [x] Limites v1 centralisées : ZIP 512 MiB, extrait 1 GiB, 512 fichiers, 512 MiB/fichier, manifeste 1 MiB, chemin 240 caractères.
- [x] Copie `content://` bornée vers brouillon + nettoyage sur erreur.
- [x] Export auto-contenu : exactement manifeste + assets référencés.
- [x] Import prévalidé : chemins interdits/doublons/symlink/chiffrement/fichier extra/exécutable refusés.
- [x] Taille/SHA + octets réellement extraits vérifiés.
- [x] Installation transactionnelle sans écrasement de révision et rollback/cleanup sur interruption.
- [x] Packaging Android de `jtrex_sets_io.py` + SHA de préparation.
- [x] Préparation canonique + 106/106 tests verts.
- [x] Run Android #84 `37477862014` SUCCESS sur `d0a56cf364f88a677f22f986d04eac5bcbe33054`.
- [x] APK 156478186 octets ; SHA-256 `759b574f49abd7f08e4607de6117fa856e005a39a0c0c72909432ac17509fedb`.
- [ ] Validation téléphone du candidat si Fab souhaite tester ce jalon.

## Lot 05 — À FAIRE MAINTENANT
- [ ] Conserver les 20 touches existantes comme porte cachée et garder le diagnostic actuel accessible.
- [ ] Atelier : créer depuis un set, modifier utilisateur, importer, exporter, tester, promouvoir une révision complète.
- [ ] Assistant par rôle : ressource actuelle, remplacement, conserver, valider/continuer, retour, progression et reprise du brouillon.
- [ ] Aperçu indépendant : aucun callback gameplay ; un seul lecteur actif ; fermeture/remplacement libère tout.
- [ ] Validation légère média : type réel, ouverture, première frame, dimensions/orientation/proportions, pistes/durée + avertissements utiles.
- [ ] `TESTER CE SET` : brouillon figé, moteur commun, restauration de la sélection normale au retour atelier.
- [ ] Média obligatoire absent => lancement test refusé ; erreur de lecture => sortie bornée sans double impact ni verrou permanent.
- [ ] Packaging/tests Android + non-régression complète + APK jalon.

## Lot 06 — PLUS TARD
- [ ] Exposer uniquement les paramètres explicitement validés par Fab avec bornes approuvées.

## Non-régression globale JT-SETS-001
- [x] Set canonique strictement équivalent sur tests/intégration.
- [x] Deux sets successifs sans lecteur/texture/callback résiduel.
- [x] Un vieux EOS ne peut pas agir sur une nouvelle session.
- [x] Import/export round-trip avec empreintes et installation sans set source.
- [x] Aucun code exécutable accepté dans un pack.

## Interdictions
- Pas de merge `main`.
- Pas de Release automatique.
- Pas d'AAB sauf demande/nécessité de livraison.
- Pas de gameplay dupliqué par set.
