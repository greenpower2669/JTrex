# JTrex / June T-Rex — Ordres de mission

## ODM-JTREX-001 — Reconstruction documentaire avant portage Android

### Statut

MISSION DOCUMENTAIRE.

Cette mission crée la mémoire durable du projet. Elle ne constitue pas une autorisation de modifier le jeu.

### Autorité et rôles

Fab dirige le projet et valide le comportement sur téléphone.

La reconstruction fonctionnelle fournie par Astra sert de source documentaire pour la transcription dans :

- brain.md ;
- brainmap.md ;
- debughistorical.md ;
- todo.md ;
- ordres-de-mission.md.

Le travail doit respecter l'esprit FAB Copilot et le protocole FAB Human Sol Slaves : préserver l'intention de Fab, transmettre une connaissance vérifiable, distinguer ce qui est observé de ce qui est supposé, et ne pas transformer une mission documentaire en correction autonome.

### Références

Dépôt :
https://github.com/greenpower2669/JTrex

Révision main :
164d03be77c83f49e1094294f36f860ec183df68

Release :
https://github.com/greenpower2669/JTrex/releases/tag/JTrex

Archive :
https://github.com/greenpower2669/JTrex/releases/download/JTrex/JuneTrex.zip

Programme de référence :
JuneTrex/main.py

SHA-256 :
3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231

Le main.py de « June air hockey » n'est pas la référence JTrex.

### Objectif fonctionnel à mémoriser

JTrex est un jeu d'adresse compétitif à deux camps avec :

- trois orbes rouge/vert/bleu par camp ;
- arrêt des orbes par trois boutons de couleur ;
- comparaison de précision ;
- séquences de dinosaures image par image ;
- confrontations spéciales au tapotement ;
- vie ;
- énergie ;
- trois pouvoirs par camp ;
- modes humain/ordinateur indépendants ;
- cinq niveaux indépendants ;
- deux chronomètres ;
- états de fin et retour menu.

La référence exacte des règles et formules est dans brain.md.
La localisation technique de ces règles est dans brainmap.md.

### Objectif futur

Préparer à terme un portage Android propre et installable.

Ce futur portage devra d'abord reproduire le comportement historique validé avant toute simplification.

Livraison future attendue, lorsque Fab l'autorisera :

- nom/version cohérents ;
- icône Android ;
- APK installable 📦 ;
- AAB séparé si nécessaire pour la diffusion 📦.

### Souhait futur médias

Fab souhaite retrouver les vidéos originales et remplacer plus tard les séries d'images par de vraies vidéos.

Ce souhait est reporté.

Interdictions actuelles :

- ne pas rechercher activement ces vidéos dans cette mission ;
- ne pas convertir les JPEG en vidéos ;
- ne pas supprimer les séries ;
- ne pas modifier les timings ;
- ne pas fusionner des embranchements ;
- ne pas inventer une vidéo de remplacement.

### Interdiction de coder

Pendant ODM-JTREX-001 :

- aucune modification de main.py ;
- aucune modification de main.kv ;
- aucune modification de buildozer.spec ;
- aucune modification du workflow Android ;
- aucune modification de ressource ;
- aucune correction des observations JT-OBS ;
- aucun build ;
- aucun déploiement ;
- aucune publication de release.

Seuls les fichiers documentaires du cerveau du projet peuvent être créés ou mis à jour.

### Mémoire obligatoire

brain.md doit décrire le jeu et ses règles.

brainmap.md doit expliquer où ces règles se trouvent et comment elles s'enchaînent techniquement.

debughistorical.md doit conserver les anomalies et incertitudes sans les déclarer corrigées.

todo.md doit décrire l'état réel, les validations à faire et le prochain geste.

Aucune mémoire antérieure ne doit être écrasée silencieusement lors des mises à jour futures. En cas de divergence de référence, conserver l'historique et signaler explicitement la nouvelle source.

### Organigrammes obligatoires

La brainmap doit conserver des diagrammes distincts pour :

1. menu et cycle complet ;
2. arrêt des orbes et comparaison ;
3. embranchements rouge/bleu ;
4. embranchements jaunes ;
5. disponibilité/utilisation/effet des pouvoirs ;
6. fin de combat et retour menu.

Ces schémas doivent représenter le programme actuel, y compris ses exceptions. Ils ne doivent pas remplacer la réalité par un comportement idéal.

### Registre d'observations

JT-OBS-001 à JT-OBS-026 sont des observations documentaires.

Certaines asymétries peuvent être volontaires. Une observation ne devient un bug à corriger qu'après validation de Fab.

### Passation

À la fin de cette mission documentaire :

