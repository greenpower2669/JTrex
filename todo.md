# JTrex / June T-Rex — TODO

## État actuel

Phase : RECONSTRUCTION DOCUMENTAIRE AVANT PORTAGE ANDROID.

Référence fonctionnelle : JuneTrex/main.py de la release JTrex, SHA-256 3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231.

Révision main servant de référence : 164d03be77c83f49e1094294f36f860ec183df68.

Interdictions actuelles :

- ne modifier aucun code ;
- ne supprimer aucun bloc hérité ;
- ne renommer ou convertir aucun média ;
- ne corriger aucune JT-OBS ;
- ne changer aucun réglage Buildozer/workflow ;
- ne lancer aucun build ni déploiement dans la mission documentaire ;
- ne rechercher/remplacer les vidéos originales qu'après nouvelle autorisation de Fab.

## Terminé dans cette mission documentaire

- [x] Créer le cerveau fonctionnel JTrex dans brain.md.
- [x] Cartographier classes, fonctions, variables, états, callbacks et Android dans brainmap.md.
- [x] Consigner JT-OBS-001 à JT-OBS-026 dans debughistorical.md.
- [x] Séparer constats, conséquences à confirmer et intentions à valider.
- [x] Documenter le moteur air hockey comme héritage encore exécuté.
- [x] Documenter les séries d'images et leurs indices.
- [x] Documenter les deux chronomètres car et car2.
- [x] Documenter l'IA et les cinq niveaux.
- [x] Documenter les six pouvoirs et leur asymétrie.
- [x] Documenter les confrontations rouge/bleu et jaunes.
- [x] Ajouter six organigrammes Mermaid du comportement actuel.
- [x] Enregistrer l'ordre de mission et l'objectif futur Android.

## À valider avec Fab avant toute modification fonctionnelle

- [ ] Nom complet historique de ST si une documentation utilisateur l'exige.
- [ ] Noms complets des six pouvoirs ; ne pas les déduire de sf/ls/ta/fs/ph/ma.
- [ ] Confirmer si le seuil S différent gauche/droite est voulu.
- [ ] Confirmer si les asymétries d'énergie sont voulues.
- [ ] Confirmer le comportement voulu en cas de double KO.
- [ ] Confirmer le comportement voulu de l'IA dans les confrontations au tapotement.
- [ ] Confirmer l'intention de conservation ou de retrait futur du moteur air hockey une fois ses dépendances prouvées.
- [ ] Confirmer le comportement attendu du soin état 22.

## Validation future du jeu de référence — seulement après autorisation

- [ ] Démarrer une partie humain/humain.
- [ ] Vérifier rouge/vert/bleu à gauche et à droite.
- [ ] Arrêter les trois orbes d'un camp avant l'autre.
- [ ] Laisser car2 forcer l'arrêt des six orbes.
- [ ] Comparer un échange gagné à gauche puis à droite.
- [ ] Obtenir une égalité et vérifier l'état jaune.
- [ ] Faire basculer une confrontation avec une puis trois touches d'avance.
- [ ] Vérifier la continuité d'images lors d'un changement de variante.
- [ ] Tester séparément les six pouvoirs.
- [ ] Comparer énergie=60 et énergie>60.
- [ ] Vérifier qu'un pouvoir utilisé ne redevient pas disponible pendant le même combat.
- [ ] Observer le soin avec vie très basse et vie presque pleine.
- [ ] Tester une fin gauche, une fin droite et un double KO.
- [ ] Vérifier le retour menu puis une deuxième partie.
- [ ] Tester les cinq niveaux et les quatre combinaisons humain/ordinateur.
- [ ] Observer l'ordinateur pendant les phases de tapotement.
- [ ] Comparer le score sur plusieurs tailles de fenêtre.
- [ ] Appuyer à l'emplacement d'une commande graphiquement masquée.
- [ ] Vérifier pause/reprise.
- [ ] Vérifier quel main.py le workflow Android sélectionne réellement.

## Préparation future du portage Android — ne pas commencer ici

Ordre recommandé après validation du comportement historique :

1. figer une version de référence reproductible ;
2. sélectionner explicitement JuneTrex/main.py dans le pipeline ;
3. vérifier les ressources sensibles à la casse ;
4. vérifier l'image absente charge tr win 83 sans substitution automatique ;
5. vérifier dimensions/ratios des séries ;
6. décider quelles dépendances du moteur air hockey sont encore nécessaires ;
7. définir une architecture Android qui reproduit d'abord le comportement observé ;
8. conserver les formules de score, dégâts, énergie et timers jusqu'à validation ;
9. ajouter nom/version/icône cohérents ;
10. produire et tester un APK installable ;
11. produire un AAB séparé si la diffusion Play l'exige.

## Médias futurs

Après stabilisation du portage seulement :

