# JT-SETS-001 — Lot 01 — Inventaire prouvé

Date : 2026-10-05
Mission : `JT-SETS-001`
Branche : `feature/dinosaur-sets-v1`
Base de mission : `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`

## 1. Baseline reproductible

### Source d’autorité

Le `app/main.py` Android n’est pas une source versionnée. Il est généré à partir de l’archive historique officielle `JuneTrex.zip` par `tools/prepare_android.py`.

Archive officielle, Release/tag `JTrex` :
- taille : `327992765` octets ;
- SHA-256 : `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.

Source historique `main.py` attendue par le préparateur :
- SHA-256 : `3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231`.

Main Android réellement préparé avec le code courant de la branche :
- SHA-256 : `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.

Le rapport `app/android-preparation.json` produit par la chaîne confirme les trois empreintes ci-dessus et indique notamment Python cible `3.12.14`, version application `1.0.15`, numeric version `115` et package `com.junedady.junetrex`.

### Exécution de preuve

Le conteneur de travail de cette session ne pouvait pas résoudre GitHub pour un `git clone` / `curl` direct. Ruling d’exécution : utiliser un workflow GitHub Actions temporaire sur la branche de mission afin d’exécuter exactement la génération contre la Release officielle, puis supprimer ce workflow avant clôture du Lot 01. Coût si ce choix était erroné : une différence d’environnement d’audit ; mitigation : même OS CI Ubuntu 24.04 que la chaîne Android et même `tools/prepare_android.py`, avec contrôle préalable taille/SHA de l’archive.

Workflow temporaire : `JT-SETS-001 Lot01 Diagnostic`.

Preuves fraîches :
- run #1 : `37339520665` — GREEN ;
- run #2 : `37339853652` — GREEN ;
- head du run #2 : `4b883f6e1fad5003426b598fbed0036a890039f3` ;
- vérification `ce858fe57b...` ancêtre de HEAD : PASS ;
- vérification taille/SHA archive : PASS ;
- préparation `JuneTrex.zip -> app/main.py` : PASS ;
- artefact de preuve run #2 : `JT-SETS-001-Lot01-Evidence`, id `11358400072`, SHA-256 d’artefact `734651b6f532aa6079f543ff2e1a27fce83fbb512fd542877466ab46eada5c21`.

Commande canonique exécutée :

```text
python3 tools/prepare_android.py --archive JuneTrex.zip --output app --spec buildozer.spec
```

`JuneTrex.zip` et `app/` restent des produits temporaires de génération et ne doivent pas être ajoutés au dépôt.

### Baseline de tests

Commande exécutée dans le run diagnostic :

```text
python3 -m unittest discover -s tests -v
```

Résultat : `Ran 38 tests` — `OK`.

Les tests comprennent notamment les gardes de taille des médias, le média d’attente canonique, le chrono orbes, les phases, le contrat KO/rounds et le modèle de round.

Deux `SyntaxWarning: invalid decimal literal` provenant du source historique généré sont visibles dans le harness ; ils n’ont provoqué aucun échec de test et ne sont pas modifiés dans ce lot d’audit.

## 2. Identités du duo canonique

Le main généré ne contient pas de chaîne d’affichage dédiée `Stegosaurus`, `Steg`, `T-Rex` ou `Tyrannosaurus`. Les camps sont identifiés fonctionnellement par :
- gauche : `ST`, énergie `stamg`, slots `1..3` ;
- droite : `TR`, énergie `stamd`, slots `4..6`.

La nomenclature visible du duo vient actuellement des noms de médias et de l’identité générale June T-Rex (`Steg...Trex...`). Conséquence pour le format v1 : les `display_name` des dinosaures doivent être des données explicites du set ; le moteur ne doit pas essayer de les reconstruire à partir des noms de fichiers ou des variables historiques.

Aucun portrait autonome de dinosaure exploité comme portrait de catalogue n’a été trouvé dans le main généré. Les anciennes séquences d’images des scènes (`dinos1`, `stsf`, `stls`, etc.) sont aujourd’hui des séquences legacy MP4-only/prunées et ne doivent pas être détournées en portraits. Le portrait reste donc optionnel dans le format v1.