- le cerveau fonctionnel existe ;
- la cartographie technique existe ;
- le registre des observations existe ;
- le TODO sépare documentation, validation et portage futur ;
- aucun code n'a été touché.

Toute phase suivante exige un nouvel ordre explicite de Fab.


### Contrôle de complétude documentaire

Après création initiale des mémoires, une relecture croisée avec le relais Astra a été effectuée pour vérifier la fidélité de transcription.

Les détails qui restaient implicites ont été rendus explicites dans brain.md et brainmap.md, notamment le suivi tactile choixidh/choixidb, colv[7..9], les limites exactes du hash et de l'inventaire, les variantes de ressources horseg2ko et certaines nuances de l'héritage tactile.

Ce contrôle reste strictement documentaire : aucun code, média, build, workflow ou comportement n'a été modifié.


## JT-ANDROID-001 — Premier APK installable de June T-Rex

### Statut
MISSION ACTIVE SUR BRANCHE DÉDIÉE — PHASE 1 : DOSSIER ASTRA.

Branche : `port/android-first-apk`
SHA de départ : `379ae278f2199cad26f1746c418512f47e04d106`

Objectif : produire un premier APK 📦 installable et fidèle au jeu historique, puis un AAB 📦 distinct si la chaîne le permet. La validation finale du gameplay appartient à Fab sur téléphone.

Rôles :
- Fab dirige, arbitre les changements de comportement et teste sur téléphone.
- Astra analyse les extraits/données ciblés et prépare les corrections nécessaires.
- Sol prépare les sources, applique les corrections validées, gère Git, build, livraison et mémoires.

Invariants : ne pas réécrire le jeu, ne pas rééquilibrer, ne pas moderniser globalement, ne pas ajouter d'IA de tapotement, ne pas remplacer les séquences par des vidéos et ne pas supprimer le moteur Air Hockey hérité sans preuve et ordre distinct.

Source de jeu : asset `JuneTrex.zip` de la release/tag `JTrex`, racine explicitement `JuneTrex`. Ne jamais dépendre de « latest » ni du premier `main.py` trouvé.

Adaptations autorisées : compatibilité Android, chemins/casse des ressources, configuration/workflow, identité/version/icône, diagnostics bornés et corrections ciblées d'un blocage Android démontré.

La branche ne doit pas être fusionnée automatiquement dans main avant retour de Fab.


### JT-ANDROID-001 — proposition Astra appliquée

La proposition Astra reçue après le commit de préparation `609c38b7c0994337fdc5bc22dbb519ff326ce5ec` est autorisée sur `port/android-first-apk`.

Elle ajoute le préparateur contrôlé, fige la source sur la release/tag `JTrex`, corrige uniquement les références de casse dans la copie de compilation, passe le candidat à 1.0.1, ajoute l'icône provisoire issue de `pter/pter0.png` et deux traces bornées de démarrage.

`horseg2ko/chargetrwin_83.jpeg` reste absente et aucune image n'est fabriquée.

La chaîne de compilation reste à qualifier après build ; aucune promesse de reproductibilité intégrale n'est faite tant que Buildozer/python-for-android ne sont pas verrouillés sur des révisions vérifiées.


### JT-ANDROID-001 — retour run #7

Le premier run ciblé a validé la préparation de JuneTrex mais a échoué avant création de l'APK dans la compilation native libffi/python-for-android.

Erreur discriminante :
`configure.ac:215: error: possibly undefined macro: LT_SYS_SYMBOL_USCORE`.

Aucune correction autonome de gameplay ou de main.py n'est autorisée en réponse à cet échec. Le prochain changement doit être une correction de chaîne ciblée préparée par Astra selon FAB-DEBUG-001.


### JT-ANDROID-001 — correction ciblée libltdl-dev

Astra autorise un essai FAB-DEBUG-001 unique : ajouter `libltdl-dev` aux dépendances Ubuntu du workflow. Aucun autre changement n'est inclus dans cet essai.

Succès attendu : disparition de l'erreur `LT_SYS_SYMBOL_USCORE` à l'étape `autoreconf` de libffi. Une erreur ultérieure éventuelle devient un blocage distinct.


### JT-ANDROID-001 — résultat essai libltdl-dev

L'essai FAB-DEBUG-001 n°1 est concluant pour son objectif : `LT_SYS_SYMBOL_USCORE` est franchi.

Le nouveau blocage est distinct et concerne le pip interne de python-for-android sous Python 3.14.2 :
`ImportError: cannot import name 'BuildDependencyInstallError' from 'pip._internal.exceptions'`.

La correction suivante doit rester mono-hypothèse et préparée par Astra. Aucun changement de gameplay ou de main.py n'est autorisé.


