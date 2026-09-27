# JTrex / June T-Rex — Brainmap technique

## 1. Référence et périmètre

Dépôt : https://github.com/greenpower2669/JTrex

Révision de référence de main :
164d03be77c83f49e1094294f36f860ec183df68

Release :
https://github.com/greenpower2669/JTrex/releases/tag/JTrex

Archive :
https://github.com/greenpower2669/JTrex/releases/download/JTrex/JuneTrex.zip

Fichiers étudiés :

- JuneTrex/main.py — 73 507 octets, 2 523 lignes ;
- JuneTrex/main.kv ;
- JuneTrex/android.txt ;
- buildozer.spec ;
- .github/workflows/android.yml ;
- inventaire des ressources de JuneTrex.

SHA-256 du main.py :
3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231

main est actuellement essentiellement un lanceur documentaire/build : README.md, LICENSE, buildozer.spec et workflow. Le programme est dans l'archive de release.

Attention : « June air hockey » contient aussi un main.py. Ne pas le confondre avec JuneTrex/main.py.

## 2. Architecture Kivy

Technologie :

- Python ;
- Kivy ;
- jah(FloatLayout) : interface et majorité du moteur ;
- mainApp(App) : cycle Kivy ;
- Rectangle, Color, Ellipse, Point : dessin ;
- SoundLoader : audio ;
- Clock : callbacks périodiques.

main.kv contient les directives Kivy et une règle <jah> vide ; il n'héberge pas une interface complète parallèle.

android.txt :

- title=main ;
- author=junedady ;
- orientation=landscape.

mainApp.build() retourne jah().
mainApp.on_pause() retourne True sans resynchronisation détaillée des timers/animations/sons identifiée.

## 3. Table des responsabilités

| Élément | Responsabilité |
|---|---|
| jah.__init__ / init historique | création rectangles, commandes, jauges, textes, états graphiques |
| jah.on_touch_down | arrêt des orbes, tapotement, pouvoirs, options/menu |
| jah.on_touch_move | suivi tactile, notamment moteur hérité |
| jah.on_touch_up | relâchement, apparence boutons, libération toucher |
| jah.colvv | mouvement des orbes, IA d'arrêt, arrêt forcé, fin saisie |
| colpts | scores des deux camps et choix résultat |
| asb | appréciation S/AAA/.../F et sons |
| jah.anim_1 | progression des séries, impact, son, dégâts, énergie |
| jah.mc1 | détection fin de combat et appel de anim_1 |
| jah.affbt | visibilité selon état et réinitialisations menu |
| jah.affpv | jauges vie/énergie, disponibilité pouvoirs |
| jah.carupdate | car/car2 et déclenchement pouvoirs IA |
| computer | décision d'arrêt et tirage pour capacités IA |
| rr | pseudo-aléatoire fondé sur l'horloge |
| jah.screen_up | moteur air hockey hérité, toujours planifié |
| jah.ga / jah.da / jah.pter | animations secondaires héritées |
| collide | proximité circulaire des commandes |
| calculate_points / tantemps / vectoriser / radc / raddif / collidedif / verifdif | utilitaires moteur hérité |
| cleanchangecoul | nettoyage groupes graphiques |

Fonctions définies mais non identifiées comme planifiées activement : savemc1, vvincrem, restart et divers utilitaires historiques. Toujours garder la distinction entre définition, appel et planification.

## 4. Variables structurantes

