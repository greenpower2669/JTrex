# JTREX — JT-SETS-001 — Vérification Lot 04

Date : 2026-10-06
Branche : `feature/dinosaur-sets-v1`
Statut : TERMINÉ / VALIDÉ CI

## Portée

Lot 04 ajoute uniquement le stockage et l'I/O des sets :
- racine officielle embarquée en lecture seule ;
- racine utilisateur persistante ;
- racine brouillon séparée ;
- copie Android `content://` vers un vrai fichier local de brouillon ;
- export ZIP auto-contenu ;
- import ZIP sûr et transactionnel.

Exclusions respectées : aucun atelier admin, aucun aperçu admin, aucun mode test brouillon, aucun paramètre gameplay éditable, aucun changement de règles moteur.

## Contrat portable et sécurité

Un pack v1 contient exactement `manifest.json` et les assets référencés par ce manifeste.

Refus couverts par tests :
- traversée `..`, chemin absolu, backslash/drive Windows, NUL ;
- doublon/collision case-insensitive ;
- symlink ;
- entrée chiffrée ;
- fichier extra non référencé ;
- type exécutable/interdit ;
- asset manquant ;
- format/manifeste incompatible ;
- taille ou SHA forgés ;
- collision avec identifiant officiel ;
- collision de même révision utilisateur.

Limites v1 centralisées :
- ZIP : 512 MiB ;
- total extrait : 1 GiB ;
- nombre de fichiers : 512 ;
- taille par fichier : 512 MiB ;
- manifeste : 1 MiB ;
- chemin : 240 caractères.

L'extraction compte les octets réellement copiés, puis revalide taille et SHA des assets. L'installation se fait dans un staging sur le même filesystem ; seule la dernière opération rend la révision visible par renommage atomique. Une collision ou une exception avant ce renommage conserve l'ancienne révision et nettoie le staging.

`content://` n'est jamais transmis directement à CoreVideo : la ressource est copiée vers le brouillon avec limite réelle et suppression du fichier partiel en cas d'erreur.

## Implémentation

Commit produit : `156ee830155bc34c840a83666de20fca43fb72d8`

Fichiers produit/tests principaux :
- `tools/jtrex_sets_runtime.py` : helpers publics de manifeste portable et vérification d'assets ;
- `tools/jtrex_sets_io.py` : stockage, limites, ingress, import/export et transaction ;
- `tools/prepare_android.py` : staging du runtime I/O + empreinte dans le rapport ;
- tests Lot 04 : `test_sets_io*.py` ;
- `.github/workflows/android.yml` : compilation/validation du runtime I/O dans la chaîne Android.

`app/main.py` reste généré depuis l'archive historique et n'est pas une source versionnée.

## Preuve fonctionnelle / non-régression

Archive historique utilisée :
- taille : 327992765 octets ;
- SHA-256 : `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.

Préparation canonique : OK.
Runtime I/O préparé SHA-256 : `a607282406c734be9c93fed3fd6c21866b10267b8c7b486521fe9cc792d7e29b`.

Suite complète après préparation : **106/106 tests verts**.
Elle couvre notamment :
- round-trip export/import et empreintes ;
- pack incomplet/incompatible ;
- zip-slip et chemins interdits ;
- collisions ;
- interruption avant installation finale ;
- comptage des octets réels ;
- copie `content://` ;
- non-régression phases, 10 s, pouvoirs, KO, rounds, match, stale callbacks/EOS et isolation de sessions.

## Validation Android finale

HEAD testé : `d0a56cf364f88a677f22f986d04eac5bcbe33054`
Commit workflow : `ci: validate JT-SETS Lot04 set I/O in Android build`

Run #84 : `37477862014`
Job : `112317924340`
Conclusion : **SUCCESS**.

Toutes les étapes sont vertes, notamment :
- archive historique ;
- préparation JuneTrex ;
- validation média/audio/pouvoir/score ;
- compilation des runtimes sets ;
- tests moteur/présentation générés ;
- Buildozer et python-for-android ;
- build APK ;
- collecte et upload APK.

Artefact APK : `11421465099` (`JuneT-Rex-1.0.15-debug`).
Digest ZIP artefact GitHub : `sha256:9482f4d88876a1292285a27405b4471337c6b1518b6cce9824c39370568dca01`.

APK extrait :
- fichier : `JuneT-Rex-1.0.15-debug.apk` ;
- taille : **156478186 octets** ;
- SHA-256 : **`759b574f49abd7f08e4607de6117fa856e005a39a0c0c72909432ac17509fedb`**.

## Décision

Lot 04 fermé. Aucun merge `main`, aucune Release, aucun AAB.

Lot suivant : **Lot 05 — atelier admin via les 20 touches, assistant par rôle, aperçu indépendant et TESTER CE SET sur brouillon figé**. Les paramètres de gameplay restent fermés jusqu'au Lot 06 et validation explicite de Fab.