L’icône Android `assets/icon/JtrexIcon.png` reste une ressource de l’application, pas l’icône d’un set.

## 3. Rôles média canoniques

Les politiques `loop`, `play_to_end`, verrouillage, première frame, audio et EOS sont des propriétés du moteur. Le set choisit uniquement la ressource correspondant au rôle logique.

| Rôle logique | États moteur | Fichier canonique | Politique moteur |
| --- | --- | --- | --- |
| `intros[]` | lancement | `assets/intro/JTrexintro1.mp4`, `JTrexintro2.mp4`, `JTrexintro3.mp4` | choix aléatoire, aspect-fit |
| `orbs_background` | 1 | `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` | boucle |
| `charge_red_blue` | 2,3,4 | `assets/combat/Chargestegtrexchargerougebleucorrected.mp4` | non boucle |
| `charge_yellow` | 5,6,7 | `assets/combat/Stegtrexegalitechargeboutonjaune.mp4` | non boucle |
| `verdict_draw` | présentation `-7` | `assets/combat/Zerowinstegtrexsurleschargedejaugejauneetbleuetrouge.mp4` | non boucle ; injecté actuellement par le runtime phase |
| `verdict_left` | 8 / ST | `assets/combat/Stegtrexresultstegwin.mp4` | non boucle |
| `verdict_right` | 9 / TR | `assets/combat/Stegtrexresulttrexwin.mp4` | non boucle |
| `finishing_left` | 10 / ST | `assets/finishing/steg-finishing-trex.mp4` | `play_to_end=True` |
| `finishing_right` | 11 / TR | `assets/finishing/trex-finishing-steg.mp4` | `play_to_end=True` |

Point d’architecture confirmé : `jtrex_phase_runtime.py::_install_zero_win_scene()` modifie actuellement le dictionnaire global `SCENES` pour ajouter `zero-win`. Cette mutation globale est un point à supprimer au Lot 02 afin qu’un set, un aperçu ou une session ne puisse pas polluer le catalogue d’une autre session.

## 4. Matrice des six pouvoirs

`POWER_COSTS={1:60,2:40,3:60,4:60,5:60,6:80}` est commun au moteur. L’activation reste strictement `énergie > coût`.

| Slot | Camp | État | Identité interne prouvée | Coût | MP4 canonique | Icônes historiques | Son d’activation | Audio legacy de scène |
| ---: | --- | ---: | --- | ---: | --- | --- | --- | --- |
| 1 | ST/gauche | 21 | `stsf` | 60 | `assets/powers/stsf-sanctuary-force.mp4` | `stsf1.png` / `stsf0.png` | `sf.wav` | `stsf.wav` |
| 2 | ST/gauche | 22 | `stls` | 40 | `assets/powers/stls-lifestream.mp4` | `sth1.png` / `sth0.png` | `ls.wav` | `stls.wav` |
| 3 | ST/gauche | 23 | `stta` | 60 | `assets/powers/stta-tornado-attack.mp4` | `stta1.png` / `stta0.png` | `ta.wav` | `stta.wav` |
| 4 | TR/droite | 24 | `trfs` | 60 | `assets/powers/trfs-fire-storm.mp4` | `trfs1.png` / `trfs0.png` | `fs.wav` | `trfs.wav` |
| 5 | TR/droite | 25 | `trph` | 60 | `assets/powers/trph-phoenix-attack.mp4` | `trph1.png` / `trph0.png` | `ph.wav` | `trph.wav` |
| 6 | TR/droite | 26 | `trma` | 80 | `assets/powers/trma-meteor-attack.mp4` | `trma1.png` / `trma0.png` | `ma.wav` (objet historique `maa`) | `trma.wav` |

Le mapping de lancement humain est directement visible dans le main généré : slots `1..3` débitent `stamg` puis passent respectivement en `21..23`; slots `4..6` débitent `stamd` puis passent en `24..26`. Le chemin IA utilise la même table de coûts et `indexa=20+i`.

### Sens des images de pouvoir