| Variable | Rôle |
|---|---|
| indexa | état / séquence actuelle |
| anim1 | indice d'image courant |
| anim1vv | direction de lecture +1/-1 |
| indexa0 | dernier état vu par affbt |
| namea | préfixe de série |
| longanim1 | limite déclarée de série |
| genrea | mode de lecture |
| deg | indice d'événement/impact, pas un montant de dégâts |
| sona | bande-son liée à l'état |
| haut[1..6] | Y des six orbes |
| haut[7] | Y cible |
| haut[8], haut[9] | limites mouvement |
| col[1..6] | X des orbes |
| colv[1..6] | pas |
| colvv[1..6] | sens |
| colstop[1..6] | mobile/arrêté |
| stopg, stopd | trois orbes du camp notés |
| tapg, tapd | compteurs tapotement |
| pvg, pvd | capital initial de vie |
| degg, degd | dégâts cumulés gauche/droite |
| degg0, degd0 | références de variation |
| deggt, degdt | montants temporaires, convention dépendant du chemin |
| stamg, stamd | énergie |
| staminag, staminad | indicateur jauge pleine |
| selected[1..6] | pouvoir déjà utilisé |
| select[1..6] | mise en évidence disponibilité |
| bonus[1..6] | garde tactile des pouvoirs |
| vsg, vsd | contrôle IA |
| lvlg, lvld | niveau 1..5 |
| car | temps global de phase active |
| car2 | délai de saisie des orbes |

Ne pas interpréter deggt/degdt uniquement par leur nom : les chemins normaux et tapotement utilisent des conventions différentes.

## 5. Matrice d'états et séries

| État | Préfixe | Limite | deg | Son | Mode / rôle |
|---:|---|---:|---:|---|---|
| 0 | insertcoin/insertcoin_ | 11 | 300 | jtrm0.wav | menu figéf |
| 1 | dinos1/dinos_ | 59 | 180 | jtrm1.wav | orbes, vv |
| 2 | chargetr/chargetrwin_ | 128 | 88 | jtrm3.wav | RB victoire droite |
| 3 | chargest/chargetrwin_ | 128 | 87 | jtrm3.wav | RB victoire gauche |
| 4 | horseg2ko/chargetrwin_ | 105 | 85 | jtrm3.wav | RB neutre / démarrage |
| 5 | egtrwin/egtrwin_ | 9128 | 800 | jtrm7.wav | jaune gauche, branche spéciale |
| 6 | egtrwin/egtrwin_ | 152 | 130 | jtrm7.wav | jaune droite |
| 7 | eg2ko/eg2ko_ | 153 | 129 | jtrm7.wav | jaune neutre / égalité |
| 8 | stwin/stwin_ | 193 | 118 | jtrm8.wav | échange gagné gauche |
| 9 | trwin/trwin_ | 195 | 94 | jtrm9.wav | échange gagné droite |
| 10 | finishst/finishst_ | 165 | 918 | jtrm10.wav | fin |
| 11 | finishtr/finishtr_ | 104 | 194 | jtrm11.wav | fin |
| 21 | stsf/stsf_ | 242 | 181 | stsf.wav | pouvoir G1 |
| 22 | stls/stls_ | 213 | 182 | stls.wav | pouvoir G2 / soin |
| 23 | stta/stta_ | 238 | 183 | stta.wav | pouvoir G3 |
| 24 | trfs/trfs_ | 232 | 184 | trfs.wav | pouvoir D1 |
| 25 | trph/trph_ | 230 | 185 | trph.wav | pouvoir D2 |
| 26 | trma/trma_ | 239 | 186 | trma.wav | pouvoir D3 |

Le champ deg est un indice d'événement. Un indice non atteint dans un chemin normal n'implique pas un impact effectivement joué.

## 6. Callbacks Clock et dépendances temporelles

Planification dans mainApp.on_start :

| Méthode | Intervalle demandé |
|---|---:|
| screen_up | 0,04 s |
| ga | 0,04 s |
| pter | 0,05 s |
| da | 0,04 s |
| colvv | 0,04 s |
| affpv | 0,5 s |
| mc1 | 0,03 s |
| affbt | 0,05 s |
| carupdate | 1 s |

Ce ne sont que des fréquences nominales. Orbes, images, interface, jauges et compteurs ne sont pas mis à jour dans une boucle atomique unique.

mc1 peut appeler anim_1(True) ou anim_1(False) selon le retard observé ; la logique continue d'avancer même lorsque l'image n'est pas changée.

## 7. Correspondances tactiles

| Côté | Rouge | Vert | Bleu | Jaune |
|---|---|---|---|---|
| Gauche | gr / orbe1 | gg / orbe2 | gb / orbe3 | gj / tap jaune |
| Droite | dr / orbe4 | dg / orbe5 | db / orbe6 | dj / tap jaune |