- [ ] Retrouver les vidéos originales.
- [ ] Établir une table vidéo ↔ séquence d'images.
- [ ] Comparer timing, événements d'impact, audio et embranchements.
- [ ] Faire valider par Fab.
- [ ] Remplacer progressivement les séries, sans perte des états 2–7 ni des bifurcations.

## Prochain geste

Ne rien coder à partir de cette seule reconstruction.

Le prochain geste autorisable est une phase de validation d'exécution de la référence historique ou un nouvel ordre de mission explicite de Fab.


## Audit de complétude du relais Astra

- [x] Relire le relais Astra contre les cinq mémoires.
- [x] Rendre explicites choixidh/choixidb.
- [x] Rendre explicite le rôle temporel non normalisant de colv[7..9].
- [x] Conserver les limites de provenance : hash main.py seulement, variantes historiques non comparées, séries non toutes vérifiées visuellement.
- [x] Consigner les variantes/sauvegardes horseg2ko sans substitution automatique.
- [x] Conserver les nuances du suivi tactile hérité.
- [x] Confirmer qu'aucune correction de code ni validation d'exécution n'a été effectuée.


## JT-ANDROID-001 — Premier APK installable

État : DOSSIER ASTRA EN PRÉPARATION / AUCUN CODE MODIFIÉ.

- [x] Lire les cinq mémoires à la référence actuelle.
- [x] Vérifier que main est sur `379ae278f2199cad26f1746c418512f47e04d106`.
- [x] Créer `port/android-first-apk` depuis cette référence.
- [x] Lire le buildozer.spec actuel.
- [x] Lire le workflow Android actuel.
- [x] Vérifier les métadonnées de la release/tag JTrex et le digest de JuneTrex.zip.
- [x] Confirmer que le workflow actuel dépend de `releases/latest` et du premier `main.py`.
- [ ] Faire valider/proposer par Astra les modifications Android ciblées.
- [ ] Appliquer uniquement les modifications proposées et justifiées.
- [ ] Construire l'APK 📦.
- [ ] Installer/exécuter si un environnement compatible est disponible ; sinon marquer « à valider par Fab ».
- [ ] Préparer l'AAB 📦 si la chaîne le permet.
- [ ] Publier une préversion de test seulement après contrôles.

Prochain geste : transmettre à Astra le dossier ciblé JT-ANDROID-001. Aucun gameplay ne doit être modifié.


## JT-ANDROID-001 — patch Astra appliqué

- [x] Ajouter `tools/prepare_android.py`.
- [x] Figer la release source `JTrex` et la racine `JuneTrex`.
- [x] Vérifier archive et main historique par empreintes avant adaptation.
- [x] Préparer les corrections de casse uniquement sur la copie de compilation.
- [x] Passer le candidat à version 1.0.1 / numeric version 101.
- [x] Configurer l'icône provisoire `pter/pter0.png`.
- [x] Conserver JT-OBS-003 sans remplacement d'image.
- [x] Remplacer le workflow par le build APK ciblé et diagnostics bornés.
- [ ] Examiner le résultat réel de GitHub Actions.
- [ ] Relever Buildozer et python-for-android réellement utilisés.
- [ ] Si APK produit : vérifier taille, SHA-256, package/version/architectures/signature avec les outils disponibles.
- [ ] Rapporter à Astra les logs/diagnostics et le commit exact.
- [ ] Validation téléphone par Fab.
- [ ] AAB après stabilisation APK.


## JT-ANDROID-001 — résultat run #7

- [x] Préparation archive/main vérifiée.
- [x] Buildozer et python-for-android réellement identifiés.
- [x] Diagnostic complet récupéré.
- [ ] Corriger l'échec native libffi/autoreconf uniquement après proposition Astra.
- [ ] Relancer un scénario identique après une seule correction discriminante.
- [ ] Produire l'APK 📦.
- [ ] Vérifier statiquement package/version/architectures/signature.
- [ ] Faire valider sur téléphone par Fab.

Blocage actuel précis :
`configure.ac:215: error: possibly undefined macro: LT_SYS_SYMBOL_USCORE`.

Prochain geste : transmettre à Astra le run #7, les révisions d'outillage et cette première erreur pertinente.


## JT-ANDROID-001 — FAB-DEBUG-001 essai n°1

- [x] Hypothèse unique reçue : ajouter `libltdl-dev`.
- [x] Limiter la modification à `.github/workflows/android.yml`.
- [ ] Relancer le même build.
- [ ] Vérifier si `autoreconf` franchit `LT_SYS_SYMBOL_USCORE`.
- [ ] Si nouvelle erreur : consigner uniquement la première nouvelle erreur discriminante.


## JT-ANDROID-001 — résultat FAB-DEBUG-001 essai n°1

- [x] `libltdl-dev` installé.
- [x] Blocage `LT_SYS_SYMBOL_USCORE` franchi.
- [x] Versions Buildozer/python-for-android comparées : inchangées.
- [x] Nouveau blocage isolé.
- [ ] Transmettre à Astra l'erreur pip interne Python 3.14.2.
- [ ] Recevoir une seule correction ciblée.
- [ ] Relancer le même scénario.
- [ ] Produire l'APK 📦.