Les paires `*1.png` / `*0.png` ne sont pas des variantes « appui » et « disponibilité » :
- `*1.png` est affichée quand le slot n’a pas encore été utilisé ;
- `*0.png` est affichée quand `selected[slot]` est vrai, donc après utilisation.

La disponibilité réelle est un overlay séparé `b1s..b6s`, utilisant les images animées `select/select0.png` à `select/select15.png`; sa taille n’est non nulle que si `jt_power_available(slot)` est vrai.

Le slot 2 conserve un nom de fichier historique atypique `sth0.png` / `sth1.png` alors que son identité moteur/média est `stls`. Le format de set ne doit pas déduire l’identité d’un pouvoir depuis ce nom historique.

Le préparateur contient en outre une correction explicite de l’identité visuelle droite : slot 4 = `TRFS`, slot 6 = `TRMA`. Le main généré vérifié reflète bien cette correction.

### Libellés humains

Aucun texte de bouton contenant les noms des pouvoirs n’est trouvé dans le main généré. Les noms lisibles `Sanctuary Force`, `Lifestream`, `Tornado Attack`, `Fire Storm`, `Phoenix Attack`, `Meteor Attack` sont cohérents avec les noms des MP4 canoniques mais doivent devenir des champs explicites de manifeste ; ils ne seront pas reconstruits depuis le chemin du média.

## 5. Empreintes des médias canoniques

| Ressource | Taille | SHA-256 |
| --- | ---: | --- |
| `assets/intro/JTrexintro1.mp4` | 3278089 | `3f072bbaa2dcd961d5bf756168b40bd187ac06f61f133cbacb3fe114131e6bc0` |
| `assets/intro/JTrexintro2.mp4` | 2584105 | `c152f33e5b5c4773cdac69ce1be84ad99d05d54d51f735532a4d128fb0a7d310` |
| `assets/intro/JTrexintro3.mp4` | 3349412 | `4ba0dd3a14b00cf3f03a4a2a64e0e5cec1056e37ce41ed62d1e4b15acb007d28` |
| `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` | 9848376 | `71b1abe5498d7e9f5dfd61cccede099759c49ec0a82324e8dd76b8c054dccd9d` |
| `assets/combat/Chargestegtrexchargerougebleucorrected.mp4` | 833378 | `a7e379505123460803f5d2b244ffa8f24c2aa2a7380dee0f0b2e8adde8467862` |
| `assets/combat/Stegtrexegalitechargeboutonjaune.mp4` | 1432415 | `9f66ca15e0e3e376e029e8002a1588e379b0c6f3557f7118d00d729a2d04fedf` |
| `assets/combat/Zerowinstegtrexsurleschargedejaugejauneetbleuetrouge.mp4` | 1147683 | `798b4ac8605a599e29e7cdd1449741b25537d9654e529c687d825bf1f933ccfa` |
| `assets/combat/Stegtrexresultstegwin.mp4` | 1521350 | `e4399e90eaf5a698e5284335704202e01851141b57ab54a859c471a869e469a5` |
| `assets/combat/Stegtrexresulttrexwin.mp4` | 760242 | `3a786dd13f12aace72efe4be457d5dcc0272094024bfd5b1f80460452e273a57` |
| `assets/powers/stsf-sanctuary-force.mp4` | 2525411 | `c2e287425f9f2343c3a50c23428662b33db9afd77ff3380d933deec9e8f74cc4` |
| `assets/powers/stls-lifestream.mp4` | 2243703 | `f7d0ad630162ecf4135ec51541971b10da38ed62ac485d9770c063f555d876b7` |
| `assets/powers/stta-tornado-attack.mp4` | 2928334 | `cea65b5b2a8705101bef5b982032972e384f96024e5d01b5e5b752c6d3f682b9` |
| `assets/powers/trfs-fire-storm.mp4` | 2431111 | `632d661fc1ee7dbe3bd5768de6f1dd7dfd7504da3f001dbb8af13867a96b6c48` |
| `assets/powers/trph-phoenix-attack.mp4` | 1945922 | `d099068f109d00116031442dc472c1e3300795e1df83296b6cf28b94140e3b2c` |
| `assets/powers/trma-meteor-attack.mp4` | 2544535 | `11c5f05af8840b4f9f5d0fc0cf9ba45d80ce3af84d8acaacc77c08f96c102cf1` |
| `assets/finishing/steg-finishing-trex.mp4` | 2184229 | `ae9e28330da5db03c0ff68059794d4d070e643d08d2b3a1989946b7c5834be5a` |
| `assets/finishing/trex-finishing-steg.mp4` | 1834787 | `7f6e532092f5914854b61a97b329060edd23f2f40e2f041a2f4633c5ad19ee66` |

