# JTrex / June T-Rex — Debug historical

## Statut

Registre documentaire issu d'une analyse statique de JuneTrex/main.py et de ses ressources.

Aucune observation ci-dessous n'a été corrigée pendant la mission. Le jeu n'a pas été exécuté ; les manifestations à l'écran restent à confirmer lorsque Fab autorisera une phase de validation.

Statuts utilisés :

- CONSTAT STATIQUE : directement lisible dans le code, la configuration ou l'inventaire ;
- CONSÉQUENCE À CONFIRMER : effet probable qui demande une exécution ;
- INTENTION À VALIDER : asymétrie ou comportement qui peut être volontaire.

Référence :
main 164d03be77c83f49e1094294f36f860ec183df68
main.py SHA-256 3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231

## Observations JT-OBS

### JT-OBS-001 — Casse a.png / A.png
Statut : CONSTAT STATIQUE.
Source : chargement de ressource actif vs inventaire de JuneTrex.
Le code demande a.png tandis que l'archive contient A.png. Risque sur systèmes sensibles à la casse.

### JT-OBS-002 — Casse boutbleu0.png / boutBleu0.png
Statut : CONSTAT STATIQUE.
Source : chargement de ressource actif vs inventaire.
Même risque de casse.

### JT-OBS-003 — horseg2ko/chargetrwin_83.jpeg absent
Statut : CONSTAT STATIQUE.
Source : série horseg2ko et inventaire.
Ne pas renommer automatiquement un fichier voisin sans comparaison visuelle.

### JT-OBS-004 — Score dépendant des coordonnées de fenêtre
Statut : CONSTAT STATIQUE.
Source : colpts.
Le score utilise les écarts verticaux en coordonnées de fenêtre avec des constantes fixes. L'indépendance à la résolution n'est pas démontrée.

### JT-OBS-005 — Pas des orbes non normalisé au temps
Statut : CONSTAT STATIQUE.
Source : colvv.
haut[i] est incrémenté par sens*pas à chaque callback, sans multiplication par delta temps.

### JT-OBS-006 — Zones tactiles actives malgré rectangle masqué
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : on_touch_down + représentation par Rectangle.
La taille/visibilité graphique n'est pas une garde tactile automatique.

### JT-OBS-007 — Menu/IA/niveaux sans garde générale de phase
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : tests tactiles indépendants dans on_touch_down.
Vérifier les effets d'appuis hors menu.

### JT-OBS-008 — Lettres et minima ex æquo
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : asb.
Les comparaisons strictes du minimum peuvent ne sélectionner aucun des trois écarts en cas d'ex æquo.

### JT-OBS-009 — Seuil S asymétrique
Statut : CONSTAT STATIQUE / INTENTION À VALIDER.
Source : asb.
S gauche <5,6 ; S droite <8.

### JT-OBS-010 — Pas de nouvelle lettre pour valeur >=320
Statut : CONSTAT STATIQUE.
Source : asb.
Aucune branche supérieure identifiée après F<320.

### JT-OBS-011 — Énergie : branche supplémentaire asymétrique
Statut : CONSTAT STATIQUE / INTENTION À VALIDER.
Source : fin de anim_1.
La branche if ΔD<ΔG ... else ... n'est pas symétrique pour toutes les variations, notamment égales.

### JT-OBS-012 — Soin état 22 et références de dégâts
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : anim_1.
Le soin écarte une partie du bloc commun et ne met pas degg0/degd0 à jour comme les autres états. Vérifier réinterprétation ultérieure de la variation négative et effet sur énergie.

### JT-OBS-013 — Pouvoirs héritent anim1 / anim1vv
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : on_touch_down/carupdate vers états 21..26.
Le changement d'indexa n'est pas accompagné d'un reset explicite de l'indice/sens.

### JT-OBS-014 — Ancien préfixe + nouvel indice possible
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : ordre des opérations de anim_1.
Le préfixe est mémorisé avant certaines transitions de indexa/anim1.

### JT-OBS-015 — Frames logiques non affichées lors de retard
Statut : CONSTAT STATIQUE.
Source : mc1.
anim_1(False) avance la logique sans changer l'image.

### JT-OBS-016 — Premier/troisième pouvoirs droits visuellement inversés
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : création des rectangles vs affbt.
Création associe premier à trfs et troisième à trma ; affbt emploie ensuite trma pour le premier et trfs pour le troisième.

### JT-OBS-017 — Faute babokpbd / babokepbd
Statut : CONSTAT STATIQUE.
Source : réinitialisation côté droit.
Nom incohérent à vérifier en exécution.

### JT-OBS-018 — Mort simultanée termine sur état 10
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : mc1.
Les deux if de fin sont indépendants et les comp sont calculés avant ; la branche compd<1 écrase finalement l'état précédent.

### JT-OBS-019 — Retour menu avant dernières images finales
Statut : CONSTAT STATIQUE.
Source : états 10/11.
Retour à longanim1[indexa]-3.

### JT-OBS-020 — Reset de partie distribué
Statut : CONSTAT STATIQUE.
Source : affbt, carupdate, colvv, anim_1 et autres.
Il n'existe pas un reset transactionnel unique de tout l'état.

### JT-OBS-021 — Visibilité des jauges pilotée par callbacks distincts
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : affpv et affbt.
Vérifier les états transitoires ou clignotements inattendus.

### JT-OBS-022 — Moteur air hockey encore exécuté
Statut : CONSTAT STATIQUE.
Source : mainApp.on_start.
screen_up, ga, da et pter restent planifiés alors que les éléments correspondants peuvent être masqués.