Nouvelle première erreur :
`ImportError: cannot import name 'BuildDependencyInstallError' from 'pip._internal.exceptions'`.

Commande interne associée :
`source venv/bin/activate && pip install -U pip`.


## JT-ANDROID-001 — FAB-DEBUG-001 essai n°2

- [x] Vérifier la ligne exacte dans `pythonforandroid/build.py` au SHA p4a utilisé.
- [x] Ajouter le patch versionné `p4a-venv-clear.patch`.
- [x] Préparer le workflow pour utiliser exactement la base p4a `58d2114…` puis appliquer le patch.
- [x] Conserver `pip install -U pip`, Python 3.14.2 et le reste de la chaîne inchangés.
- [ ] Relancer le même build.
- [ ] Vérifier dans le journal la commande `python -m venv --clear venv`.
- [ ] Vérifier si `pip install -U pip` termine avec code 0 sur les deux architectures.
- [ ] Si nouvelle erreur : isoler uniquement la première nouvelle erreur discriminante.


## JT-ANDROID-001 — run #9 réussi

- [x] Patch p4a `venv --clear` appliqué au SHA de base.
- [x] Build debug APK réussi.
- [x] APK collecté.
- [x] SHA-256 calculé.
- [x] Architectures arm64-v8a et armeabi-v7a confirmées.
- [x] Signature debug identifiée.
- [ ] Fab installe et ouvre l'APK sur téléphone.
- [ ] Vérifier nom, icône, paysage, menu et Start.
- [ ] Vérifier les 3 orbes des deux camps.
- [ ] Vérifier première confrontation et retour au menu.
- [ ] Selon retour Fab, corriger uniquement les problèmes observés.
- [ ] Publier ensuite une préversion GitHub stable si l'outil de publication est disponible.
- [ ] AAB 📦 après stabilisation APK.


## Mission vidéo / icône — intake

- [x] Vérifier les cinq fichiers à la racine de `main`.
- [x] Importer leurs blobs uniquement dans `assets/` sur `port/android-first-apk`.
- [x] Préparer l'inspection ffprobe + images début/milieu/fin.
- [x] Préparer l'extraction des hooks historiques de `main.py`.
- [ ] Confirmer visuellement/techniquement le rôle de `StegVsTrexvaetviensremolace.mp4`.
- [ ] Choisir un fournisseur vidéo Android compatible avec la chaîne p4a figée.
- [ ] Passer à une version/versionCode supérieure pour le premier APK qui active les vidéos.
- [ ] Intégrer l'intro aléatoire et l'icône.
- [ ] Brancher la vidéo d'attente uniquement après confirmation du point d'intégration.
- [ ] Construire et livrer l'APK installable direct.


### Inspection légère
- [x] Ajouter un workflow séparé d'inspection média/source, sans compilation APK, afin de récupérer rapidement les preuves avant intégration.


## JT-MEDIA-001 — intégration candidate 1.0.2

- [x] Confirmer codecs/durations des 4 vidéos.
- [x] Confirmer `indexa=1 / dinos1 / vv` comme attente aller-retour historique.
- [x] Préparer intro aléatoire unique avec audio original et blocage des touches.
- [x] Différer jtrm0.wav jusqu'à la fin de l'intro.
- [x] Préparer vidéo d'attente en texture du Rectangle historique, audio vidéo muet.
- [x] Préserver le moteur et les JPEG comme repli.
- [x] Configurer JtrexIcon.png.
- [x] Passer à 1.0.2 / versionCode 102.
- [x] Ajouter MP4 aux extensions.
- [x] Ajouter ffpyplayer et recette FFmpeg 6.1.2 compatible candidate.
- [ ] Faire passer la préparation sur GitHub Actions.
- [ ] Faire passer le build APK.
- [ ] Vérifier inclusion MP4, ABIs et signature.
- [ ] Livrer l'APK direct à Fab.
- [ ] Validation téléphone : intro, son, icône, attente vidéo, attaque, retour attente, pause/reprise.


## JT-MEDIA-001 — FAB-DEBUG vidéo essai Python 3.11

- [x] Run #11 : préparation média réussie.
- [x] Run #11 : FFmpeg 6.1.2 franchi suffisamment pour atteindre ffpyplayer.
- [x] Isoler l'incompatibilité ffpyplayer 4.5.1 / Python 3.14.
- [x] Vérifier le mécanisme p4a de pin `VERSION_<recipe>`.
- [x] Fixer python3 à 3.11.13 et hostpython3 à la même version.
- [ ] Relancer exactement le candidat 1.0.2.
- [ ] Vérifier disparition des erreurs `_PyLong_AsByteArray` / `_PyGen_SetStopIterationValue`.
- [ ] Si build vert : récupérer et contrôler l'APK.