En indexa=1, rouge/vert/bleu arrêtent leurs orbes.
En indexa 2/3/4, rouge ou bleu incrémente le compteur du camp si anim1<84.
En indexa 5/6/7, jaune incrémente le compteur si anim1<127.

Les zones de menu, niveaux, IA et pouvoirs sont aussi testées manuellement dans on_touch_down ; l'absence d'un widget Button signifie que la visibilité graphique n'est pas une garde d'interaction.

## 8. Organigramme — menu et cycle complet

~~~mermaid
flowchart TD
    A[Application démarre] --> B[indexa=0 menu]
    B --> C[Choix humain/ordinateur G et D]
    B --> D[Choix niveau S A B C D G et D]
    B --> E{Start et anim1=11 ?}
    E -- non --> B
    E -- oui --> F[indexa=4 sans reset explicite de anim1]
    F --> G[Impact partagé de séquence initiale]
    G --> H[indexa=1 phase orbes]
    H --> I{Six orbes arrêtés ?}
    I -- non --> H
    I -- oui --> J[colpts compare Sg/Sd]
    J --> K[indexa 7 égalité ou 8 gauche ou 9 droite]
    K --> L[Séquence / impact]
    L --> M{Une vie <1 ?}
    M -- non --> H
    M -- oui gauche --> N[indexa=11]
    M -- oui droite --> O[indexa=10]
    N --> P[Retour indexa=0 à longanim1-3]
    O --> P
    P --> B
~~~

## 9. Organigramme — arrêt des orbes et comparaison

