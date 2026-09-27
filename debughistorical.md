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