### JT-OBS-023 — Workflow Android peut choisir le mauvais main.py
Statut : CONSTAT STATIQUE.
Source : .github/workflows/android.yml + inventaire de l'archive.
Le workflow cherche le premier main.py ; June air hockey et plusieurs variantes en contiennent.

### JT-OBS-024 — Taille de fenêtre mémorisée sans recalcul global
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Source : initialisation Window/xmax/ymax.
Vérifier rotation, redimensionnement ou reprise selon plateforme.

### JT-OBS-025 — Audio chargé sans garde systématique
Statut : CONSTAT STATIQUE.
Source : SoundLoader.load puis .play() dans plusieurs chemins.
Un échec de chargement n'est pas toujours testé.

### JT-OBS-026 — Aucun tapotement automatique IA trouvé
Statut : CONSTAT STATIQUE.
Source : parcours du main.py.
Les incréments tapg/tapd identifiés se trouvent dans les commandes tactiles ; aucune stratégie de tap automatisé n'a été trouvée.

## Observations supplémentaires liées au moteur hérité

### JT-LEGACY-001 — tantemps et temps nul
Statut : CONSTAT STATIQUE avec CONSÉQUENCE À CONFIRMER.
Pas de garde explicite identifiée avant division par l'intervalle temporel.

### JT-LEGACY-002 — vectoriser et axe identique
Statut : CONSTAT STATIQUE.
Retour (0,0) lorsque l'un des axes est exactement identique dans le chemin observé.

### JT-LEGACY-003 — référence musicale m
Statut : CONSTAT STATIQUE.
Une branche historique référence m alors que sa création est commentée.

### JT-LEGACY-004 — pbt reste False
Statut : CONSTAT STATIQUE.
Le drapeau pbt est forcé False dans les deux branches du test observé ; les anciennes branches de but exigeant True ne devraient pas être atteintes par ce chemin.

## Règle de traitement

Aucune entrée de ce fichier n'est une autorisation de correction. Avant de modifier le programme :

1. reproduire si possible sur la version de référence ;
2. distinguer bug, asymétrie volontaire et dette historique ;
3. faire valider l'intention par Fab ;
4. préparer un ordre de mission séparé ;
5. préserver le gameplay historique tant que la correction n'est pas explicitement autorisée.


## Audit de complétude documentaire

### JT-DOC-001 — Vérification de transcription du relais Astra
Statut : DOCUMENTATION COMPLÉTÉE.

Une relecture croisée du relais Astra et des cinq mémoires a identifié quelques détails qui étaient seulement implicites dans la première transcription : rôle de choixidh/choixidb, colv[7..9], portée du hash, limites de l'inventaire visuel, variantes horseg2ko et nuances du suivi tactile hérité.

Ces éléments ont été ajoutés à brain.md et brainmap.md. Cette opération n'est pas une validation en exécution et ne transforme aucune JT-OBS en correction.


## JT-ANDROID-001 — observations de préparation

### JT-PORT-001 — Archive binaire non rematérialisée par Sol
Statut : LIMITE D'ENVIRONNEMENT.
Le téléchargement binaire direct de l'asset de 327 992 765 octets n'a pas pu être matérialisé dans l'environnement Sol courant. Le digest de l'asset a été vérifié via les métadonnées GitHub, mais le SHA-256 de `JuneTrex/main.py` n'a pas été recalculé par Sol. La valeur de référence reste celle de l'audit Astra.

### JT-PORT-002 — Workflow source non reproductible
Statut : CONSTAT STATIQUE.
Le workflow actuel dépend de la « dernière release », alors que la mission exige la release/tag `JTrex` explicitement identifiée.

### JT-PORT-003 — Sélection ambiguë de la racine
Statut : CONSTAT STATIQUE.
Le workflow actuel sélectionne le premier `main.py` trouvé. La mission exige explicitement `JuneTrex/main.py`.

### JT-PORT-004 — Aucun journal de build exploitable retrouvé dans les contrôles accessibles
Statut : ÉTAT DE PRÉPARATION.
Aucun run/log antérieur exploitable n'a été obtenu par les accès disponibles à Sol. Ne pas en déduire qu'aucun build historique n'a jamais été tenté.


## JT-ANDROID-001 — application du patch Astra

### JT-PORT-005 — Version Android candidate
Statut : DÉCISION DE BRANCHE.
Le dépôt GitHub public ne contient qu'une release historique avec `JuneTrex.zip` et aucun APK/AAB antérieur visible. `versionName=1.0.1` et `android.numeric_version=101` sont retenus pour ce candidat. Cela ne constitue pas une vérification de l'historique éventuel du Play Console.

### JT-PORT-006 — Icône provisoire
Statut : À VALIDER VISUELLEMENT.
`pter/pter0.png` est utilisée sans transformation comme icône provisoire. Son rendu dans le lanceur Android reste à contrôler.

### JT-PORT-007 — Reproductibilité partielle
Statut : OUVERT.
Archive, racine, main historique et transformations sont figés par empreintes. Buildozer et python-for-android ne sont pas encore verrouillés à des révisions déterminées ; relever les versions/révisions du build avant toute affirmation de reproductibilité complète.

### JT-OBS-003
Reste OUVERT. `horseg2ko/chargetrwin_83.jpeg` n'est ni créée, ni remplacée, ni contournée par décalage d'indice.


### JT-PORT-008 — Run #7 : échec libffi / Autoconf
Statut : CONFIRMÉ PAR BUILD.

Run : `36319044247`.
Commit : `e702da7c07e63ee760dbfe677a9d9062f6c7d587`.

La préparation historique passe intégralement. L'échec survient pendant la compilation native de python-for-android/libffi :

