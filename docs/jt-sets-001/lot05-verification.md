# JT-SETS-001 — Vérification Lot 05

Date : 2026-10-06  
Branche : `feature/dinosaur-sets-v1`

## Résultat

Lot 05 validé côté code et CI Android.

Le lot ajoute l'atelier admin caché, les brouillons/révisions utilisateur, l'assistant DATA/MEDIA par rôle, l'aperçu indépendant, le pont Android SAF, la promotion explicite et `TESTER CE SET`, sans ouvrir les paramètres gameplay.

## Références Git

- Plan : `docs/superpowers/plans/2026-10-06-jtrex-sets-lot05.md`.
- Base de Lot 05 : `c2460a7e0eba31922ba2a7c39646accb2514aa11`.
- HEAD produit validé : `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17`.
- Message produit : `feat: add hidden JTrex dinosaur set workshop`.

## Fonctionnalités validées

### Catalogue utilisateur et résolution

- Un set utilisateur promu résout ses médias dans sa propre révision installée.
- Aucun chemin physique absolu n'est écrit dans le manifeste portable.
- Un asset utilisateur homonyme ne retombe pas silencieusement sur un asset officiel.
- Les sets officiels conservent le résolveur applicatif historique.
- Une promotion manquante/corrompue est écartée et la sélection persistée revient proprement au canonique.
- Une révision importée n'est jamais promue automatiquement.

### Brouillons et atelier

- Les 20 touches historiques restent la porte cachée.
- Le diagnostic média historique reste accessible.
- Le joueur normal ne voit pas l'atelier.
- L'atelier est limité au MENU hors session active.
- Création depuis le set courant, reprise de brouillon, modification d'un set utilisateur, import, export, test et promotion explicite sont présents.
- L'assistant conserve progression et reprise ; il expose les rôles médias/images/audio et les six libellés de pouvoirs.
- `mechanism`, `parameters`, coûts, dégâts, chrono, KO, EOS et jalons gameplay restent non éditables.

### Aperçu indépendant

- Un seul aperçu actif.
- Surface aspect-fit dédiée et grand popup d'aperçu.
- Remplacement/fermeture libère lecteur et callbacks.
- Les vieux frame/EOS sont rejetés par génération.
- Le contrôleur d'aperçu n'a aucune surface moteur/phase/KO/énergie.
- Échec décodeur ou dimensions invalides se terminent de manière bornée avec avertissement.

### Android SAF

- Sélection de document Android avec succès/annulation/stale result couverts.
- `content://` est ouvert en lecture puis copié ; il n'est jamais passé directement à CoreVideo.
- Copie longue exécutée hors thread UI puis résultat remarshalé sur le Clock Kivy.
- Copie partielle nettoyée sur erreur.
- Export utilise le document picker Android et l'egress asynchrone.

### TESTER CE SET

- Le brouillon est validé puis figé dans une session temporaire en mémoire.
- Aucune préférence joueur ni promotion n'est écrite par le test.
- Les médias et identités de pouvoirs viennent du brouillon testé.
- Retour MENU restaure le set normal et appelle le callback de retour une seule fois.
- Vieux frame/EOS du test ne peuvent pas agir sur le contexte normal.
- Média obligatoire absent refuse le lancement.
- Échec du décodeur est borné ; le retour MENU restaure le normal.

## Preuve CI

Run d'inspection :
- run `37515396279` : SUCCESS.

Run Android #85 :
- run `37515396288` ;
- job `112446897658` ;
- HEAD `dd598f6bc6c92be818bc7af227d7eb6cd13d2a17` ;
- préparation historique : SUCCESS ;
- validation média/pouvoirs/score : SUCCESS ;
- compilation des runtimes : SUCCESS ;
- tests générés : **152/152 PASS** ;
- Buildozer / Gradle : **BUILD SUCCESSFUL** ;
- collecte et upload APK : SUCCESS.

Empreintes de préparation :
- `prepared_main_sha256 = a699120c493af6b41dc9eabc1b8040bb6b248ebf1ee7f6d85b88f4937747ff34`
- `sets_runtime_sha256 = 933ec8822c8cc50ff5faff8c3bbfe4f6bde406f269e81d86a2e244bad962df7c`
- `sets_io_runtime_sha256 = c9a02c4e2fa1f33c90ba0c0a9b1660d4bd6e4e23836537241ac50fa837c572ae`
- `sets_admin_runtime_sha256 = 07dcec9f7e16843ec65c35cc89ecb64e429789b3c3d5506bfd927eb6db1198c3`
- `sets_preview_runtime_sha256 = 0726578c718e59e2d6aa1392c0b2450105e3a9990fccd79e262e149c19806e9e`
- `sets_android_runtime_sha256 = a0651adfc78c6a892f279b2373f1e25d65244c425deac23bbdc28843d17fec5d`

## APK

Artefact GitHub Actions :
- ID `11437986330`
- nom `JuneT-Rex-1.0.15-debug`

APK extrait :
- `JuneT-Rex-1.0.15-debug.apk`
- taille : **156521694 octets**
- SHA-256 : **`fd08bc534da84fc8753cbc30bb7e8200eda2fcd3a3cbe0a6ea98147867673cc2`**

L'empreinte recalculée localement est identique à `SHA256SUMS.txt` produit par la CI.

## Non-régression

Le run CI couvre notamment :
- phases/rounds/KO ;
- orbes et protections historiques ;
- pouvoirs et identités data-driven ;
- sélection/session et isolation de callbacks ;
- stockage/import/export sécurisé ;
- brouillons/admin ;
- preview ;
- Android picker/ingress ;
- session temporaire de test.

Les règles canoniques restent moteur-owned et inchangées.

## Hors périmètre / suite

- Validation téléphone réelle : distincte de la CI, non enregistrée ici.
- Aucun merge `main`.
- Aucune Release.
- Aucun AAB.
- Lot 06 reste bloqué jusqu'à validation explicite par Fab des paramètres de pouvoirs réellement éditables et de leurs bornes.