## 6. Empreintes des images de pouvoir historiques générées

| Image | Taille | SHA-256 |
| --- | ---: | --- |
| `stsf0.png` | 26201 | `66f940dacf991453c04c7d555257c0b40b0d0cdaab6182a5a6838f36cc386958` |
| `stsf1.png` | 34821 | `91e4f20b5b363e78ddf8701d8a139ec138564a07719612aa6689896afd7ee837` |
| `sth0.png` | 24704 | `1942a01a775233d7441715ec93eb2aab08fd53596309a5a8225ad247907ad2a7` |
| `sth1.png` | 34826 | `9b8f8ea93907b9f6b9fd03928ffdb01bf5d0e7cde9515632d41796345afa3fc5` |
| `stta0.png` | 21713 | `7b73d84d4e65a832686e34a5233b784065a8fc20332714013ee4bd0c3889a286` |
| `stta1.png` | 30457 | `93c589b6056a828464618e4fbcdd811072a774342dc6a59c02e79ac5a02e9a3f` |
| `trfs0.png` | 23568 | `323e546d252a649c96d1c39797380c696c93ddebf6fe911b36c91fb93a99f4f7` |
| `trfs1.png` | 32854 | `bd62802f334b1d4eccec6492cee9e8db21a0c6548b5daf1b20c16278d98266dd` |
| `trph0.png` | 26263 | `8b3e4a4be0c38e0acb2b8106e53a6f79fa3ec457be0a5ff2f0c4676721093380` |
| `trph1.png` | 36674 | `dc5b89d115ec5fdb418c344b344d9101d73143d4f1e1e63b0ddd9d8c2af49238` |
| `trma0.png` | 26139 | `124e45202c317af15f7d6a1f1ffa1c0a37dde08a0e45ad6dcac0fc74fcd5af64` |
| `trma1.png` | 37948 | `27a0a4a96a0f17120b5978d380266d92ccbbee91b82afdbf076942c9a626747b` |

## 7. Audio de pouvoirs

Deux niveaux audio existent aujourd’hui :
1. son court d’activation au clic/lancement (`sf.wav`, `ls.wav`, `ta.wav`, `fs.wav`, `ph.wav`, `ma.wav`) ;
2. audio legacy de scène référencé par `sona[21..26]` (`stsf.wav`, `stls.wav`, `stta.wav`, `trfs.wav`, `trph.wav`, `trma.wav`).

Le runtime MP4 démarre avec le volume natif à 0 puis active l’audio MP4 après la première vraie frame ; l’audio historique sert de fallback tant que la vidéo native n’est pas effectivement active.

## 8. Vérification Task 2

La suite complète fraîche contient et valide explicitement :
- `test_media_asset_size_guards.MediaAssetSizeGuardTests.test_declared_media_sizes_match_repository_assets` — PASS ;
- `test_orb_media_manifest.OrbMediaManifestCanon.test_beach_loop_is_guarded_by_android_media_manifest` — PASS ;
- `test_orb_media_manifest.OrbMediaManifestCanon.test_legacy_wait_media_is_retired_from_active_candidate` — PASS.

Les six slots, leurs camps, états, coûts, vidéos et identités visuelles sont donc inventoriés sans ambiguïté. Aucune règle de gameplay n’a été modifiée.

## 9. Mécanismes réels des six pouvoirs

### Jalons historiques

Les métadonnées du main généré sont :