`configure.ac:215: error: possibly undefined macro: LT_SYS_SYMBOL_USCORE`
`autoreconf: error: /usr/bin/autoconf failed with exit status: 1`

Aucun APK n'a été produit. La collecte APK a été ignorée après cet échec.

Ce constat pointe la chaîne native/autotools et non une erreur démontrée dans le gameplay JTrex. Ne pas modifier main.py pour traiter cette erreur sans preuve.

Révisions relevées :
- Buildozer : `a153097b3c534bea8a17da2abf1369d67c8cbfcb`
- python-for-android : `58d21141f17c889bf8585f5665921d72028f8831`

Le diagnostic `JuneTrex-Android-Diagnostics` a été produit avec succès.


### JT-PORT-009 — Hypothèse libltdl-dev
Statut : HYPOTHÈSE EN TEST.

Astra propose l'ajout de `libltdl-dev` au runner Ubuntu, car `ltdl.m4` fournit la macro `LT_SYS_SYMBOL_USCORE` manquante lors du run #7.

Le test doit modifier uniquement cette dépendance et relancer le même scénario. Si l'erreur persiste, vérifier le chemin aclocal avant toute autre correction.


### JT-PORT-010 — libltdl-dev valide l'hypothèse du run #7
Statut : CONFIRMÉ PAR BUILD.

Run #8 : `36322734005`.
L'erreur `LT_SYS_SYMBOL_USCORE` n'apparaît plus. Le build franchit donc le blocage Autoconf/libffi identifié au run #7.

### JT-PORT-011 — Nouveau blocage pip interne python-for-android
Statut : CONFIRMÉ PAR BUILD.

Première nouvelle erreur discriminante du run #8 :

`ImportError: cannot import name 'BuildDependencyInstallError' from 'pip._internal.exceptions'`

Le traceback provient du venv interne situé sous :
`build/venv/lib/python3.14/site-packages/pip/`

La commande en échec rapportée est :
`source venv/bin/activate && pip install -U pip`

Le host Python construit par la chaîne indique Python 3.14.2.

Aucune correction n'est autorisée ici sans nouvelle proposition Astra. Ne pas attribuer ce blocage au gameplay JTrex.


### JT-PORT-012 — Hypothèse venv p4a réutilisé
Statut : HYPOTHÈSE EN TEST.

Astra relie le traceback `BuildDependencyInstallError` à un possible mélange de modules pip dans le venv temporaire commun aux architectures.

Test unique : patch local de python-for-android au SHA `58d21141f17c889bf8585f5665921d72028f8831`, ajoutant uniquement `--clear` à la création du venv.

Ne pas pinner une version de pip ni changer Python 3.14.2 pendant ce test. Si la même erreur persiste, examiner l'origine réelle des modules importés avant une nouvelle correction.


### JT-PORT-013 — Run #9 : premier APK produit
Statut : CONFIRMÉ PAR BUILD.

Run `36330526427` : succès complet.

Le patch p4a `venv --clear` permet de franchir le blocage pip du run #8 et la compilation Android aboutit à `JuneT-Rex-1.0.1-debug.apk`.

APK :
- taille : 297060998 octets ;
- SHA-256 : `e9ca9935c79616868969dfe249a4a3afcd945c06d37392fb7ab3d8055057011c` ;
- architectures : arm64-v8a + armeabi-v7a ;
- signature : certificat Android Debug, vérification JAR sans erreur fatale dans l'environnement Sol.

Aucune installation/exécution téléphone n'a encore été réalisée par Sol. Statut fonctionnel : APK compilé et contrôlé statiquement ; installation et fonctionnement à valider par Fab.


### JT-MEDIA-001 — Fournisseur vidéo Android à qualifier
Statut : EN COURS.

Kivy 2.3.1 expose notamment les fournisseurs vidéo ffmpeg et ffpyplayer, mais le fournisseur réellement disponible dans l'APK actuel n'est pas encore un lecteur vidéo exploitable : aucun backend vidéo supplémentaire n'est inclus dans `requirements = python3,kivy`.

Le commit p4a actuellement figé contient une recette ffpyplayer 4.5.1 dépendant de FFmpeg 8.0.1. Un signalement public amont décrit une incompatibilité de compilation ffpyplayer 4.5.1 / FFmpeg 8.0.1. Ne pas ajouter cette dépendance sans test ciblé ou solution compatible documentée.

L'intake média utilise le ffprobe du runner uniquement pour inspection ; cela n'ajoute pas FFmpeg à l'APK.


### JT-MEDIA-002 — Compatibilité ffpyplayer / FFmpeg
Statut : CORRECTION DE CHAÎNE CANDIDATE À TESTER.

Le p4a figé utilise ffpyplayer 4.5.1 et FFmpeg 8.0.1, combinaison pour laquelle un échec de compilation public existe (avfft.h supprimé). Le candidat 1.0.2 conserve le même p4a mais remplace uniquement sa recette FFmpeg par la recette 6.1.2 provenant du commit p4a `541fe992ea86b3902f0e0f776167555da6dbca01`.

Ce changement est motivé uniquement par le décodage MP4 H.264/AAC requis par JT-MEDIA-001. Il doit être validé par build réel.

### JT-MEDIA-003 — Repli vidéo
Statut : PAR CONCEPTION.

Si l'intro ne produit pas de lecture valide, un timeout borné libère le lecteur et donne accès au jeu. Si la vidéo d'attente ne produit aucune frame en 4 s, elle est libérée et les JPEG historiques reprennent. Aucun événement de vidéo ne déclenche dégâts ou changements de phase.