### JT-ANDROID-001 — essai ciblé p4a venv --clear

Astra autorise un second test FAB-DEBUG-001 mono-hypothèse : conserver le commit p4a `58d21141f17c889bf8585f5665921d72028f8831` et appliquer localement un patch ajoutant uniquement `--clear` à la création du venv dans `run_pymodules_install()`.

La mise à jour de pip interne reste volontairement inchangée. Aucun autre composant de chaîne, gameplay, main.py ou média n'est modifié dans cet essai.


### JT-ANDROID-001 — jalon APK atteint

Le run #9 a produit `JuneT-Rex-1.0.1-debug.apk` avec succès.

Statut : **APK compilé et contrôlé statiquement ; installation et fonctionnement à valider par Fab**.

Le fichier est signé avec un certificat Android Debug. Il ne constitue pas encore une version de distribution ni une validation du gameplay.

La prochaine validation appartient à Fab sur téléphone selon la fiche de test courte prévue par JT-ANDROID-001.


## JT-MEDIA-001 — Intros aléatoires, icône et premier essai vidéo

Mission autorisée par Fab sur `port/android-first-apk`.

Ressources source fournies sur `main` : `JtrexIcon.png`, `JTrexintro1.mp4`, `JTrexintro2.mp4`, `JTrexintro3.mp4`, `StegVsTrexvaetviensremolace.mp4`.

Contraintes structurantes :
- importer uniquement ces ressources, sans fusion de `main` ;
- ranger sous `assets/icon`, `assets/intro`, `assets/combat` ;
- une seule intro tirée uniformément au hasard par lancement d'application ;
- aucune relance d'intro par manche ou reprise ;
- conserver le son d'intro et éviter le chevauchement avec la musique du jeu ;
- utiliser `JtrexIcon.png` comme icône Android ;
- la vidéo Steg/T-Rex est lue normalement et boucle telle quelle, sans inversion temps réel ;
- ne remplacer qu'une attente historique clairement correspondante ;
- conserver score, dégâts, énergie, pouvoirs, timers, IA, tapotements et Air Hockey ;
- ne pas remplacer `horseg2ko/chargetrwin_83.jpeg` ;
- préserver les images historiques comme solution de repli ;
- validation réelle vidéo sur téléphone par Fab.

Phase actuelle : intake/inspection. Les médias sont importés dans la branche mais pas encore activés dans l'application.


### JT-MEDIA-001 — implémentation candidate 1.0.2

Version de test : `1.0.2`, versionCode `102`.

Décisions d'intégration :
- une intro aléatoire parmi trois, une seule fois par lancement ;
- intro en letterbox noir, audio original, touches absorbées et gameplay non planifié ;
- repli automatique vers le jeu en cas de lecture réellement indisponible ;
- icône Android `assets/icon/JtrexIcon.png` ;
- `StegVsTrexvaetviensremolace.mp4` affectée exclusivement à l'attente `indexa=1` ;
- lecture de cette vidéo en boucle normale, sans reverse calculé ;
- piste audio de l'attente vidéo muette afin de préserver la bande-son historique ;
- sortie de l'attente arrête/libère le lecteur sans attendre la fin du fichier ;
- gameplay, impacts, scores, énergie, IA et timers restent pilotés par le moteur historique ;
- JPEG historiques conservés comme fallback.

La chaîne vidéo candidate utilise ffpyplayer 4.5.1 avec la recette FFmpeg 6.1.2 de p4a historique, à confirmer par build réel avant toute déclaration de compatibilité téléphone.


### JT-MEDIA-001 — correction ciblée après run #11

Le run #11 démontre un blocage natif ffpyplayer 4.5.1 / Python 3.14.2. La correction suivante ne modifie ni le runtime JTrex ni les médias : elle fixe uniquement python3 et hostpython3 à 3.11.13 tout en gardant le p4a `58d2114…`, `venv --clear`, FFmpeg 6.1.2, NDK r28c et les deux architectures.

Critère de réussite : ffpyplayer compile sans les erreurs d'API CPython 3.14 et le build poursuit vers l'APK.


## 2026-09-28 — FAB-DEBUG-001 / JT-MEDIA-001

Appliquer un seul essai fonctionnel : Python 3.12.14 pour `python3` et `hostpython3` dans `buildozer.spec`. Ne modifier ni ffpyplayer 4.5.1, ni FFmpeg 6.1.2, ni p4a, ni le runtime/médias/gameplay. Relancer le workflow proprement. Si un blocage antérieur à ffpyplayer apparaît, rapporter ce blocage seul et ne pas empiler de seconde correction.


### Clôture du run #13

