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


## 2026-09-28 — FAB-DEBUG-001 / JT-MEDIA-001

- [x] Remplacer le pin intermédiaire Python 3.11.13 par `python3==3.12.14,hostpython3==3.12.14` dans le seul `buildozer.spec` racine.
- [ ] Relever le run GitHub Actions déclenché par ce commit et son commit construit.
- [ ] Vérifier si la préparation franchit la garde héritée 3.11.13 ; sinon classer l'hypothèse comme non testée/incomplète.
- [ ] Si ffpyplayer est atteint, relever requirements p4a, Python/hostpython, Cython isolé si visible, et résultat sur arm64-v8a puis armeabi-v7a.
- [ ] Si un APK est produit, relever SHA-256 et artefact `JuneT-Rex-1.0.2-debug.apk` ; la validation vidéo/gameplay reste à Fab sur téléphone.


### Après run #13

- [x] Run #13 identifié : `36355762409`, commit `0f73b3d31d4dc242daecb102f4c18579c8413627`.
- [x] Premier nouveau blocage relevé : garde 3.11.13 dans `tools/prepare_android.py`.
- [x] Ne pas ajouter de seconde correction dans le run #13.
- [ ] Prochain ordre de mission : décider séparément si la garde/reporting 3.11.13 du préparateur doit être alignée sur 3.12.14 pour permettre au test d'atteindre p4a.
- [ ] Après cette décision seulement, relancer et relever les preuves p4a/ffpyplayer demandées.


## 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — alignement préparation Python 3.12.14

- [x] Aligner la garde `requirements` de `tools/prepare_android.py` sur `python3==3.12.14`.
- [x] Aligner le message d'exception sur 3.12.14.
- [x] Aligner `python_target` du rapport sur 3.12.14.
- [x] Aligner la ligne descriptive du rapport sur 3.12.14.
- [ ] Vérifier que le prochain run franchit `Verify and prepare JuneTrex sources`.
- [ ] Relever dans p4a les versions effectives de python3 et hostpython3, ffpyplayer et le résultat par architecture.
- [ ] Vérifier disparition/persistance de `_PyLong_AsByteArray` et `_PyGen_SetStopIterationValue`.
- [ ] En cas d'échec, consigner uniquement la première nouvelle erreur discriminante ; ne pas ajouter un second correctif dans la même tentative.
- [ ] Annoncer l'APK 📦 1.0.2 uniquement s'il est réellement produit, avec SHA-256.


### Après run #14

- [x] Garde préparation 3.12.14 franchie.
- [x] Confirmer dans p4a les versions demandées : python3 3.12.14 et hostpython3 3.12.14.
- [x] Confirmer téléchargement des deux sources CPython v3.12.14.
- [x] Isoler la première nouvelle erreur : `Modules/grpmodule.c` sous armeabi-v7a, fonctions `setgrent/getgrent/endgrent` indisponibles/non déclarées.
- [x] Confirmer que ffpyplayer n'est pas encore compilé et que arm64-v8a n'est pas atteint pour python3.
- [x] Consigner l'export workflow hérité `VERSION_hostpython3=3.11.13` sans le modifier dans cette tentative.
- [ ] Transmettre le run #14 à Astra pour analyse et prochaine correction mono-hypothèse.
- [ ] Ne pas annoncer d'APK 📦 1.0.2 tant qu'il n'existe pas réellement.


## 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — grp Android API 21

- [x] Créer `tools/patches/p4a-python312-grp-api21.patch` avec l'exclusion ciblée `py_cv_module_grp=n/a`.
- [x] Ajouter le patch à `on.push.paths`.
- [x] Appliquer le patch par `git apply --check` puis `git apply` après `p4a-venv-clear.patch`.
- [x] Ne pas modifier `VERSION_hostpython3=3.11.13` dans cette tentative.
- [ ] Vérifier le message `JT-MEDIA-001: target grp unavailable below Android API 26`.
- [ ] Vérifier `checking for stdlib extension module grp... n/a`.
- [ ] Vérifier l'absence de compilation de `Modules/grpmodule.c`.
- [ ] Relever séparément la progression de python3 sur armeabi-v7a puis arm64-v8a.
- [ ] Si Python passe, relever ensuite la compilation ffpyplayer et les erreurs `_PyLong_AsByteArray` / `_PyGen_SetStopIterationValue`.
- [ ] En cas de nouvel échec, consigner seulement la première erreur discriminante sans ajouter de second correctif.
- [ ] Nettoyer ultérieurement l'export historique `VERSION_hostpython3=3.11.13` dans une mission distincte.