### JT-MEDIA-004 — Run #11 : ffpyplayer incompatible Python 3.14
Statut : CONFIRMÉ PAR BUILD.

Run : `36351063741`.
Commit : `e11a37fb88417d9e0cf102a3604374a86a97f950`.

La préparation média et la recette FFmpeg 6.1.2 passent. L'échec survient pendant la compilation de ffpyplayer 4.5.1 contre Python 3.14.2.

Erreurs discriminantes :
- `_PyLong_AsByteArray` attend 6 arguments, le C généré en fournit 5 ;
- `_PyGen_SetStopIterationValue` n'est plus déclaré.

Un ticket ffpyplayer Python 3.14 est encore ouvert. Aucun APK 1.0.2 n'a été produit par ce run.

Hypothèse suivante : conserver p4a/FFmpeg mais fixer python3 + hostpython3 à 3.11.13, sans modifier le C de ffpyplayer.


## 2026-09-28 — FAB-DEBUG-001 / JT-MEDIA-001

- Run #11 (commit `e11a37fb88417d9e0cf102a3604374a86a97f950`) : ffpyplayer échoue avec des appels C incompatibles avec CPython 3.14.
- Un commit intermédiaire `04a539992baabe25a5cea218636c7bedb4928585` avait tenté `python3==3.11.13`.
- Nouvel essai ciblé : `python3==3.12.14` + `hostpython3==3.12.14`, sans autre changement fonctionnel.
- Risque identifié avant relance : le préparateur contient une assertion 3.11.13 et peut arrêter le workflow avant ffpyplayer. Si cela se produit, le test 3.12.14 sera classé incomplet et aucune deuxième correction ne sera ajoutée à ce run.


### Résultat réel du run #13 — 2026-09-28

- Commit construit : `0f73b3d31d4dc242daecb102f4c18579c8413627`.
- GitHub Actions : run #13, ID `36355762409`, job `108723048564`.
- Échec à l'étape `Verify and prepare JuneTrex sources`, avant installation Buildozer/p4a et avant compilation ffpyplayer.
- Erreur discriminante : `RuntimeError: Python cible doit rester figé sur 3.11.13 pour ffpyplayer.`
- Le pin 3.12.14 présent dans `buildozer.spec` n'a donc pas encore été transmis à p4a ; les versions effectives python3/hostpython3 3.12.14 et le Cython isolé ne peuvent pas être prouvés sur ce run.
- Artefact disponible : `JuneTrex-Android-Diagnostics` (ID `10943932232`).
- Aucun APK 1.0.2 produit. Lecture vidéo et gameplay non testés.
- Conformément à FAB-DEBUG-001, aucune seconde correction fonctionnelle n'est ajoutée à ce run.


## 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — alignement préparation Python 3.12.14

- Cause du blocage du run #13 conservée dans l'historique : `tools/prepare_android.py` imposait encore Python 3.11.13 alors que `buildozer.spec` testait 3.12.14.
- Correction autorisée : quatre remplacements exacts dans le préparateur, uniquement 3.11.13 → 3.12.14 pour la garde et le reporting.
- Le test de compatibilité natif Python 3.12.14 / ffpyplayer 4.5.1 reste à réaliser ; aucun succès n'est présumé.


### Résultat réel du run #14 — 2026-09-28

- Commit construit : `393e1612fa98d04cd5d69c33eae140caf693c8d2`.
- GitHub Actions : run #14, ID `36356865568`, job `108726222221`.
- `Verify and prepare JuneTrex sources` : SUCCÈS ; la garde 3.12.14 est franchie.
- p4a demande explicitement `python3 3.12.14` et `hostpython3 3.12.14`, puis télécharge pour les deux le tag CPython `v3.12.14.tar.gz`.
- Le workflow conserve toutefois une variable d'environnement héritée `VERSION_hostpython3=3.11.13` ; elle est consignée comme incohérence de diagnostic, sans correction dans ce run. Les traces p4a de recette/source indiquent bien 3.12.14 pour hostpython3.
- p4a prévoit les architectures `armeabi-v7a, arm64-v8a` et commence par construire Python cible pour `armeabi-v7a`.
- Premier nouveau blocage : CPython 3.12.14 échoue dans `Modules/grpmodule.c` sur Android/armeabi-v7a : `setgrent`, `getgrent` et `endgrent` sont non déclarées ; `getgrent` entraîne aussi une conversion int→pointeur invalide.
- `python3` pour `arm64-v8a` n'est pas atteint ; la compilation de `ffpyplayer` n'est pas atteinte.
- Les erreurs historiques `_PyLong_AsByteArray` et `_PyGen_SetStopIterationValue` n'apparaissent pas dans ce run, mais leur disparition dans ffpyplayer n'est pas prouvée puisque ffpyplayer n'a pas été compilé.
- Aucun APK 1.0.2 produit. Artefact diagnostic : `JuneTrex-Android-Diagnostics`, ID `10944283554`.
- Aucun correctif supplémentaire appliqué conformément à FAB-DEBUG-001.


## 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — grp Android API 21

- Run #14 : échec de CPython 3.12.14/armeabi-v7a dans `Modules/grpmodule.c` sur `setgrent/getgrent/endgrent`.
- Correction mono-hypothèse proposée par Astra : déclarer `grp` indisponible dans le Python Android cible pour API native <26 via `py_cv_module_grp=n/a`.
- Aucun warning n'est désactivé, aucune fonction Android n'est simulée, et aucun autre module standard n'est modifié.
- Risque assumé : le Python Android résultant n'aura pas le module `grp`; si une dépendance l'importe obligatoirement, cet échec devra être rapporté explicitement.
- L'hypothèse ffpyplayer 4.5.1 / Python 3.12.14 reste non validée avant le prochain run.