| État | `longanim1` | `namea` | `genrea` | `deg[state]` | `sona` |
| ---: | ---: | --- | --- | ---: | --- |
| 21 | 242 | `stsf/stsf_` | `1x` | 181 | `stsf.wav` |
| 22 | 213 | `stls/stls_` | `1x` | 182 | `stls.wav` |
| 23 | 238 | `stta/stta_` | `1x` | 183 | `stta.wav` |
| 24 | 232 | `trfs/trfs_` | `1x` | 184 | `trfs.wav` |
| 25 | 230 | `trph/trph_` | `1x` | 185 | `trph.wav` |
| 26 | 239 | `trma/trma_` | `1x` | 186 | `trma.wav` |

Dans `anim_1`, l’effet est déclenché par l’égalité exacte `anim1 == deg[indexa]`. Pour les états 21..26, `deg` est donc un **numéro de jalon d’animation**, pas une quantité de dégâts.

### Effet brut par slot

Vie historique : `pvg=pvd=500000000`.

| Slot | État | Cible | Écriture brute au jalon | Base canonique | Sémantique |
| ---: | ---: | --- | --- | --- | --- |
| 1 / STSF | 21 | TR/droite | `degd += pvd/4` | 25 % de la vie max droite | dégâts bruts droite |
| 2 / STLS | 22 | ST/gauche | `degg -= pvg/4` | 25 % de la vie max gauche | soin gauche via réduction des dégâts cumulés |
| 3 / STTA | 23 | TR/droite | `degd += pvd/4` | 25 % de la vie max droite | dégâts bruts droite |
| 4 / TRFS | 24 | ST/gauche | `degg += pvg/4` | 25 % de la vie max gauche | dégâts bruts gauche |
| 5 / TRPH | 25 | ST/gauche | `degg += pvg/4` | 25 % de la vie max gauche | dégâts bruts gauche |
| 6 / TRMA | 26 | ST/gauche | `degg += pvg/3` | 33,333… % de la vie max gauche | dégâts bruts gauche |

Avec les vies canoniques actuelles, une base `1/4` représente 125 000 000 avant le traitement partagé et `1/3` environ 166 666 666,67.

### Traitement partagé dégâts / énergie

Après une variation de `degg` ou `degd`, le moteur historique exécute un traitement commun :
- pour tous les jalons sauf `182`, il calcule des gains d’énergie à partir des nouveaux deltas de dégâts (`/4000000` et bonus conditionnel `/10000000`) ;
- pour tous les jalons sauf `182`, il retire ensuite un quart du nouveau delta aux accumulateurs de dégâts, puis synchronise `degg0/degd0` ;
- l’énergie est ensuite bornée à `0..100`.

Conséquence : modifier une fraction de dégâts d’un pouvoir modifie **à la fois** les PV effectifs et la quantité d’énergie redistribuée. Ce n’est pas un paramètre purement cosmétique.

En l’absence d’un autre delta simultané, le passage partagé conserve 3/4 du delta brut dans l’accumulateur de dégâts après son lissage historique. Cette observation décrit le code actuel ; le contrat v1 n’expose pas cette formule au pack.

### Cas particulier Lifestream / état 22

Le jalon 182 est explicitement exclu du calcul de gain d’énergie et du lissage `/4`. Le main applique `degg -= pvg/4`, puis `affpv` borne `degg` à zéro si le soin ferait passer les dégâts cumulés sous zéro. Le pouvoir ne peut donc pas donner plus que la vie maximale : il soigne jusqu’à 25 % de la vie max, limité par les dégâts réellement subis.

### Unicité et réarmement

Chaque activation marque `selected[slot]=True`. La disponibilité canonique exige `not selected[slot]`; le slot ne peut donc pas être réactivé pendant le même vrai round/combat d’usage. Le runtime de phases réarme ces usages uniquement lors du vrai reset de round déjà canonique.

Les six scènes historiques sont `genrea='1x'`; leur effet est attaché au jalon numérique de l’animation historique. La vidéo MP4 ne définit pas ce jalon.

## 10. Séparation impact historique / EOS média

`jtrex_media_runtime.py` annonce et applique la règle suivante : l’EOS vidéo ne modifie pas la machine d’états historique. Pour les scènes `play_to_end` :
- le runtime média vérifie l’identité du lecteur et la génération de callback ;
- à EOS il appelle seulement `JTPhaseController.video_complete(state)` puis libère la scène ;
- `video_complete` marque `media_done/media_failed` ;
- aucun code EOS n’ajoute de dégâts, soin ou énergie.