### Après run #15

- [x] Confirmer l'application du patch p4a grp.
- [x] Confirmer le message de recette JT-MEDIA-001.
- [x] Distinguer hostpython Linux (`grp... yes`) et Python Android cible (`grp... n/a`).
- [x] Confirmer l'absence de compilation de `Modules/grpmodule.c` pour la cible Android.
- [x] Confirmer que le blocage grp du run #14 est franchi.
- [x] Isoler la première nouvelle erreur : FFmpeg 6.1.2 / Vulkan sur armeabi-v7a, `VkVideoSessionParametersKHR = NULL`.
- [x] Confirmer que arm64-v8a et la phase réelle `Building ffpyplayer` ne sont pas atteintes.
- [ ] Transmettre à Astra le run #15 et la commande configure FFmpeg contenant `--enable-hwaccels`.
- [ ] Conserver le nettoyage de `VERSION_hostpython3=3.11.13` pour une mission distincte.
- [ ] Ne pas annoncer d'APK 📦 1.0.2 tant qu'il n'existe pas réellement.


## 2026-09-28 — JT-MEDIA-001 — exclusion Vulkan FFmpeg 6.1.2

- [x] Ajouter uniquement `--disable-vulkan` après `--enable-hwaccels` dans `tools/p4a-ffmpeg-6.1.2.py`.
- [ ] Vérifier que la configuration effective contient `--disable-vulkan`.
- [ ] Vérifier que Vulkan et ses accélérations sont désactivés.
- [ ] Vérifier que H.264, AAC et le démuxeur MOV/MP4 restent actifs.
- [ ] Si visible dans les fichiers générés, confirmer `CONFIG_VULKAN=0`, `CONFIG_H264_DECODER=1`, `CONFIG_AAC_DECODER=1`, `CONFIG_MOV_DEMUXER=1`.
- [ ] Relever le résultat FFmpeg puis ffpyplayer pour chaque architecture.
- [ ] Vérifier la disparition/persistance de `_PyLong_AsByteArray` et `_PyGen_SetStopIterationValue` lorsque ffpyplayer est réellement compilé.
- [ ] En cas d'échec, consigner uniquement la première nouvelle erreur discriminante sans ajouter de second correctif.
- [ ] Annoncer l'APK 📦 1.0.2 uniquement s'il est réellement produit, avec SHA-256.


### Après run #16
- [x] `--disable-vulkan` transmis aux deux architectures.
- [x] FFmpeg 6.1.2 postbuild sur arm64-v8a et armeabi-v7a.
- [x] ffpyplayer 4.5.1 postbuild sur arm64-v8a et armeabi-v7a.
- [x] Absence de `_PyLong_AsByteArray` / `_PyGen_SetStopIterationValue`.
- [x] APK 📦 `JuneT-Rex-1.0.2-debug.apk` produit.
- [x] SHA-256 : `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a`.
- [ ] Fab : validation téléphone des intros, icône, vidéo d'attente, fluidité, audio et gameplay.


### Crash téléphone 1.0.2 — diagnostic ouvert

- [x] Identifier l'APK réellement transmis : run #16 / commit `e88bd93ec0a7d9b34b2d4f64eb10b3627d230149`.
- [x] Vérifier version 1.0.2, versionCode 102 et package `com.junedady.junetrex` dans les logs de packaging.
- [x] Vérifier SHA-256 réel : `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a`.
- [x] Vérifier que l'APK contient `arm64-v8a` et `armeabi-v7a`.
- [ ] Récupérer `jtrex-demarrage.txt` depuis le téléphone avec logcat non filtré.
- [ ] Relever modèle téléphone, version Android et ABI réellement utilisée.
- [ ] Relever le dernier marqueur effectivement observé parmi `[JT-BOOT]`, `[JT-START]`, `[JT-INTRO] chosen=`, `[JT-INTRO] begin=`, `[JT-INTRO] gameplay enabled`.
- [ ] Extraire le traceback Python complet ; sinon l'exception Java ou le signal natif + backtrace.
- [ ] Identifier la première erreur fatale et la fonction/ressource/bibliothèque concernée.
- [ ] Ne proposer aucune correction tant que cette première erreur fatale n'est pas établie.