### Résultat réel du run #15 — 2026-09-28

- Commit construit : `b7323fdb940b9be6e47e31f1ceed8d1094adc31c`.
- GitHub Actions : run #15, ID `36360940843`, job `108737876412`.
- Le patch `tools/patches/p4a-python312-grp-api21.patch` est appliqué avec succès par le workflow.
- La recette python3 cible journalise : `JT-MEDIA-001: target grp unavailable below Android API 26`.
- Pour le hostpython Linux, le configure conserve `checking for stdlib extension module grp... yes` et `Modules/grpmodule.c` est compilé : comportement attendu, le patch ne vise pas hostpython.
- Pour le Python Android cible armeabi-v7a, le configure journalise `checking for stdlib extension module grp... n/a`.
- Aucun `Modules/grpmodule.c` cible Android n'est compilé ; le blocage `setgrent/getgrent/endgrent` du run #14 est franchi.
- Le build progresse ensuite jusqu'à `Building ffmpeg for armeabi-v7a` avec FFmpeg 6.1.2.
- Première nouvelle erreur discriminante : `libavcodec/vulkan_av1.c:183:43: error: incompatible pointer to integer conversion initializing 'VkVideoSessionParametersKHR' ... with 'void *'`, sur `.videoSessionParametersTemplate = NULL`.
- La même phase signale ensuite dans `libavcodec/vulkan_decode.c` des affectations `NULL` incompatibles vers `VkImageView`.
- La commande configure FFmpeg observée contient notamment `--enable-hwaccels`.
- `python3` pour arm64-v8a n'est pas atteint ; FFmpeg arm64-v8a n'est pas atteint.
- ffpyplayer 4.5.1 est téléchargé/préparé pour armeabi-v7a, mais sa phase `Building ffpyplayer` n'est pas atteinte.
- Les erreurs `_PyLong_AsByteArray` et `_PyGen_SetStopIterationValue` sont absentes du log, sans valeur probante pour ffpyplayer puisqu'il n'a pas été compilé.
- Aucun APK 1.0.2 produit. Artefact diagnostic : `JuneTrex-Android-Diagnostics`, ID `10945787341`.
- Aucun second correctif appliqué dans cette tentative.


## 2026-09-28 — JT-MEDIA-001 — exclusion Vulkan FFmpeg 6.1.2

- Run #15 : premier nouveau blocage dans FFmpeg 6.1.2/Vulkan pour armeabi-v7a sur `VkVideoSessionParametersKHR = NULL`, puis `VkImageView = NULL`.
- Correction mono-hypothèse autorisée : ajouter uniquement `--disable-vulkan` à la recette FFmpeg tout en conservant `--enable-hwaccels`.
- Aucun patch `NULL -> VK_NULL_HANDLE`, aucune mise à jour FFmpeg et aucune désactivation globale des hwaccels dans cette tentative.
- Conséquence assumée : l'accélération Vulkan FFmpeg sera absente de l'APK ; la fluidité du décodage logiciel restera à valider sur téléphone si l'APK est produit.


### Run #16 — résultat réel (2026-09-28)
Le correctif unique `--disable-vulkan` franchit le blocage Vulkan du run #15. FFmpeg 6.1.2 et ffpyplayer 4.5.1 compilent pour arm64-v8a et armeabi-v7a ; les erreurs Cython historiques ne réapparaissent pas. APK produit avec SHA-256 `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a`. Validation runtime téléphone encore ouverte.


### Premier crash téléphone — diagnostic ouvert — 2026-09-28

Constat Fab : l'application affiche le logo Kivy puis se ferme. La compilation du run #16 est réussie, mais le démarrage applicatif, l'intro vidéo et le gameplay ne sont pas validés.

APK identifié :
- fichier transmis : `JuneT-Rex-1.0.2-debug.apk` ;
- build GitHub Actions : run #16, ID `36364807323` ;
- commit construit : `e88bd93ec0a7d9b34b2d4f64eb10b3627d230149` ;
- version : `1.0.2` ;
- versionCode / numeric-version : `102` ;
- package : `com.junedady.junetrex` ;
- SHA-256 vérifié sur l'artefact réellement téléchargé : `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a` ;
- ABIs contenues dans l'APK : `arm64-v8a` et `armeabi-v7a`.

Limite actuelle : aucun accès ADB au téléphone de Fab dans cette session et aucun environnement Android compatible disponible ici pour reproduire le lancement. Le crash n'est donc pas reproduit et sa cause reste inconnue.

Marqueurs disponibles dans les sources préparées : `[JT-BOOT]`, `[JT-START]`, `[JT-INTRO] chosen=`, `[JT-INTRO] begin=`, `[JT-INTRO] gameplay enabled`. Sans logcat du lancement réel, aucun de ces marqueurs ne peut être déclaré comme dernier marqueur atteint.

Diagnostic à poursuivre uniquement avec un journal de lancement complet (Python, Java et natif). Ne pas attribuer le crash à la vidéo, ffpyplayer, FFmpeg, Kivy ou une ressource avant la première erreur fatale observée.


### Crash téléphone 1.0.2 — preuve bugreport reçue — 2026-09-28

Rapport téléphone reçu : `bugreport-a57xnaeea-BP4A.251205.006-2026-09-28-10-54-03.zip`.

Identité de l'appareil et de l'installation vérifiée dans le bugreport :
- modèle : `SM-A576B` ;
- Android : 16, build `BP4A.251205.006` ;
- ABI réellement utilisée : `arm64-v8a` ;
- package installé : `com.junedady.junetrex` ;
- version : `1.0.2` ; versionCode : `102` ; minSdk 21 ; targetSdk 36 ;
- application installée en mode debuggable ; APK signing version 2.

