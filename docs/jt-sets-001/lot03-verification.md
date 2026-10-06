# JT-SETS-001 — Vérification Lot 03

Date : 2026-10-06
Branche : `feature/dinosaur-sets-v1`
Base Lot 03 : `9efad3d0dfaf480aa46e715442d104357969abef`
Commit produit : `dfad8fbc5ae4678fb5bd704ea38a858116966a5b`
HEAD de validation Android : `c5330f29814430944500839aa3bcd29afbc3ff8b`

## Périmètre validé
- catalogue officiel lisible au MENU ;
- sélection officielle persistante entre lancements ;
- fallback et réparation vers `trex_vs_steg` si JSON/ID persisté invalide ;
- écriture de l'état par remplacement atomique ;
- intro de lancement basée sur le dernier set persisté valide ;
- set figé au début de la session et changement refusé pendant le match ;
- retour MENU termine la session et autorise la sélection du prochain match ;
- changement au menu invalide lecteur, reprise et génération de l'ancien set ;
- médias, six couples d'icônes ready/used, sons d'activation et fallbacks audio proviennent du même set figé ;
- aucune règle de gameplay, coût, mécanisme, jalon, KO, round, chrono ou score déplacée dans le manifeste.

## TDD et non-régression
Suite complète : 77/77 tests verts.

Couvertures Lot 03 principales :
- catalogue ordonné et rejet des doublons ;
- persistance valide, JSON cassé, ID inconnu et écriture atomique ;
- gel de session et refus de changement en match ;
- deux sessions synthétiques successives A puis B ;
- vieux frame/EOS de A sans effet sur B ;
- résolution set-aware des identités de pouvoirs ;
- 12 affectations d'icônes ready/used du main généré pilotées par `JT_POWER_PATHS` ;
- préparation du main historique audité conservant chrono/KO/pouvoirs historiques.

## Android
Workflow : `Build June T-Rex APK`
Run : #83 — `37417205571`
Conclusion : SUCCESS.

Étapes vérifiées GREEN :
- archive historique téléchargée ;
- `prepare_android.py` exécuté ;
- hooks historiques inspectés ;
- média/audio/pouvoirs/score validés ;
- moteur généré et phases exercés ;
- dépendances Buildozer/p4a installées ;
- APK debug construit, collecté et uploadé.

Artefact APK GitHub : `11391049002` (`JuneT-Rex-1.0.15-debug`).
Digest ZIP artefact : `sha256:b3b3886af98f2585ebedac179cedfc89dc1a6e1d69a03adf1fae15f570c0df65`.

Fichier APK extrait :
- nom : `JuneT-Rex-1.0.15-debug.apk` ;
- taille : 156468471 octets ;
- SHA-256 : `612af2912050c392c63ec2054b03fc875b3a7a4c8f915c3a40d074cb077dec20`.

## Interdictions respectées
- aucun merge `main` ;
- aucune Release ;
- aucun AAB ;
- aucune duplication du moteur de gameplay par set ;
- aucun import ZIP, atelier admin ou équilibrage ajouté dans ce lot.

## Suite contractuelle
Lot 04 : stockage officiel/utilisateur/brouillon et import/export ZIP sûr, transactionnel et non exécutable.