### Crash téléphone 1.0.2 — bugreport exploité

- [x] Récupérer un rapport téléphone complet sans ordinateur.
- [x] Identifier appareil : SM-A576B / Android 16 / arm64-v8a.
- [x] Confirmer installation : com.junedady.junetrex 1.0.2, versionCode 102.
- [x] Identifier la première erreur fatale reproductible : `Python initialization failed: failed to get the Python codec of the filesystem encoding`.
- [x] Confirmer que `main.py` et tous les marqueurs JT ne sont pas atteints.
- [x] Confirmer statiquement que `_python_bundle/stdlib.zip` contient bien `encodings` et `codecs.pyc`.
- [ ] Transmettre ce diagnostic à Astra pour la prochaine correction mono-hypothèse.
- [ ] Ne modifier ni Python, ni p4a, ni FFmpeg, ni Cython, ni runtime média, ni gameplay avant le nouvel ordre Astra.


## 2026-09-28 — FAB-DEBUG-001 — diagnostic bootstrap Python

- [x] Relire le bugreport sans filtrage limité au tag python.
- [x] Confirmer l'absence de traceback/ModuleNotFoundError/ImportError/ZipImportError/bad magic autour du lancement.
- [x] Confirmer que les probes libpython3.14/3.13 échouent mais libpython3.12.so charge avec succès.
- [x] Créer `tools/patches/p4a-python312-bootstrap-exception-diag.patch`.
- [x] Appliquer le patch au start.c du checkout p4a figé avant construction.
- [ ] Vérifier dans p4a-patch.txt que le start.c effectif contient P4A_DIAG.
- [ ] Produire l'APK diagnostique et relever run/commit/SHA-256.
- [ ] Fab : installer l'APK diagnostique et générer un nouveau rapport complet immédiatement après le crash.
- [ ] Relever status.func/status.err_msg, version native, module_search_paths, stdlib.zip, exception raised/cause/context.
- [ ] Ne pas annoncer le crash corrigé tant que [JT-BOOT] n'est pas atteint.


### Après run #17
- [x] Identifier l'échec comme un patch corrompu avant compilation.
- [x] Confirmer qu'aucun nouveau diagnostic Python n'a été exécuté.
- [x] Corriger uniquement les compteurs/en-têtes des hunks du patch bootstrap diagnostique.
- [ ] Relancer le même diagnostic sans autre changement fonctionnel.


### Après run #18

- [x] Relancer le diagnostic après correction des en-têtes de hunks.
- [x] Confirmer run #18 réussi.
- [x] Confirmer le diff P4A_DIAG dans le checkout p4a effectif.
- [x] Confirmer compilation de start.c pour arm64-v8a et armeabi-v7a.
- [x] Produire l'APK diagnostique.
- [x] SHA-256 : `fbc4a1d0f72cf677591e4a4ffb366db9237377c5f5c3574d6f7ca025249d8e64`.
- [ ] Fab : installer l'APK diagnostique du run #18.
- [ ] Fab : lancer JTrex puis générer immédiatement un nouveau rapport de bug complet.
- [ ] Extraire les lignes P4A_DIAG : version, chemins, stdlib.zip, status.func, status.err_msg, exception raised/cause/context.
- [ ] Ne pas annoncer « crash corrigé » tant que [JT-BOOT] n'est pas atteint.


### Après bugreport diagnostic du run #18