Lancement pertinent observé à 10:53:39 : process `16365`. PythonActivity atteint `onCreate`, `onStart`, `onResume`, crée sa SurfaceView puis lance `SDL_main` et `Initializing Python for Android`.

Dernières traces Python avant terminaison :
```text
10:53:40.440 python: Initializing Python for Android
10:53:40.440 python: Setting additional env vars from p4a_env_vars.txt
10:53:40.440 python: Changing directory to '/data/user/0/com.junedady.junetrex/files/app'
10:53:40.442 python: Preparing to initialize python
10:53:40.442 python: _python_bundle dir exists
10:53:40.442 python: set wchar paths...
10:53:40.506 python: Python initialization failed:
10:53:40.506 python: failed to get the Python codec of the filesystem encoding
10:53:40.506 python: Python for android ended.
```

Le processus meurt ensuite à 10:53:40.604. Aucun marqueur `[JT-BOOT]`, `[JT-START]` ou `[JT-INTRO]` n'apparaît dans le bugreport : le code applicatif `main.py` n'est donc pas atteint. Le crash ne peut pas être attribué aux vidéos, à l'intro ou au gameplay à ce stade.

La même erreur `failed to get the Python codec of the filesystem encoding` est répétée sur plusieurs autres tentatives de lancement dans le rapport, ce qui confirme un échec reproductible de l'initialisation CPython sur l'appareil.

Inspection statique de l'APK du run #16 : `libpybundle.so` contient `_python_bundle/stdlib.zip`, et cette archive contient bien le paquet `encodings` (122 entrées) ainsi que `codecs.pyc`. Le diagnostic ne doit donc pas être simplifié en « encodings absent » sans analyse supplémentaire ; il s'agit d'un échec de chargement/initialisation du codec de filesystem pendant le démarrage CPython.

Aucune correction n'est appliquée dans cette étape de diagnostic.


## 2026-09-28 — FAB-DEBUG-001 — diagnostic bootstrap Python

Le bugreport 1.0.2 ne contient que le PyStatus générique `failed to get the Python codec of the filesystem encoding`. Aucun détail import/zip/codecs n'est disponible. Les probes libpython 3.14/3.13 échouent mais libpython3.12.so charge correctement : ils ne sont pas retenus comme cause du crash.

Patch diagnostique ajouté sous `tools/patches/p4a-python312-bootstrap-exception-diag.patch`, sans modification des chemins, du bundle, des médias, de FFmpeg, de Cython ou du gameplay. L'objectif du prochain APK est uniquement d'exposer l'exception Python en attente et les chemins réels.


### Run #17 — échec de forme du patch diagnostique
Le run #17 (36410139322) n'a pas compilé p4a. `git apply --check` a rejeté `p4a-python312-bootstrap-exception-diag.patch` comme corrompu à la ligne 113. Cet échec ne teste aucune hypothèse Python. Les seules modifications suivantes portent sur les compteurs d'en-tête des hunks afin d'appliquer le même diagnostic Astra.


### Run #18 — diagnostic compilé, runtime non encore observé

Le run #18 (36410518782) construit avec succès le même diagnostic Astra après correction de forme du patch. Le log de build confirme la compilation de `start.c` pour arm64-v8a et armeabi-v7a, et `p4a-patch.txt` contient les traces `P4A_DIAG`. APK : SHA-256 `fbc4a1d0f72cf677591e4a4ffb366db9237377c5f5c3574d6f7ca025249d8e64`. Aucune conclusion sur la cause racine n'est encore possible avant lancement téléphone et nouveau rapport.


### Run #18 — cause immédiate identifiée par P4A_DIAG

Le nouveau bugreport téléphone montre la même séquence sur de nombreuses tentatives. L'exception sous-jacente est enfin visible :
`ZipImportError: can't decompress data; zlib not available`, avec contexte `ImportError: dlopen failed: cannot locate symbol "PyExc_MemoryError" referenced by zlib.cpython-312.so`.

Contrôle ELF sur l'APK du run #18 : le symbole `PyExc_MemoryError` est bien exporté par `libpython3.12.so`, tandis que `zlib.cpython-312.so` le laisse non résolu et n'a pas de DT_NEEDED vers `libpython3.12.so`. Cet élément est une preuve technique à analyser par Astra pour choisir la prochaine correction mono-hypothèse.

Aucune modification de code ni de chaîne n'est appliquée après cette observation.


## 2026-09-28 — FAB-DEBUG-001 — essai DF_1_GLOBAL

Précondition vérifiée sur l'APK du run #18 : `GLOBAL` est absent de `DT_FLAGS_1` sur arm64-v8a et armeabi-v7a ; seul `NOW` est présent. `PyExc_MemoryError` reste exporté par libpython. Aucun DT_SONAME explicite n'est observé sur libpython3.12.so dans cet APK.

Essai mono-hypothèse : marquer uniquement la libpython cible 3.12.14 avec `-Wl,-z,global`. Aucun LDFLAGS global, aucun DT_NEEDED ajouté à zlib, aucune modification de main.py, chemins, bundle, médias ou gameplay.


### Run #19 — résultat de l'essai GLOBAL

Le run #19 compile avec succès l'unique hypothèse Astra. L'APK final contient `DF_1_GLOBAL` sur libpython3.12.so pour arm64-v8a et armeabi-v7a, et `PyExc_MemoryError` reste exporté. Le log de liaison contient bien `-Wl,-z,global`.