Le test FAB-DEBUG-001 est **incomplet** : la préparation s'arrête avant p4a sur une assertion héritée imposant Python 3.11.13. Aucun second patch n'est autorisé dans ce run. Le prochain ordre de mission devra traiter explicitement cette garde s'il veut poursuivre le test 3.12.14.


### 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — alignement préparation Python 3.12.14

Astra autorise la suite du run #13 sous forme d'un essai séparé : modifier uniquement les quatre occurrences prévues dans `tools/prepare_android.py` afin d'aligner la garde et le rapport sur Python 3.12.14. Le contrôle reste actif. `buildozer.spec`, ffpyplayer 4.5.1, FFmpeg 6.1.2, le p4a figé, Cython, les médias, le runtime et le gameplay restent inchangés. Le prochain run doit mesurer la première erreur réelle sans empiler de correction.


### Clôture du run #14

L'alignement de préparation est validé, mais le test Python 3.12.14 / ffpyplayer reste incomplet : la compilation s'arrête d'abord dans CPython 3.12.14 pour `armeabi-v7a`, `Modules/grpmodule.c`, sur `setgrent/getgrent/endgrent`. Aucun second correctif ne doit être empilé. Astra doit recevoir ce blocage avec la note que p4a demande/télécharge hostpython3 3.12.14 alors que le workflow exporte encore une variable héritée `VERSION_hostpython3=3.11.13`.


### 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — grp Android API 21

Astra autorise un essai mono-hypothèse supplémentaire : conserver Python 3.12.14 et toute la chaîne actuelle, mais déclarer le module `grp` indisponible uniquement dans la recette `python3` Android lorsque `ndk_api < 26`. Le mécanisme est versionné dans `tools/patches/p4a-python312-grp-api21.patch` et appliqué par le workflow après le patch venv. Le hostpython3 Linux, l'export historique VERSION_hostpython3, ffpyplayer, FFmpeg, p4a, Cython, API/NDK, architectures, médias, runtime et gameplay restent inchangés. Aucun second correctif ne doit être ajouté au prochain run.


### Clôture du run #15

Le correctif ciblé `grp` est validé pour son objectif : la cible Android armeabi-v7a configure `grp` à `n/a` et dépasse le blocage CPython du run #14. Le nouveau blocage apparaît ensuite dans FFmpeg 6.1.2 pendant la compilation Vulkan pour armeabi-v7a, première erreur sur `libavcodec/vulkan_av1.c:183` lors de l'initialisation d'un `VkVideoSessionParametersKHR` avec `NULL`. La commande configure contient `--enable-hwaccels`. Aucun correctif supplémentaire n'est autorisé dans cette tentative ; Astra doit analyser ce nouveau blocage. ffpyplayer n'a pas encore été réellement compilé et arm64-v8a n'est pas atteint.


### 2026-09-28 — JT-MEDIA-001 — exclusion Vulkan FFmpeg 6.1.2

Astra autorise un nouvel essai mono-hypothèse : ajouter uniquement `--disable-vulkan` à `tools/p4a-ffmpeg-6.1.2.py`, immédiatement après `--enable-hwaccels`. Tous les autres éléments de la chaîne et les correctifs déjà validés sont conservés. Aucun patch Vulkan supplémentaire, aucune mise à jour FFmpeg et aucune désactivation générale des accélérations matérielles ne doivent être ajoutés dans cette tentative. Le prochain run doit relever le résultat réel de FFmpeg, puis seulement de ffpyplayer s'il est atteint.


### Clôture du run #16
L'essai `--disable-vulkan` est concluant : FFmpeg 6.1.2 et ffpyplayer 4.5.1 passent sur les deux architectures et le workflow produit `JuneT-Rex-1.0.2-debug.apk`. SHA-256 : `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a`. La validation runtime reste à Fab sur téléphone.


### JTREX — diagnostic du premier crash sur téléphone

Ordre Astra reçu : diagnostic uniquement. L'APK testé est identifié comme le 1.0.2 debug du run #16, SHA-256 `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a`. Le retour Fab est « logo Kivy puis fermeture ». Aucun accès ADB au téléphone n'est disponible dans cette session et aucune reproduction n'est revendiquée. La prochaine preuve obligatoire est un logcat complet du lancement permettant de déterminer le dernier marqueur JT et la première erreur fatale. Aucune modification Python/FFmpeg/Cython, gameplay ou média n'est autorisée avant cette preuve.


### Retour diagnostic bugreport téléphone — crash 1.0.2