- [x] Recevoir un nouveau rapport complet du téléphone.
- [x] Relever `status.func=init_fs_encoding`.
- [x] Relever `ZipImportError: can't decompress data; zlib not available`.
- [x] Relever le contexte `ImportError: dlopen failed: cannot locate symbol "PyExc_MemoryError"`.
- [x] Vérifier que stdlib.zip existe et est lisible.
- [x] Vérifier les module_search_paths réels.
- [x] Vérifier statiquement zlib.cpython-312.so et libpython3.12.so dans l'APK arm64-v8a.
- [x] Confirmer que libpython exporte `PyExc_MemoryError`.
- [x] Confirmer que zlib a ce symbole non résolu et n'a pas `libpython3.12.so` dans DT_NEEDED.
- [ ] Transmettre à Astra cette cause immédiate pour décision sur une seule correction mono-hypothèse.
- [ ] Ne rien modifier avant retour Astra.


## 2026-09-28 — FAB-DEBUG-001 — visibilité globale libpython

- [x] Contrôler run #18 avant modification : FLAGS_1=NOW, GLOBAL absent sur arm64-v8a et armeabi-v7a.
- [x] Confirmer PyExc_MemoryError toujours exporté par libpython.
- [x] Relever l'absence de DT_SONAME explicite dans le libpython du run #18 sans la modifier.
- [x] Créer `tools/patches/p4a-python312-libpython-global.patch`.
- [x] Limiter l'enregistrement du patch à python3 cible version 3.12.14.
- [x] Limiter `-Wl,-z,global` à la cible `libpython$(LDVERSION).so`.
- [ ] Vérifier application du patch p4a dans le prochain run.
- [ ] Vérifier `-Wl,-z,global` dans la commande effective de liaison.
- [ ] Vérifier `FLAGS_1` avec `GLOBAL` dans le nouvel APK pour les deux ABI.
- [ ] Vérifier PyExc_MemoryError toujours exporté.
- [ ] Relever le SONAME réel du nouvel APK sans inventer sa présence.
- [ ] Ne transmettre à Fab pour test runtime que si GLOBAL est réellement matérialisé.
- [ ] Sur téléphone : vérifier disparition du dlopen PyExc_MemoryError puis progression de Py_InitializeFromConfig et [JT-BOOT].


### Après run #19

- [x] Build #19 réussi.
- [x] Relever `-Wl,-z,global` dans les commandes de liaison des deux ABI.
- [x] Vérifier `FLAGS_1: NOW GLOBAL` sur arm64-v8a.
- [x] Vérifier `FLAGS_1: NOW GLOBAL` sur armeabi-v7a.
- [x] Vérifier `PyExc_MemoryError` toujours exporté sur les deux ABI.
- [x] Relever l'absence persistante de DT_SONAME explicite sans la corriger.
- [x] SHA-256 APK : `945f795bce1b925ac981df48bbd3781d73d5816927ef4356ce00e2875068a241`.
- [ ] Fab : installer l'APK du run #19.
- [ ] Fab : lancer JTrex et vérifier si le bootstrap franchit l'ancien blocage.
- [ ] Si crash : générer immédiatement un rapport complet et relever la première nouvelle erreur discriminante.
- [ ] Ne pas annoncer « crash corrigé » avant réussite de Py_InitializeFromConfig et apparition de [JT-BOOT].

## 2026-09-30 — JT-MEDIA-POWER-SCORE-001

- [x] Vérifier que la branche active est exactement au SHA Android audité `a6caa620…` avant patch.
- [x] Importer uniquement les cinq nouveaux médias depuis main, sans merge global.
- [x] Généraliser le contrôleur vidéo aux familles 1 / 2-4 / 5-7 / 8 / 9.
- [x] Conserver 10/11 historiques, intros aspect-fit+audio et combat muet.
- [x] Passer les scènes de jeu en aspect-fill et protéger les callbacks par génération.
- [x] Définir `POWER_COSTS = 60/40/60 | 60/60/80` et la garde stricte `énergie > coût`.
- [x] Revalider tactile et IA au déclenchement et débiter le coût exact une seule fois.
- [x] Recalculer bonus/select depuis la même disponibilité.
- [x] Corriger le verrou de disponibilité droit et l'identité slot4 TRFS / slot6 TRMA.
- [x] Ajouter les diagnostics STOP / FINAL / LETTER du score sans changer la formule.
- [x] Passer le candidat à 1.0.3 / versionCode 103.
- [x] Étendre l'inspection CI aux cinq vidéos et ajouter une validation du main généré.
- [ ] Vérifier le résultat du workflow sur le commit candidat `d547fb9315f1432f2b5cda4417340fda67abacc5`.
- [ ] Si échec : corriger uniquement la première erreur discriminante sans toucher à la chaîne native.
- [ ] Si build vert : relever run, commit construit, APK, SHA-256, ABI/signature et artefacts.
- [ ] Contrôler les métadonnées ffprobe/SHA-256 et captures début/milieu/fin des cinq vidéos.
- [ ] Fab : valider sur téléphone les cinq scènes, les touches R/B et jaunes, les victoires 8/9 et le maintien de 10/11.
- [ ] Fab : vérifier les limites 40/40.5, 60/60.5 et 80/80.5, humain et IA.
- [ ] Fab : fournir logs/captures des scénarios score déterministes.
- [ ] Seulement si les mesures le prouvent : appliquer la correction géométrique minimale du centre de fenêtre.
- [ ] AAB 📦 après stabilisation de l'APK.