Observation conservée : aucun `DT_SONAME` explicite n'est présent dans le libpython final, comme dans le run #18. Aucun correctif supplémentaire n'est appliqué.

La cause runtime n'est pas encore déclarée corrigée : seul un lancement téléphone peut confirmer la disparition de l'erreur `cannot locate symbol "PyExc_MemoryError"` et la progression du bootstrap.

## 2026-09-30 — JT-MEDIA-POWER-SCORE-001 — garde de non-régression

État de départ vérifié : `port/android-first-apk` = `a6caa620e51281d4a2a8dc854830f15b5db66c7b`. Aucun changement natif autorisé ni appliqué dans ce lot. Les correctifs qui ont rendu le bootstrap Android fonctionnel restent intacts.

Médias importés sans merge de main, depuis leurs blobs existants. Le runtime remplace uniquement l'image de fond des états 1, familles 2/3/4 et 5/6/7, 8 et 9. EOS n'agit jamais sur `indexa`, dégâts ou timers. 10/11 ne sont pas remplacés.

Le débit historique unique 60 des six pouvoirs est remplacé seulement sur les six chemins de pouvoirs par la table Fab : 60/40/60 | 60/60/80. La garde est strictement `>`. Les autres constantes 60 du jeu ne doivent pas être modifiées par généralisation.

Le score reste `max(0, 150000000 - somme(abs(haut[i]-haut[7])**3))`. L'écart connu entre la cible `haut[7]` et le centre de la fenêtre affichée est instrumenté, pas corrigé. Toute correction future exige une preuve téléphone et doit rester géométrique/minimale.

Statut au moment de cette entrée : modifications Git présentes jusqu'à `d547fb9315f1432f2b5cda4417340fda67abacc5`; tests Actions, APK 1.0.3 et validation téléphone non encore consignés.



## 2026-09-30 — JT-MEDIA-POWER-SCORE-001 — constats après CI verte

Le run Android #32 (`36753181725`) et le run inspection #11 (`36753181720`) sont verts au commit code `7f83389086ebe847007ddd48e506157ae41f74ad`.

APK produit :
- `JuneT-Rex-1.0.3-debug.apk`
- 319081968 octets
- SHA-256 `48de9d70a2a6b03f641ff001973e782e7d56e8ec1d9e367c624ca4af85a73fdb`
- arm64-v8a + armeabi-v7a
- signature Android Debug.

Les cinq médias combat inspectés sont H.264 852×480 avec piste AAC stéréo 44,1 kHz. Aucune rotation n'est signalée. ffprobe retourne PAR/DAR non renseigné pour ces fichiers ; aucune transformation de rotation/PAR particulière n'est donc appliquée dans le runtime.

Durées observées :
- rouge/bleu : 3.791667 s ;
- jaune : 6.757007 s ;
- attente : 11.333334 s ;
- verdict ST : 7.166667 s ;
- verdict TR : 3.625000 s.

Les captures début/milieu/fin montrent que les scènes 15, 16, 60 et 61 commencent et finissent sur des frames quasi noires de transition, tandis que l'action utile apparaît au milieu. La scène 20 montre l'action sur les trois captures. Ceci est une propriété des pixels de la vidéo, pas une marge créée par l'aspect-fill.

Non validé à ce stade :
- comportement réel des cinq scènes sur le téléphone ;
- limites d'énergie 40/40,5, 60/60,5 et 80/80,5 en interaction réelle ;
- absence de double activation sous taps rapides en conditions téléphone ;
- cause géométrique du score sur écran réel ;
- correction géométrique éventuelle.

Ne pas déclarer ces points corrigés/validés avant retour Fab.


## 2026-09-30 — JT-MEDIA-AUDIO-001 — audio natif des vidéos de combat

Correction codée : les vidéos de combat ne sont plus volontairement muettes ; l'audio MP4 est activé au premier frame exploitable et l'ancien son de scène est stoppé à ce moment. Risques restant à valider sur téléphone : double son résiduel, audio continu après transition, synchronisation de la boucle indexa 1 et pause/reprise. Ne pas déclarer ces points validés avant test réel.


## 2026-10-01 — JT-MEDIA-ADMIN-001 — diagnostic des sources d'animation

Ajout d'un diagnostic non intrusif pour distinguer le rendu réellement actif. Point clignotant vert si _jt_scene_video_active=True, rouge sinon. Le menu admin expose les chemins legacy afin d'éviter de confondre une jauge historique superposée avec une nouvelle vidéo de fond. À valider sur téléphone : déclenchement 20 taps, lisibilité du Popup, couleur correcte lors des transitions/fallback, absence d'effet sur les contrôles.


## 2026-10-01 — JT-POWER-VIDEOS-001 — six pouvoirs vidéo + charge corrigée

Le lot remplace uniquement les médias/rendus : aucune correction gameplay, dégâts, durée logique, score, IA ou coût n'est dérivée de la durée des MP4. Les fichiers source ont été envoyés par Fab sur main ; intégration prévue par réutilisation des blobs, sans merge main. Points à vérifier sur téléphone : chaque état 21..26 lance la bonne vidéo et son audio, retour historique correct après fin logique, charge corrected 2/3/4, aucune double bande-son, aura présente seulement lorsqu'un pouvoir peut réellement être lancé, voyant/admin corrects.


### CI #41 / #42
Le run #41 a été arrêté par le validateur qui cherchait encore la chaîne UI `20 taps bas-droite pour ouvrir`; la préparation et le code avaient réussi. Correctif CI seul dans f8e90d5. Sur le run #42, les étapes de préparation, inspection des hooks et validation Python/média/audio/pouvoirs/auras sont vertes. Aucune régression fonctionnelle identifiée à ce stade; FFprobe et Buildozer restent à terminer.