Le bugreport Samsung confirme que l'application ne parvient pas jusqu'au code JTrex. Sur SM-A576B / Android 16 / arm64-v8a, Python-for-Android atteint `_python_bundle dir exists` puis `set wchar paths...` et échoue avec `Python initialization failed: failed to get the Python codec of the filesystem encoding`. Aucun marqueur JT n'est émis. L'archive `stdlib.zip` de l'APK contient pourtant `encodings` et `codecs.pyc`. Diagnostic uniquement ; aucune correction appliquée. Astra doit décider de la prochaine hypothèse de chaîne Python/p4a.


### 2026-09-28 — FAB-DEBUG-001 — diagnostic bootstrap Python

Astra autorise uniquement un patch diagnostique du bootstrap p4a figé. Le bugreport existant ne révèle pas l'exception sous-jacente, donc `tools/patches/p4a-python312-bootstrap-exception-diag.patch` journalise les paramètres de bootstrap et capture immédiatement l'exception en attente lors de l'échec Py_InitializeFromConfig. La chaîne du run #16, les chemins, le bundle, main.py, FFmpeg, Cython, médias et gameplay restent inchangés. Le livrable de cette tentative est un APK de diagnostic, pas une correction de runtime.


### Run #17 — correction de forme du patch diagnostique

Le run #17 s'est arrêté sur `git apply --check` avant toute compilation. Cet arrêt ne constitue pas un test du bootstrap Python. La correction autorisée dans la continuité de cette même mission est limitée aux en-têtes de hunks du patch diagnostique ; son contenu fonctionnel reste identique.


### Run #18 — livrable diagnostique disponible

Le run #18 (ID `36410518782`) sur le commit `7fa5e4bd32ae02dbe88b8eb74e04e73b0a834986` compile le patch diagnostique Astra pour les deux architectures et produit un APK. SHA-256 : `fbc4a1d0f72cf677591e4a4ffb366db9237377c5f5c3574d6f7ca025249d8e64`. Ce livrable reste strictement diagnostique : la prochaine étape est le lancement sur le téléphone de Fab suivi d'un nouveau rapport complet afin de récupérer l'exception sous-jacente. Aucun correctif de cause racine n'est encore autorisé.


### Retour bugreport diagnostique run #18 — cause immédiate établie