## 2026-09-30 — JT-MEDIA-POWER-SCORE-001 — après run #32

- [x] Coder les cinq scènes de combat selon indexa 1 / 2-4 / 5-7 / 8 / 9.
- [x] Conserver 10/11 historiques.
- [x] Combat aspect-fill muet ; intros aspect-fit avec audio.
- [x] Protéger les callbacks par lecteur + génération et conserver un seul lecteur de scène.
- [x] Conserver JPEG historiques comme fallback.
- [x] Appliquer `POWER_COSTS={1:60,2:40,3:60,4:60,5:60,6:80}`.
- [x] Utiliser strictement énergie `> coût`, jamais `>=`.
- [x] Partager la même règle entre UI, tactile, IA, débit et disponibilité sonore.
- [x] Corriger verrou sonore droit et identité visuelle TRFS/TRMA.
- [x] Ajouter diagnostics score STOP / FINAL / LETTER sans modifier le score.
- [x] Inspecter les cinq MP4 et produire captures début/milieu/fin.
- [x] Build Android run #32 vert au commit code `7f83389086ebe847007ddd48e506157ae41f74ad`.
- [x] Produire APK 1.0.3 / versionCode 103.
- [x] Vérifier APK : SHA-256 `48de9d70a2a6b03f641ff001973e782e7d56e8ec1d9e367c624ca4af85a73fdb`, 319081968 octets, Android Debug, deux ABI.
- [ ] Fab : installer l'APK 1.0.3 sur téléphone.
- [ ] Fab : valider scènes 1 / 2-4 / 5-7 / 8 / 9 et confirmer que 10/11 restent historiques.
- [ ] Fab : valider touches rouge/bleu et jaune aux bons seuils anim1.
- [ ] Fab : tester humain et IA à 40/40,5 ; 60/60,5 ; 80/80,5.
- [ ] Fab : tester deux taps rapides et recharge après slot déjà utilisé.
- [ ] Fab : fournir logs/captures score déterministes A-F.
- [ ] Seulement si les mesures le prouvent : appliquer la correction géométrique minimale de la fenêtre-cible.
- [ ] Ne pas merger main ni publier de release sans validation Fab.


## 2026-09-30 — JT-MEDIA-AUDIO-001 — audio natif des vidéos de combat

- [x] Coder la bascule audio native MP4 au premier frame utilisable.
- [x] Conserver `ma/sona` comme fallback avant frame et en cas d'échec média.
- [x] Empêcher `anim_1` de relancer le son historique pendant une vidéo active.
- [x] Arrêter explicitement l'audio du lecteur lors d'une sortie de scène.
- [x] Passer le candidat à 1.0.4 / versionCode 104.
- [ ] Vérifier le workflow Android du commit audio.
- [ ] Fab : tester les cinq scènes avec son MP4, absence de doublage et absence de son résiduel.
- [ ] Fab : tester plusieurs boucles indexa 1 et pause/reprise.


## 2026-10-01 — JT-MEDIA-ADMIN-001 — diagnostic des sources d'animation