## 2026-10-02 — JT-CINEMATIC-FINISHING-001 — lecture complète, auras tournantes, protection orbes

Correction d'une mauvaise interprétation de 1.0.6 : les PNG stsf1/sth1/stta1/trfs1/trph1/trma1 sont les items/icônes, pas l'aura tournante. La vraie aura est b1s..b6s et ses frames select/select0..15.png. 1.0.7 corrige cela sans changer les items. Ajout d'un verrou de touches humaines pendant les cinématiques complètes et d'une protection d'orbes 2 s au démarrage de charge. Risques à valider téléphone : moteur historique peut continuer en arrière-plan pendant la cinématique ; vérifier que ce comportement reste cohérent, que toutes les vidéos vont jusqu'à EOS, que les finishing correspondent au bon vainqueur et qu'aucun tap caché n'agit.


## 2026-10-02 — JT-ORB-PROTECT-002 — défaut 1.0.7 détecté après CI

Le run #48 était vert mais son test ne vérifiait que des tokens. Inspection du main généré : les six arrêts humains étaient placés sous `_jt_touch_start_indexa!=1`; en phase orbes normale (`indexa==1`) l'utilisateur ne pouvait donc plus arrêter les orbes. De plus, aucun garde ne bloquait `haut[i]+=...` dans `colvv`, donc les orbes n'étaient pas figées. Correction 1.0.8 : protection armée sur la vraie transition `2/3/4 -> 1`, horloge Kivy `Clock.get_time()`, garde humaine stricte phase 1, `continue` avant mouvement/IA, pause des deux compteurs de phase. CI #49 ajoute un faux Clock avec tests de frontière (avant échéance=true, à l'échéance=false, hors indexa1=false), compte exactement six gardes humaines et interdit les anciennes chaînes. Run #49 terminé success sur toutes les étapes, y compris FFprobe, Buildozer, APK et uploads. Le diagnostic généré porte `game_executed=false` : aucune validation téléphone ne doit être revendiquée.


## 2026-10-02 — JT-FINISH-EOS-002 — cause de coupure confirmée sur téléphone

Symptôme Fab 1.0.8 : finishing T-Rex / Steg non joué jusqu'au bout. Cause prouvée dans le main généré : bloc historique `if indexa==10 or indexa==11` puis `if indexa>9 and anim1==longanim1[indexa]-3: indexa=0; anim1=0`. Le state 11 legacy est particulièrement plus court que le MP4 (104×~0,06 s ≈ 6,24 s contre 8,336009 s FFprobe). Le simple `play_to_end` du contrôleur vidéo ne suffit donc pas si l'UI historique quitte et reconfigure la scène derrière lui. Correctif 1.0.9 : geler l'animation historique 10/11 après première frame vidéo, puis libérer une seule fois au vrai EOS MP4. La CI #50 vérifie l'ordre du garde avant la sortie legacy et l'ordre `pending EOS` avant `_stop_scene`. Validation téléphone encore requise.

## 2026-10-02 — JT-PHASES-001 — audit et régressions reproduites

Base e60561d3a2ecaf3441b005cd2e5805ecfc030854, main historique explicite/hash vérifié; audit du code réel.

1. Le masque pouvoir omet rails/orbes/cibles/HUD; affpv réécrit les tailles toutes les0,5s après affbt. Un masque seulement dans affbt ne garantit pas l'exclusivité.
2. carupdate est programmé indépendamment du début réel de round; les gardes pouvoir/protection2s ne créent pas de pré-phase. Des écrivains UI reprennent quand indexa revient à1 avant EOS.
3. Un EOS de pouvoir court détruit le lecteur alors que indexa reste21..26; la synchronisation suivante peut recréer le même MP4. Reproduit par test, corrigé par scène terminée jusqu'au changement logique. Cela ne prouve PAS la cause du doublon T-Rex de Fab.
4. Le lancement IA depuis carupdate passe encore par le else car2=10 après indexa=22. Reproduction : car75/car2=3, énergie40,5 → soin ST2/coût40; ancien chemin car2=10, correctif conserve75/3 et énergie0,5.

Correction : phases, masque exhaustif après callbacks, chrono détenu par ROUND_ACTIVE, attente effet historique/EOS, synchronisation sur état vivant. Gardes finishing et génération players conservées.

Pendant développement : test supplémentaire a détecté un verrou EOS initial qui empêchait d'arrêter VV au timeout→menu; corrigé et testé. Dernière frame d'un MP4 court reste aspect-fill. 16 tests verts, main/runtimes compilables, assertions CI code/helpers existantes vertes. Kivy/vidéo simulés : aucun résultat acoustique ou visuel Android revendiqué.

Validation téléphone encore attendue. Ne pas annoncer le doublon vocal résolu. Les erreurs médias restent journalisées; les messages legacy génériques ne signifient pas que les banques prunées sont restaurées.

### JT-PHASES-001 — complément canvas et nettoyage tactile

Pendant le build du premier candidat df03316 (run54), dernière vérification des instructions canvas : coul/scr créent des Ellipse locales non référencées comme attributs root. Une telle géométrie persistante échappait au premier inventaire; test reproduit puis corrigé. Le blocage de on_touch_up pouvait aussi laisser son groupe canvas : conserver ce nettoyage historique, sans autoriser on_touch_down/move. Deux nouveaux tests échouaient avant, passent après; total18. Le candidat du run54 est donc remplacé pour la livraison finale, sans nouvelle version publique ni changement natif.