`jtrex_phase_runtime.py` précise que le moteur legacy reste l’autorité des dégâts, énergie et jalons d’animation. Un pouvoir peut rendre un camp KO avant la fin du MP4 ; la phase POWER reste alors verrouillée jusqu’à EOS, puis le KO déjà observé est résolu sans réappliquer l’effet.

Conclusion contractuelle : **durée vidéo, EOS et position du lecteur ne sont jamais des paramètres d’impact**. Une vidéo plus longue ou plus courte ne déplace pas automatiquement le jalon historique.

## 11. Candidats de personnalisation — fermés en v1 tant que Fab ne valide pas

Chaque valeur ci-dessous est techniquement prouvée, mais reste `NON ÉDITABLE v1` jusqu’à validation explicite des champs et bornes par Fab.

| Candidat | Source prouvée | Type/unité | Valeur canonique | Conséquence d’un changement | Test d’équivalence canonique requis |
| --- | --- | --- | --- | --- | --- |
| `left_1.raw_damage_fraction` | état 21, `degd += pvd/4` | fraction vie max cible | `1/4` | dégâts TR + énergie dérivée + lissage partagé | état 21, mêmes PV/énergie avant/après avec profil canonique |
| `left_2.heal_fraction` | état 22, `degg -= pvg/4` | fraction vie max propre | `1/4` | soin ST, plafonné par `degg>=0`; pas de gain énergie au jalon 182 | cas dégâts suffisants + cas soin plafonné, mêmes PV/énergie |
| `left_3.raw_damage_fraction` | état 23, `degd += pvd/4` | fraction vie max cible | `1/4` | dégâts TR + énergie dérivée + lissage partagé | état 23, mêmes PV/énergie |
| `right_1.raw_damage_fraction` | état 24, `degg += pvg/4` | fraction vie max cible | `1/4` | dégâts ST + énergie dérivée + lissage partagé | état 24, mêmes PV/énergie |
| `right_2.raw_damage_fraction` | état 25, `degg += pvg/4` | fraction vie max cible | `1/4` | dégâts ST + énergie dérivée + lissage partagé | état 25, mêmes PV/énergie |
| `right_3.raw_damage_fraction` | état 26, `degg += pvg/3` | fraction vie max cible | `1/3` | dégâts ST + énergie dérivée + lissage partagé | état 26, mêmes PV/énergie |

Les coûts d’énergie ne font **pas** partie des paramètres éditables de cette première version : `60/40/60/60/60/80` reste moteur-owned.

## 12. Non-paramètres obligatoires

| Valeur historique | Signification prouvée | Statut format v1 |
| --- | --- | --- |
| `deg[21..26] = 181..186` | jalon/indice d’animation auquel le moteur applique l’effet | jamais paramètre d’équilibrage du pack |
| `longanim1[21..26]` | longueur historique de séquence d’animation | engine-owned ; ne suit pas la durée MP4 |
| `anim1` | curseur/compteur de frame historique | engine-owned |
| `indexa` | état de la machine historique | engine-owned |
| `21..26` | identifiants d’états des six mécanismes | engine-owned |
| durée MP4 | durée de présentation audiovisuelle | ressource validée, jamais base de calcul gameplay |
| EOS | événement de fin de présentation | verrou/libération uniquement ; aucun effet gameplay |
| `play_to_end`, `loop` | politiques de lecture du moteur | engine-owned |
| `selected`, réarmement | unicité d’usage du slot et cycle de round | engine-owned |

## 13. Vérification Task 3

La preuve fraîche `python3 -m unittest discover -s tests -v` contient :
- 19 tests `test_phase_integration` — PASS ;
- 7 tests `test_round_ko_contract` — PASS ;
- 5 tests `test_round_model` — PASS ;
- 4 tests `test_orb_presentation` — PASS.

Le sous-ensemble demandé par le plan est donc inclus intégralement dans la suite fraîche GREEN. Aucun changement de phase, KO, chrono ou gameplay n’a été nécessaire pour produire cet inventaire.