- [x] Ajouter le voyant bas-gauche vert=MP4 réel / rouge=legacy-fallback.
- [x] Ajouter l'ouverture admin par 20 taps bas-droite.
- [x] Afficher indexa, MP4 présent/raccordé, dossier/prefix legacy, frames, mode et son.
- [x] Exposer namea/longanim1/genrea/sona au contrôleur média.
- [x] Passer le candidat diagnostic à 1.0.5 / versionCode 105.
- [x] Validation Python/CI de préparation et des hooks admin sur le run #40.
- [ ] Attendre la fin du build APK du run #40.
- [ ] Fab : relever les lignes rouges/LEGACY correspondant aux jauges à remplacer.


## 2026-10-01 — JT-POWER-VIDEOS-001 — six pouvoirs vidéo + charge corrigée

- [x] Identifier les 7 nouveaux MP4 déposés sur main.
- [x] Fixer le mapping 21 STSF Sanctuary / 22 STLS Lifestream / 23 STTA Tornado / 24 TRFS FireStorm / 25 TRPH Phoenix / 26 TRMA Meteor.
- [x] Préparer le raccordement de Chargestegtrexchargerougebleucorrected.mp4 pour 2/3/4.
- [x] Forcer les six auras sur jt_power_available(slot), identique à la lançabilité réelle.
- [x] Ajouter le nom du répertoire legacy au-dessus du voyant rouge lorsque le mode 20 touches est activé.
- [ ] Vérifier ffprobe/frames des 7 nouveaux MP4 dans CI.
- [ ] Vérifier compilation Android et produire June-T-Rex-1.0.6-debug.apk.
- [ ] Fab : tester les six pouvoirs, la charge corrected, les auras et le diagnostic 20 touches sur téléphone.


### CI #41 / #42
- [x] Run #41 : préparation réussie ; échec uniquement sur un ancien token de texte du test admin, avant Buildozer.
- [x] Corriger le garde-fou CI obsolète sans modifier le code fonctionnel.
- [x] Run #42 : préparation historique + compilation Python + validation média/audio/pouvoirs/auras réussies.
- [x] Run #42 : inspection FFprobe des 7 nouveaux MP4 et build APK 1.0.6 terminés avec succès.


## 2026-10-02 — JT-CINEMATIC-FINISHING-001 — lecture complète, auras tournantes, protection orbes

- [x] Faire jouer intégralement les six vidéos de pouvoirs.
- [x] Raccorder état 10 à StegFinishingTheTrex et état 11 à TrexFinishingTheSteg.
- [x] Corriger l'aura : b1s..b6s / select0..15, pas les icônes de pouvoir.
- [x] Aura visible uniquement si jt_power_available(slot).
- [x] Empêcher le tap de lancement de charge de figer un orbe.
- [x] Protéger les arrêts tactiles d'orbes pendant 2 secondes après la charge.
- [x] Masquer les voyants diagnostic tant que le mode 20 taps n'est pas activé.
- [x] Run #48 : préparation/CI/FFprobe des finishing et du candidat 1.0.7 terminés ; candidat ensuite rejeté par audit sémantique du verrou orbes.
- [x] Build APK 1.0.7 réussi au run #48 ; ne pas remettre à Fab comme candidat final à cause du défaut de protection orbes détecté après CI.
- [ ] Fab : tester les six pouvoirs jusqu'à EOS, les deux finishing, les auras tournantes, la protection orbes et le mode admin.


## 2026-10-02 — JT-ORB-PROTECT-002 — 1.0.8

- [x] Auditer le main généré 1.0.7 et identifier la garde d'arrêt humain inversée.
- [x] Confirmer la transition historique de début : Start indexa 0 → charge 4 → fin 1x → indexa 1 + colstop remis à False.
- [x] Armer les 2 s uniquement sur sortie charge 2/3/4 → phase orbes 1 avec Clock réel.
- [x] Figer réellement les positions pendant 2 s.
- [x] Bloquer les stops IA et humains pendant ces 2 s.
- [x] Suspendre car2 et car pendant la fenêtre afin de ne pas consommer le temps de jeu.
- [x] Conserver taps de charge, dégâts, score, pouvoirs et chaîne Android historiques.
- [x] Renforcer CI avec tests sémantiques Clock et interdiction de l'ancienne garde.
- [x] Run #49 entièrement vert ; APK 1.0.8 / versionCode 108 produit.
- [x] SHA-256 APK : a27dfb9e49e11803ca006a0fb9307a47d7d15f9eb78fd3b8e9dd76667db7523b.
- [ ] Fab : valider sur téléphone le gel réel 2 s, l'absence de stop humain/IA durant la fenêtre, puis le retour normal du contrôle.
- [ ] Fab : valider sur téléphone les six pouvoirs jusqu'à EOS, les deux finishing, les auras tournantes et le mode admin 20 taps.