Le patch diagnostique a rempli son objectif. Le téléphone expose désormais l'exception réelle : `ZipImportError: can't decompress data; zlib not available`, causée par l'échec de chargement de `zlib.cpython-312.so` avec `dlopen failed: cannot locate symbol "PyExc_MemoryError"`. Le bundle et les chemins sont présents et lisibles.

Inspection ELF complémentaire : `libpython3.12.so` exporte le symbole, `zlib.cpython-312.so` le référence comme non résolu et ne déclare pas `libpython3.12.so` en DT_NEEDED. Aucun correctif n'est appliqué. Astra doit déterminer la prochaine correction mono-hypothèse de liaison/chargement Python sur Android.


### 2026-09-28 — FAB-DEBUG-001 — visibilité globale de libpython

Astra autorise un seul changement fonctionnel : ajouter `-Wl,-z,global` à la liaison de `libpython3.12.so` via un patch spécifique à la recette python3 cible 3.12.14. Le contrôle préalable du run #18 confirme que `DT_FLAGS_1` contient `NOW` mais pas `GLOBAL` sur les deux ABI. Le libpython testé ne présente pas de DT_SONAME explicite ; ce fait est conservé sans correction hors périmètre. Aucun autre composant de chaîne, média ou gameplay ne change.


### Run #19 — preuve statique de DF_1_GLOBAL

Le run #19 (ID `36437050585`) sur le commit `e0c374fe7f436ea12ef07a9676916033cd5f6fcf` produit un APK où libpython3.12.so possède `FLAGS_1: NOW GLOBAL` sur arm64-v8a et armeabi-v7a. `PyExc_MemoryError` reste exporté. SHA-256 : `945f795bce1b925ac981df48bbd3781d73d5816927ef4356ce00e2875068a241`.

Le DT_SONAME explicite reste absent comme au run #18 et n'est pas modifié dans cette mission. L'hypothèse GLOBAL est correctement matérialisée ; la prochaine étape est uniquement le test téléphone. Si une erreur subsiste, rapporter la première nouvelle erreur sans ajouter un second correctif.

## 2026-09-30 — JT-MEDIA-POWER-SCORE-001 — ordre canonique Fab

Mission active sur `port/android-first-apk`. Base fonctionnelle initiale `a6caa620e51281d4a2a8dc854830f15b5db66c7b`. Préserver intégralement la chaîne native actuellement fonctionnelle.

Médias : indexa 1 = attente `StegVsTrexvaetviensremolacebisorigune.mp4`; 2/3/4 = confrontation rouge/bleu ; 5/6/7 = égalité bouton jaune ; 8 = victoire échange ST ; 9 = victoire échange TR. Les états 10/11 restent historiques. Combat en aspect-fill et muet ; intros intégrales en aspect-fit avec audio.

Pouvoirs : source unique `POWER_COSTS={1:60,2:40,3:60,4:60,5:60,6:80}`. Condition canonique : phase autorisée ET slot non utilisé ET énergie strictement supérieure au coût. Ne jamais convertir en `>=`. L'énergie fractionnaire et ses gains historiques sont conservés.

Score : instrumentation seulement dans ce lot. Conserver formule cubique, `haut[7]`, seuil strict d'égalité <20000 et lettres. Ne corriger la géométrie qu'après preuve téléphone.

Candidat de code/CI à tester : version 1.0.3, versionCode 103, commit `d547fb9315f1432f2b5cda4417340fda67abacc5`. Ne pas confondre push Git, succès CI, APK produit et validation téléphone.



## 2026-09-30 — ASTRA → SOL — JTREX — AVENANT CANONIQUE JT-POWERS-COSTS

Cet avenant remplace les sections « coûts à définir », la condition `>=` et les tests correspondants de l'ordre précédent.

### 1. Coûts approuvés par Fab

```python
POWER_COSTS = {
    1: 60,  # ST1 — état 21
    2: 40,  # ST2 — état 22, soin
    3: 60,  # ST3 — état 23
    4: 60,  # TR1 — état 24
    5: 60,  # TR2 — état 25
    6: 80,  # TR3 — état 26
}
```

Aucun coût ne reste à déterminer.

### 2. Condition canonique

Un pouvoir est utilisable si :
- la phase autorise son utilisation ;
- son slot n'a pas déjà été utilisé ;
- énergie > POWER_COSTS[slot].

Employer strictement `>`, jamais `>=`.

L'énergie historique peut être fractionnaire. Ne pas la convertir en entier et ne pas modifier ses gains.

Exemple : `40,5 > 40` autorise le soin. Après débit, énergie = `0,5`.

### 3. Application commune

Utiliser cette source unique pour :
- disponibilité visuelle ;
- bonus/select ;
- activation tactile ;
- activation IA ;
- débit énergétique ;
- indication sonore de disponibilité.

Revérifier énergie, phase et `selected` au déclenchement réel. Un indicateur visuel précédemment activé ne suffit pas.

Débiter exactement le coût une seule fois. Marquer `selected` et conserver l'interdiction de réutilisation du même slot pendant le combat.

Conserver la décision probabiliste historique de l'IA : être éligible ne signifie pas déclencher obligatoirement.

Auditer les anciens seuils `>60` associés aux pouvoirs. Ne pas remplacer indistinctement tous les nombres 60 du jeu.

Le clignotement à 100 reste un rappel de réserve pleine, indépendant de la disponibilité de chaque pouvoir.

### 4. Tests des limites

Pour chaque slot, avec les autres conditions satisfaites :

Coût 40 :
- énergie 40 : refus ;
- énergie 40,5 : autorisation, reste 0,5 ;
- énergie 41 : autorisation, reste 1.

Coût 60 :
- énergie 60 : refus ;
- énergie 60,5 : autorisation, reste 0,5 ;
- énergie 61 : autorisation, reste 1.

Coût 80 :
- énergie 80 : refus ;
- énergie 80,5 : autorisation, reste 0,5 ;
- énergie 81 : autorisation, reste 1.

Vérifier humain, IA et affichage. Un refus ne doit consommer aucune énergie ni marquer `selected`.

Tester aussi :
- slot déjà utilisé malgré une recharge suffisante ;
- deux appuis rapides : une seule consommation ;
- disponibilités distinctes selon les coûts ;
- aucune énergie négative.

Mesurer le débit immédiatement après activation, séparément des gains historiques liés aux impacts ultérieurs.

### 5. Périmètre et livraison

Ce patch modifie uniquement les coûts et leurs conditions cohérentes d'utilisation et d'affichage.

Conserver effets, soin, dégâts, gains d'énergie, score, vidéos, timers et chaîne native Android.

Appliquer sur la branche active. Actualiser les mémoires et l'ordre de mission :
- ST = 60 / 40 / 60 ;
- TR = 60 / 60 / 80 ;
- condition = énergie strictement supérieure au coût.

Lancer les tests ciblés puis le workflow Android existant pour construire le nouvel APK, sans modifier cette chaîne.

Livrer :
📦 `JuneT-Rex-<version>-debug.apk`
avec l'icône JTrex existante, versionCode, commit, run, SHA-256 et lien de téléchargement.

Distinguer tests réussis, APK produit et validation sur le téléphone de Fab.

### État réel obtenu au 2026-09-30

- Code média/énergie/diagnostic score : présent sur la branche et vérifié par CI.
- HEAD code construit : `7f83389086ebe847007ddd48e506157ae41f74ad`.
- Workflow Android : run #32 / ID `36753181725`, succès.
- Workflow inspection média : run #11 / ID `36753181720`, succès.
- APK : `JuneT-Rex-1.0.3-debug.apk`.
- version : `1.0.3`.
- versionCode : `103`.
- ABI : `arm64-v8a` + `armeabi-v7a`.
- Signature : Android Debug.
- Taille APK : `319081968` octets.
- SHA-256 APK : `48de9d70a2a6b03f641ff001973e782e7d56e8ec1d9e367c624ca4af85a73fdb`.
- Les cinq vidéos sont incluses dans `assets/private.tar` de l'APK avec leurs SHA-256 attendus.
- Les diagnostics contiennent les captures début/milieu/fin des cinq scènes.
- Aucune correction géométrique du score n'est appliquée : elle reste conditionnée à la preuve téléphone.
- Validation téléphone des médias, limites d'énergie et géométrie du score : encore à faire par Fab.


## 2026-09-30 — JT-MEDIA-AUDIO-001 — audio natif des vidéos de combat

Avenant canonique Fab : pour les scènes vidéo indexa 1, 2/3/4, 5/6/7, 8 et 9, la piste audio native du MP4 doit être utilisée dès la première frame vidéo exploitable. Le son historique de scène reste actif tant que la vidéo n'a pas fourni de frame, puis il est arrêté afin d'éviter tout doublage. En cas d'échec média après activation, le fallback restaure le son historique correspondant. Les états 10/11 restent entièrement historiques. Les intros conservent leur audio actuel. Aucun événement audio ne pilote le gameplay. Candidat : 1.0.4 / versionCode 104.


## 2026-10-01 — JT-MEDIA-ADMIN-001 — diagnostic des sources d'animation

Outil de repérage demandé par Fab avant le prochain rapport ASTRA. Vingt taps consécutifs dans les 12 % bas-droite ouvrent un menu administratif média. Le menu doit lister chaque indexa connu, le MP4 raccordé et présent lorsqu'il existe, sinon l'animation historique, ainsi que le répertoire/prefix legacy exact, le nombre de frames, le mode et le son. Pendant le jeu, un petit point clignotant bas-gauche est vert lorsque le rendu réellement affiché est un MP4, rouge lorsque le rendu est historique/fallback. Diagnostic uniquement : aucun effet gameplay. Candidat 1.0.5 / versionCode 105.


## 2026-10-01 — JT-POWER-VIDEOS-001 — six pouvoirs vidéo + charge corrigée

Décision Fab : intégrer les six vidéos de pouvoirs fournies sur main sans merger main, en réutilisant leurs blobs sur port/android-first-apk. Mapping canonique : état 21 / STSF = Sanctuary Force ; 22 / STLS = Lifestream ; 23 / STTA = Tornado Attack ; 24 / TRFS = Fire Storm ; 25 / TRPH = Phoenix Attack ; 26 / TRMA = Meteor Attack (coût 80, la plus chère). La montée rouge/bleu états 2/3/4 doit utiliser la vidéo corrigée Chargestegtrexchargerougebleucorrected.mp4. Toutes les vidéos gardent le moteur historique comme autorité et fallback, audio MP4 natif après première frame exploitable. Les auras des six pouvoirs doivent être visibles si et seulement si jt_power_available(slot) est vrai. En mode admin 20 touches, quand le voyant est rouge, afficher au-dessus le répertoire legacy courant.


## 2026-10-02 — JT-CINEMATIC-FINISHING-001 — lecture complète, auras tournantes, protection orbes

Décisions Fab : les vidéos des pouvoirs 21..26 doivent être lues intégralement, même si le moteur historique change d'état avant leur fin. Les deux finishing sont ajoutés : état 10 = StegFinishingTheTrex, état 11 = TrexFinishingTheSteg. Le moteur historique reste autorité pour dégâts/états ; EOS vidéo ne crée aucun dégât ni transition. Les touches gameplay sont absorbées tant qu'une cinématique play-to-end couvre l'écran. La charge initiale ne doit jamais figer un orbe avec le même tap : le tap parti de l'état 1 ne peut activer aucun colstop et les arrêts tactiles d'orbes sont ensuite protégés 2 secondes. L'aura demandée est l'overlay tournant b1s..b6s utilisant select/select0..15.png, pas les icônes de pouvoir b1..b6 ; son affichage doit être strictement jt_power_available(slot). Les voyants rouge/vert et le libellé legacy restent invisibles jusqu'à activation du mode admin par 20 taps.


## 2026-10-02 — JT-ORB-PROTECT-002 — correction de la protection de charge

Le candidat 1.0.7 ne doit pas être considéré comme final : audit du main généré après le run #48 a démontré une garde inversée sur les arrêts humains et l'absence de gel physique des orbes. Décision appliquée en 1.0.8 : à la fin d'une charge historique 2/3/4 entrant en indexa 1, armer exactement 2,0 s via `Clock.get_time()`. Pendant cette fenêtre, aucune position d'orbe ne bouge, aucun stop IA ou humain n'est accepté et les timers `car2` / `car` sont suspendus. Ne pas bloquer les taps de confrontation hors phase 1 et ne pas modifier score/dégâts/règles de pouvoir. La chaîne native reste inchangée. Run #49 du SHA 865591a8d9518d9da26533ec403c6794fc1d4fd2 : success complet ; APK 1.0.8 SHA-256 a27dfb9e49e11803ca006a0fb9307a47d7d15f9eb78fd3b8e9dd76667db7523b. Aucun merge main, aucune release. Validation téléphone Fab obligatoire avant de déclarer le lot validé en usage réel.


## 2026-10-02 — JT-FINISH-EOS-002 — finishing jusqu'au vrai EOS

Retour Fab : les vidéos finishing des états 10/11 doivent être visibles et jouées intégralement. La transition historique JPEG `longanim1-3 -> indexa 0` ne doit plus être autorisée à interrompre un MP4 ayant fourni sa première frame. Règle : avant première frame ou échec vidéo = fallback historique inchangé ; après première frame = état 10/11 maintenu sans progression legacy ; à EOS MP4 réel = libération unique vers le menu sans seconde application de gameplay et sans queue JPEG. Les pouvoirs restent selon leur contrat play-to-end existant et ne doivent pas hériter de ce gel finishing spécifique. Candidat : 1.0.9 / versionCode 109, run #50.

## 2026-10-02 — JT-PHASES-001 — ordre actif de Fab, candidat 1.0.12

Cet ordre complète les missions historiques. Fab autorise explicitement Astra à auditer le code public puis corriger `port/android-first-apk`; ce n'est plus le seul relais documentaire Astra → Sol. Base auditée : `e60561d3a2ecaf3441b005cd2e5805ecfc030854`, téléphone 1.0.11/code111, run53 vert selon la passation de Fab/Sol.

Intention : une phase de présentation explicite autour du moteur, sans déplacer les dégâts/soins vers l'EOS.

Contrat de Fab :
- INTRO : trois intros aléatoires, aspect-fit/audio, moteur différé.
- PRÉ-ROUND : VV en boucle, frise/vies et deux chronos visibles mais figés; ROUND N jaune ~1 s puis START! animé. Fin réelle de START avant commandes/orbes/chronos. Numérotation par échange scoré; pas de nouvelle présentation au retour d'un pouvoir.
- ROUND actif : logique historique, coûts ST60/40/60 et TR60/60/80, strict énergie>coût, énergie fractionnaire, selected une fois par combat.
- JAUGES2/3/4 et5/6/7 : boutons/jauges/interactions historiques visibles et actifs; aucune cinématique exclusive.
- POUVOIRS21..26 : UI gameplay masquée, orbes/tactile/car/car2 suspendus; seul le calcul historique du pouvoir continue jusqu'à son résultat. Attendre aussi EOS avant reprise. EOS n'applique aucun effet et ne rejoue pas le MP4 si le calcul n'est pas terminé.
- POUVOIR fatal : finir le pouvoir MP4, puis finishing10/11 intégral, puis sortie historique.
- FINISHING : aucun HUD; attendre EOS. Échec média explicite/borné sans blocage définitif.
- VV : continuité par fraction/seek après interruption, boucle naturelle à sa fin.

Préserver score cubique, seuil strict20000, lettres, dégâts/soins/gains, auras, menu/niveaux, moteur hérité hors suspension de présentation, admin20taps invisible avant activation, protection charge→orbes2s (chevauche ROUND/START), pruning exact-prefix validé, médias et chaîne native. Deux ABI et icône inchangées.

Le doublon « Tyrannosaurus Win » doit être attribué après corrélation fichier/génération/état/position/audio et capture téléphone, jamais supposé legacy.

Livrer candidat après1.0.11, tests du main généré, CI renforcée sans refonte native, APK debug et commit/run/SHA256. Pas de merge main, pas de release. Synchroniser les cinq mémoires; distinguer simulation, build Android et validation téléphone.