~~~mermaid
flowchart TD
    A[indexa=1] --> B[Chaque colvv: déplacer les orbes mobiles]
    B --> C{Humain appuie R/V/B ?}
    C -- oui --> D[colstop de l'orbe=True]
    C -- non --> E{Camp IA ?}
    E -- oui --> F[computer distance,niveau]
    F --> G{Arrêt accepté ?}
    G -- oui --> D
    G -- non --> B
    E -- non --> B
    D --> H{3 orbes du camp arrêtés ?}
    H -- oui --> I[asb + stopg/stopd=True]
    H -- non --> B
    I --> J{6 orbes arrêtés ?}
    J -- non --> B
    J -- oui --> K[Calcul e_i=abs haut_i-haut_7]
    K --> L[S=max 0,150M-somme e_i^3]
    L --> M{abs Sg-Sd <20000 ?}
    M -- oui --> N[indexa=7]
    M -- non et Sg>Sd --> O[indexa=8; degdt=Sg]
    M -- non et Sd>Sg --> P[indexa=9; deggt=Sd]
    N --> Q[anim1=0; anim1vv=+1]
    O --> Q
    P --> Q
~~~

## 10. Organigramme — confrontation rouge/bleu

~~~mermaid
flowchart TD
    A[indexa dans 2,3,4 et anim1<84] --> B{Appui rouge ou bleu}
    B -- gauche --> C[tapg++]
    B -- droite --> D[tapd++]
    C --> E[Comparer tapg/tapd]
    D --> E
    E --> F{Avance strictement positive ?}
    F -- non --> A
    F -- oui --> G[indexa=4]
    G --> H{tapg-tapd >2 ?}
    H -- oui --> I[indexa=3; deggt=tapg*2M; degdt=0]
    H -- non --> J{tapd-tapg >2 ?}
    J -- oui --> K[indexa=2; degdt=tapd*2M; deggt=0]
    J -- non --> A
    I --> L[Conserver anim1, bifurcation en cours]
    K --> L
~~~

## 11. Organigramme — confrontation jaune

~~~mermaid
flowchart TD
    A[indexa dans 5,6,7 et anim1<127] --> B{Appui jaune}
    B -- gauche --> C[tapg++]
    B -- droite --> D[tapd++]
    C --> E[Comparer tapg/tapd]
    D --> E
    E --> F{Une avance >0 ?}
    F -- oui --> G[indexa=7]
    F -- non --> A
    G --> H{tapg-tapd >2 ?}
    H -- oui --> I[indexa=5; deggt=tapg*2M; degdt=0]
    H -- non --> J{tapd-tapg >2 ?}
    J -- oui --> K[indexa=6; degdt=tapd*2M; deggt=0]
    J -- non --> A
    I --> L{anim1 >127 ?}
    L -- oui --> M[anim1=85; indexa=3; degd += deggt; deggt=0]
    L -- non --> A
~~~

## 12. Organigramme — disponibilité et effet des pouvoirs

~~~mermaid
flowchart TD
    A[indexa=1] --> B{Energie >60 ?}
    B -- non --> A
    B -- oui --> C{Pouvoir selected=False ?}
    C -- non --> A
    C -- oui --> D[select/bonus rendent la capacité disponible]
    D --> E{Humain appuie ou IA computer accepte}
    E -- non --> A
    E -- oui --> F[stam -=60; selected=True; indexa=21..26]
    F --> G[anim_1 poursuit avec anim1/anim1vv hérités]
    G --> H{Indice deg atteint ?}
    H -- non --> G
    H -- oui --> I{Etat 22 ?}
    I -- oui --> J[degg -= pvg/4; traitement spécial à vérifier]
    I -- non --> K[Ajouter dégâts pvd/4, pvg/4 ou pvg/3 selon état]
    J --> L[Fin séquence puis retour vers indexa=1]
    K --> M[Traitement ordinaire dégâts/énergie]
    M --> L
~~~

## 13. Organigramme — fin de combat

~~~mermaid
flowchart TD
    A[Début mc1] --> B[compg=pvg-degg; compd=pvd-degd]
    B --> C{compg <1 ?}
    C -- oui --> D[indexa=11; anim1=2; anim1vv=1; dégâts remis à zéro]
    C -- non --> E{compd <1 ?}
    D --> E
    E -- oui --> F[indexa=10; anim1=0; anim1vv=1; dégâts remis à zéro]
    E -- non --> G[Continuer anim_1]
    F --> H{anim1 == longanim1[indexa]-3 ?}
    D --> H
    H -- oui --> I[indexa=0]
    H -- non --> J[Continuer séquence finale]
    I --> K[affbt réinitialise énergie pouvoirs dégâts car]
    K --> L[Humain/IA et niveaux conservés]
~~~

Note : comme les deux tests de vie sont indépendants, une mort simultanée peut passer d'abord par indexa=11 puis finir à indexa=10.

## 14. Lecteur de séquences

anim_1 :

1. mémorise le préfixe de l'état courant ;
2. teste l'impact anim1==deg[indexa] ;
3. avance anim1 selon anim1vv ;
4. gère limites et transitions ;
5. change éventuellement l'image ;
6. traite dégâts et énergie.

Risque de transition : indexa et anim1 peuvent changer après mémorisation du préfixe ; une image peut donc combiner ancien préfixe et nouvel indice.

Mode vv : inversion en haut, puis inversion lorsque anim1 redescend sous 1.
Mode 1x : fin → anim1=0, indexa=1, six colstop=False, sauf branches spéciales documentées.

## 15. Moteur air hockey hérité

Toujours planifié :

- screen_up 0,04 s ;
- ga 0,04 s ;
- da 0,04 s ;
- pter 0,05 s.

Données :

- palet : pavx,pavy,vpavx,vpavy,fpav ;
- poignées : xh,yh,xb,yb ;
- forces : fh,fb ;
- accélérations : acch,accb ;
- traces : h,b ;
- collisions/verrous historiques ;
- score sch/scb ;
- visuels pavé,vh,vb,jh,jb,gagn,win.

La logique continue même lorsque les visuels sont masqués. Ce bloc doit rester cartographié jusqu'à ce que ses dépendances tactiles et d'état soient validées.

pbt est forcé False dans les deux branches du test correspondant ; les anciennes branches de but qui exigent pbt=True ne sont normalement pas atteintes.

## 16. Ressources sensibles

Références actives dont la casse diffère de l'inventaire :

- code demande a.png ; archive contient A.png ;
- code demande boutbleu0.png ; archive contient boutBleu0.png.

Absence confirmée :

- horseg2ko/chargetrwin_83.jpeg.

Ne pas classer les références commentées tombe.wav, tamb.wav, engo.wav ou mil.wav au même niveau de dépendance active.

Aucun mp4, avi, mov, mkv ou webm n'a été trouvé dans JuneTrex. Cela ne prouve pas que les originaux n'existent pas ailleurs.

## 17. Chemin Android actuel

main du dépôt
→ workflow android.yml
→ téléchargement de JuneTrex.zip depuis la release
→ décompression
→ recherche du premier main.py
→ copie du dossier qui le contient
→ remplacement/ajout de buildozer.spec
→ Buildozer debug
→ artefact APK + log si réussite.

Point critique : plusieurs main.py existent dans l'archive. Le workflow ne sélectionne pas explicitement JuneTrex/main.py.

Configuration actuelle : Android API 36, min API 21, NDK 28c, arm64-v8a + armeabi-v7a, SDL2, APK debug, AAB release.

Cette cartographie ne constitue pas une validation du build.


## 18. Compléments de cartographie issus de l'audit de complétude

- L'essentiel de l'état actif est stocké dans des variables globales et des dictionnaires ; la future architecture ne doit pas supposer un état déjà encapsulé.
- choixidh / choixidb appartiennent au suivi tactile historique. Ils ne constituent pas un verrou global « un doigt par camp ».
- colv[7], colv[8] et colv[9] suivent une notion temporelle, mais colvv n'utilise pas cette information pour convertir les pas des orbes en vitesse normalisée au delta temps.
- Le suivi tactile hérité emploie les conventions h/b et certaines conditions diffèrent entre on_touch_down et on_touch_move ; ne pas homogénéiser ces chemins sans validation.
- L'inventaire signale des variantes de noms et des fichiers de sauvegarde dans la famille horseg2ko ; chargetrwin_83.jpeg reste absent et aucune variante ne doit être substituée automatiquement.
- Le hash SHA-256 documenté concerne JuneTrex/main.py seulement. L'archive JuneTrex.zip entière n'a pas été téléchargée puis rehachée dans l'audit Astra.
- L'analyse n'a pas comparé les onze main.py historiques ni inspecté visuellement chaque image de chaque série.


## 19. JT-ANDROID-001 — point de départ technique

Branche de travail : `port/android-first-apk`.
SHA de départ : `379ae278f2199cad26f1746c418512f47e04d106`.

Release source figée : tag `JTrex`, asset `JuneTrex.zip`.
Métadonnées GitHub vérifiées par Sol :
- taille : 327 992 765 octets ;
- digest publié : `sha256:f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.

Le hash historique `3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231` de `JuneTrex/main.py` reste la référence issue de l'audit Astra. Sol n'a pas pu rematérialiser l'archive binaire dans son environnement courant et ne prétend donc pas avoir recalculé ce hash.

Configuration actuelle observée :
- June T-Rex / com.junedady.junetrex / version 1.0 ;
- Python + Kivy, SDL2 ;
- API 36, min API 21, NDK 28c ;
- arm64-v8a + armeabi-v7a ;
- APK debug, AAB release ;
- aucune icône Android explicite dans buildozer.spec.

Workflow actuel à corriger avant usage de référence :
- dépend de `releases/latest` ;
- recherche le premier `main.py` trouvé après extraction.
Ces deux points sont incompatibles avec JT-ANDROID-001, qui exige le tag/source figés et la racine explicite `JuneTrex`.


## 20. JT-ANDROID-001 — préparation appliquée

Nouveaux/anciens fichiers de contrôle :
- `tools/prepare_android.py` : prépare une copie de compilation vérifiée ; bibliothèque standard Python uniquement ;
- `buildozer.spec` : version 1.0.1, numeric version 101, icône provisoire `pter/pter0.png` ;
- `.github/workflows/android.yml` : téléchargement figé sur la release/tag `JTrex`, préparation explicite puis build debug.

La préparation refuse :
- une archive de taille/hash différents ;
- une racine sans `JuneTrex/main.py` ;
- un `main.py` au hash historique différent ;
- un nombre d'occurrences inattendu pour les corrections de casse ;
- une destination déjà existante ;
- une identité Buildozer différente de `com.junedady.junetrex`.

`horseg2ko/chargetrwin_83.jpeg` reste une ressource connue manquante. Aucun fallback n'est créé dans cette étape.

La chaîne n'est pas encore déclarée entièrement reproductible : Buildozer est installé depuis Git et python-for-android n'est pas encore verrouillé. Les révisions réellement utilisées doivent être relevées après le build.


## 21. JT-ANDROID-001 — chaîne réellement observée au run #7

Run GitHub Actions : `36319044247`.
Commit : `e702da7c07e63ee760dbfe677a9d9062f6c7d587`.

Préparation :
- archive SHA-256 vérifiée ;
- main historique SHA-256 vérifié ;
- 3186 fichiers extraits ;
- main préparé SHA-256 : `29e6dabe2625778a36812652c16d227541aa9e6e002bc8ae493957fd87bf0034` ;
- buildozer.spec SHA-256 : `bf0089328295fb19637d0fa04a68c383172d9682af5d32947d674cbd444ef2cd`.

Outillage réellement relevé :
- Buildozer commit `a153097b3c534bea8a17da2abf1369d67c8cbfcb` ;
- python-for-android commit `58d21141f17c889bf8585f5665921d72028f8831` ;
- Cython 0.29.34 ;
- setuptools 84.0.0 ;
- wheel 0.48.0 ;
- runner Ubuntu 24.04 ;
- Java 17 ;
- NDK Buildozer r28c.

Échec : phase native python-for-android/libffi pendant `autoreconf`, avant packaging APK.


## 22. JT-ANDROID-001 — essai libltdl-dev

Modification ciblée du workflow :
`autoconf libtool pkg-config ...`
devient
`autoconf libtool libltdl-dev pkg-config ...`.

Hypothèse : `libltdl-dev` fournit `ltdl.m4`, contenant la macro libtool requise par l'étape Autoconf de libffi.

Critère de réussite : l'étape `autoreconf` de libffi franchit l'erreur `LT_SYS_SYMBOL_USCORE`. Toute nouvelle erreur ultérieure sera traitée séparément.


## 23. JT-ANDROID-001 — run #8

Run GitHub Actions : `36322734005`.
Commit : `808268924af4c09ea5218e549e77bde9bcf73242`.

Résultat discriminant :
- `libltdl-dev` installé avec succès ;
- aucune occurrence de `LT_SYS_SYMBOL_USCORE` dans le journal ;
- Buildozer et python-for-android inchangés :
  - Buildozer `a153097b3c534bea8a17da2abf1369d67c8cbfcb`
  - python-for-android `58d21141f17c889bf8585f5665921d72028f8831`
- la préparation JuneTrex est identique au run #7 ;
- la compilation a progressé jusqu'à la construction d'un environnement Python 3.14.2 interne à python-for-android.

Nouveau blocage :
`ImportError: cannot import name 'BuildDependencyInstallError' from 'pip._internal.exceptions'`.

Le contexte montre l'échec lors de la commande interne :
`source venv/bin/activate && pip install -U pip`.


## 24. JT-ANDROID-001 — patch p4a venv --clear

Base p4a figée pour le test :
`58d21141f17c889bf8585f5665921d72028f8831`.

Patch conservé dans :
`tools/patches/p4a-venv-clear.patch`.

Le workflow préclone `python-for-android` sur la branche `master`, remet le dépôt exactement au SHA de base, vérifie `git apply --check`, applique le patch puis enregistre le diff effectif dans `p4a-patch.txt`.

Buildozer conserve sa configuration actuelle et réutilise ce dépôt p4a déjà présent dans son répertoire de plateforme. Le seul changement de comportement p4a est :
`python -m venv venv`
→
`python -m venv --clear venv`.

La commande `pip install -U pip` reste inchangée pour rendre le test discriminant.


## 25. JT-ANDROID-001 — run #9 réussi

Run GitHub Actions : `36330526427`.
Commit : `716093bbea45766c7ee6d28ae0bb15b5512d943a`.

Résultat :
- étape p4a patchée : succès ;
- `Build debug APK` : succès ;
- collecte APK : succès ;
- upload APK : succès.

Artefact Actions APK :
- nom : `JuneT-Rex-1.0.1-debug`
- artifact ID : `10935915514`
- fichier : `JuneT-Rex-1.0.1-debug.apk`
- taille : 297060998 octets
- SHA-256 APK : `e9ca9935c79616868969dfe249a4a3afcd945c06d37392fb7ab3d8055057011c`
- ABIs présents : `arm64-v8a`, `armeabi-v7a`
- intégrité ZIP APK : OK.

Signature observée :
- certificat : `Android Debug`
- SHA-256 certificat : `C0:EE:36:F2:D9:D5:48:A7:CB:86:F2:F2:ED:71:FE:62:F9:E6:61:83:15:40:EF:AC:A3:39:27:08:B9:38:0D:63`.

Cette signature debug est propre au candidat de test et ne doit pas être présentée comme une signature de distribution pérenne.


## 26. Mission vidéo — organisation des nouveaux médias

Ressources importées dans la branche Android sans fusion de `main` :
- `assets/icon/JtrexIcon.png`
- `assets/intro/JTrexintro1.mp4`
- `assets/intro/JTrexintro2.mp4`
- `assets/intro/JTrexintro3.mp4`
- `assets/combat/StegVsTrexvaetviensremolace.mp4`

Avant intégration, le workflow relève les métadonnées avec ffprobe, extrait des images début/milieu/fin et capture les zones pertinentes du `main.py` préparé dans `main-hooks.txt`.

Aucune de ces vidéos n'est encore copiée dans `app/` ni activée par le moteur à ce stade d'intake.


## 27. JT-MEDIA-001 — architecture runtime vidéo

Le préparateur copie les cinq nouveaux médias et `jtrex_media_runtime.py` dans la racine de compilation vérifiée.

`mainApp.on_start` :
intro aléatoire → overlay Kivy noir/letterbox → fin/erreur/timeout → activation unique des callbacks historiques et de jtrm0.wav.

`mc1` synchronise seulement l'état visuel avec le contrôleur média :
- `indexa=1` → CoreVideo en boucle sur `StegVsTrexvaetviensremolace.mp4` ;
- sortie de `indexa=1` → unload immédiat, restauration du Rectangle historique ;
- `anim_1` continue toute sa logique mais n'écrase pas la texture du Rectangle tant que la vidéo d'attente fournit les frames.

Provider visé : Kivy ffpyplayer. La chaîne p4a reste figée sur `58d2114…`, avec recette FFmpeg 6.1.2 issue de p4a `541fe992…` pour éviter l'incompatibilité publique ffpyplayer 4.5.1 / FFmpeg 8.0.1.


## 28. JT-MEDIA-001 — test Python 3.11.13

Configuration candidate :
- p4a base : `58d21141f17c889bf8585f5665921d72028f8831` ;
- patch p4a : `venv --clear` conservé ;
- Python cible : `python3==3.11.13` ;
- hostpython3 : `VERSION_hostpython3=3.11.13` ;
- ffpyplayer : recette p4a 4.5.1 ;
- FFmpeg : recette 6.1.2 issue de `541fe992…`.

Le pin python3 est transmis par les requirements p4a ; hostpython3 est fixé explicitement dans l'environnement du build afin de respecter la garde p4a exigeant les deux versions identiques.


## 2026-09-28 — FAB-DEBUG-001 / JT-MEDIA-001

`buildozer.spec` → Python cible/host 3.12.14 → préparation Android existante → p4a figé → ffpyplayer 4.5.1 → APK 1.0.2 si toute la chaîne passe.

Point de contrôle connu avant run : `tools/prepare_android.py` vérifie encore explicitement 3.11.13 ; ne pas le corriger dans le même essai.


### Run #13 — résultat

`buildozer.spec 3.12.14` → **blocage dans prepare_android.py (garde 3.11.13)** → p4a non atteint → ffpyplayer non atteint → APK non produit.