## 2026-10-02 — JT-FINISH-EOS-002 — 1.0.9

- [x] Reproduire par audit la coupure des finishing malgré `play_to_end`.
- [x] Identifier la sortie legacy 10/11 à `longanim1[indexa]-3`.
- [x] Comparer durée legacy état 11 (~6,24 s) au MP4 T-Rex finishing (8,336 s).
- [x] Conserver fallback historique tant qu'aucune première frame vidéo n'est exploitable.
- [x] Geler uniquement les états finishing 10/11 dès la première vraie frame MP4.
- [x] Faire de l'EOS MP4 l'unique libération vers le menu quand la vraie vidéo a pris la main.
- [x] Éviter le redémarrage du même finishing après EOS.
- [x] Ne pas modifier les pouvoirs 21..26, dégâts, score ou chaîne native.
- [x] CI #50 : génération + compilation Python + tests sémantiques finishing EOS verts.
- [x] CI #50 : FFprobe des médias verts.
- [ ] CI #50 : build APK 1.0.9 complet / artifact à confirmer.
- [ ] Fab : vérifier sur téléphone que les deux finishing sont visibles et audibles jusqu'à leur toute dernière image/son.

## 2026-10-02 — JT-PHASES-001 — état courant, candidat 1.0.12/code112

Les sections antérieures conservent l'historique.

- [x] Auditer branche e60561d, main historique vérifié/généré, écrivains UI, timers et contrôleur média.
- [x] Reproduire HUD parasite, chrono pré-round et redémarrage pouvoir court.
- [x] Ajouter phases, ROUND N/START!, chrono unique et cinématiques exclusives; conserver jauges interactives.
- [x] Corriger car2 lors du lancement IA, sans changement de coût/probabilité/effet.
- [x] 16 tests sur moteur généré/IO simulées; compilation Python et assertions code/helpers existantes vertes.
- [x] Préserver chaîne native/médias/pruning/score/coûts/auras/admin; traces audio ciblées ajoutées.
- [ ] Obtenir build CI et consigner commit/run/SHA256 APK; aucune release ni merge main.
- [ ] Fab : charge rouge/bleu interactive, puis VV/vies/deux chronos figés, ROUND1 jaune~1s, START! animé; aucun tick avant sa fin.
- [ ] Fab : égalité jaune interactive puis ROUND2 au prochain échange; aucun nouveau ROUND au simple retour de pouvoir.
- [ ] Fab : six pouvoirs sans UI/chrono/orbes actifs avant EOS; noter car/car2 avant/après. Humain/IA et seuils40/40,5;60/60,5;80/80,5, selected.
- [ ] Fab : pouvoir fatal ST puis TR, pouvoir intégral → bon finishing intégral sans HUD → menu unique.
- [ ] Fab : VV reprise proche de sa position, boucle naturelle; pause/reprise pendant START et pouvoir.
- [ ] Fab : rendu/ratios, audio MP4, admin20taps.
- [ ] Doublon vocal : capture et traces JT-PHASE/JT-SCENE (fichier/génération/EOS/position/durée/AUDIO_LEGACY/AUDIO_NATIVE), attribuer seulement après preuve.

### JT-PHASES-001 — complément canvas et nettoyage tactile

- [x] Masquer/restaurer aussi les géométries canvas directes, test reproduit avant correction.
- [x] Conserver le nettoyage historique de on_touch_up pendant cinématique; test dédié vert.
- [x] 18 tests déterministes verts.
- [ ] Suivre le build du commit complémentaire; ne pas livrer le premier candidat df03316/run54 comme résultat final.
