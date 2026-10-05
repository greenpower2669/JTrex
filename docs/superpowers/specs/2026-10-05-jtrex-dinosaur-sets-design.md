# JTREX — JT-SETS-001 — Design des sets de dinosaures

Date : 2026-10-05
Statut : design approuvé par Fab, implémentation à planifier
Branche cible : `feature/dinosaur-sets-v1`
Base vérifiée : `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`

## 1. But

Ajouter des sets de confrontations de dinosaures portables et DATA-ONLY autour du moteur June T-Rex existant, sans dupliquer le gameplay.

Un set représente un duo complet gauche/droite et fournit uniquement les différences autorisées : identités, médias, images de pouvoirs, et paramètres explicitement exposés par le moteur.

Le moteur reste l’unique autorité pour les phases, transitions, KO, rounds, pouvoirs, EOS, protections tactiles, chrono, score et verrouillages vidéo.

## 2. Contraintes canoniques non négociables

Le set canonique doit rester comportementalement identique à la référence actuelle.

Sont conservés notamment :
- 3 orbes par camp ;
- 10 s complets pour chaque nouvel échange ;
- retour de pouvoir avec temps restant ;
- verdicts de jauge distincts des victoires de round ;
- KO réel seul = victoire de round ;
- 2 rounds gagnés = victoire du match ;
- énergie remise à 0 au vrai nouveau round ;
- vie initiale 500000000 par camp ;
- score `max(0, 150000000 - somme(erreur^3))` ;
- égalité si différence absolue strictement inférieure à 20000 ;
- coûts slots 1..6 = 60, 40, 60, 60, 60, 80 ;
- activation strictement `énergie > coût` ;
- énergie fractionnaire ;
- effets appliqués une seule fois et jamais à EOS ;
- vidéos de pouvoirs/finishings jouées jusqu’à EOS réel quand requis ;
- intros aspect-fit, scènes de combat aspect-fill ;
- audio MP4 activé après première vraie frame ;
- protections de génération/callbacks, masques HUD et nettoyage tactile actuels.

## 3. Architecture retenue

### 3.1 Séparation moteur / set

Architecture choisie : adaptateur DATA/MEDIA devant le moteur historique.

Le manifeste sélectionne des ressources et des valeurs explicitement autorisées. Il ne décrit jamais une machine d’états, un callback, une formule exécutable ou un script.

Le moteur conserve :
- les états et transitions ;
- la politique de lecture des scènes ;
- les verrouillages ;
- la reprise du fond orbes ;
- les règles EOS ;
- les jalons d’impact ;
- les mécanismes des pouvoirs ;
- le KO, rounds et victoire de match.

Alternatives écartées :
1. un `main.py` ou gameplay par set : divergence et maintenance non maîtrisable ;
2. un manifeste capable de redéfinir `SCENES`, les transitions ou les effets : surface de régression trop grande sur KO/EOS/phases.

### 3.2 Composants prévus

Noms indicatifs, à confirmer pendant le Lot 01 :
- `tools/jtrex_sets_runtime.py` : contrat, catalogue, validation de manifeste, résolution logique et sélection figée ;
- `tools/jtrex_sets_io.py` : stockage, import/export, staging transactionnel ;
- `tools/jtrex_sets_admin.py` : atelier admin, brouillons, aperçu indépendant et mode test ;
- `assets/sets/catalog.json` : catalogue officiel embarqué ;
- `assets/sets/trex_vs_steg/manifest.json` : manifeste du set canonique.

Ces modules seront injectés dans la préparation Android comme les runtimes existants ; `app/main.py` reste généré et n’est pas une source versionnée.

## 4. État réel vérifié du dépôt

- `main` pointe sur `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Son parent est `976344c39dec9bb88ef8f7e18e703f2ed2659d07`, base fonctionnelle du build #78.
- Le build #78 / run `37245309424` est vert côté CI mais les mémoires vivantes indiquent encore une validation téléphone en cours.
- `app/main.py` n’est pas versionné ; le workflow télécharge `JuneTrex.zip`, puis exécute `tools/prepare_android.py --archive JuneTrex.zip --output app`.
- `tools/jtrex_media_runtime.py` possède actuellement `INTRO_FILES`, `SCENES`, `POWER_SCENE_KEYS`, `FINISH_SCENE_KEYS`, le mode admin 20 touches et la résolution `resource_find` puis fichier.
- `tools/jtrex_phase_runtime.py` installe aujourd’hui `zero-win` en modifiant le catalogue de scènes global ; ce couplage doit être retiré au profit d’une résolution de ressource sans mutation globale partagée.
- `tools/prepare_android.py` centralise `POWER_COSTS`, adapte le main historique et contient `MEDIA_ASSETS` avec garde de tailles.
- `tests/test_media_asset_size_guards.py` lit explicitement `MEDIA_ASSETS` et compare les tailles réelles.
- `tests/test_orb_media_manifest.py` protège le média d’attente canonique.
- `buildozer.spec` embarque actuellement py/kv/png/jpg/jpeg/gif/wav/mp4 et conserve l’icône Android JTrex.

## 5. Lot 01 — inventaire et contrat de format

Avant extraction fonctionnelle, générer le vrai `app/main.py` depuis `JuneTrex.zip` avec la chaîne canonique puis relever exactement :
- noms/libellés identitaires ;
- images de pouvoirs et variantes repos/appui/disponibilité ;
- portraits/images contenant les dinosaures ;
- sons identitaires et replis ;
- six branches d’effets ;
- bases de calcul, cibles, réductions, plafonds ;
- interactions dégâts/soin/énergie ;
- jalons historiques d’application.

Pour chaque valeur candidate : emplacement, sens exact, unité, valeur canonique, conséquence d’une modification et test d’équivalence.

Ne pas interpréter `deg`, `longanim1`, index de frame ou état comme paramètre d’équilibrage sans preuve du main généré.

Livrable : inventaire ciblé + contrat de format v1.

## 6. Contrat du manifeste v1

Champs minimaux :
- `format_version`, `set_id`, `revision`, `display_name`, `engine_contract` ;
- `dinosaurs.left/right` avec `id`, `display_name`, portrait optionnel ;
- `media.intros[]`, `orbs_background`, `charge_red_blue`, `charge_yellow`, `verdict_draw`, `verdict_left`, `verdict_right`, `finishing_left`, `finishing_right` ;
- `powers.left_1..left_3`, `right_1..right_3` ;
- par pouvoir : libellé, média, images, mécanisme moteur autorisé, paramètres autorisés ;
- `assets[]` avec identifiant, chemin relatif, type, taille et SHA-256.

`set_id` n’implique jamais l’ordre des camps : `dinosaurs.left` et `dinosaurs.right` font autorité.

Le premier manifeste référence les médias actuels sans déplacement massif d’assets.

## 7. Résolution et session

Tous les accès spécifiques au set passent par un résolveur logique central.

La sélection de set :
- est validée avant le match ;
- est figée pour toute la session de combat ;
- ne change jamais en plein combat ;
- invalide proprement lecteurs, textures, callbacks et positions de reprise lors d’un changement de set ;
- conserve la reprise normale du fond orbes à l’intérieur du même set ;
- revient explicitement au set canonique si la sélection persistée n’est plus valide.

L’intro de lancement utilise le dernier set valide. Changer le set dans le menu ne rejoue pas automatiquement l’intro.

## 8. Stockage, import et export

Trois racines logiques : officiel embarqué en lecture seule, utilisateur persistant, brouillon séparé.

Format portable : ZIP auto-contenu avec manifeste et ressources spécifiques. Aucun script, Python, KV, module natif, pickle, expression ou téléchargement distant.

Validation :
- schéma fermé/versionné ;
- nombres finis et bornés ;
- chemins relatifs confinés ;
- traversées et liens symboliques refusés ;
- doublons/collisions contrôlés ;
- limites centralisées sur tailles/fichiers/extraction ;
- contrôle des octets réellement extraits ;
- installation transactionnelle depuis zone temporaire ;
- ancienne révision préservée si erreur/interruption.

Une collision d’identifiant n’écrase jamais silencieusement. Le statut officiel vient seulement du catalogue embarqué.

Sur Android, les URI `content://` sont copiées dans le stockage de brouillon ; elles ne sont jamais passées directement comme chemins CoreVideo.

## 9. Menu joueur et atelier admin

Accueil : menu lisible du set avec nom, duo, vignette éventuelle et distinction officiel/utilisateur.

Le joueur normal ne voit pas l’atelier.

Les 20 touches existantes restent la porte d’entrée cachée et le diagnostic actuel reste accessible.

Atelier v1 : créer depuis un set, modifier un set utilisateur, importer, exporter, tester, promouvoir une révision complète dans le menu joueur.

Assistant par rôle : aperçu actuel, choisir ressource, aperçu remplacement, conserver, valider/continuer, retour étape précédente, progression et reprise du brouillon.

UI : textes lisibles, grandes commandes, aperçu agrandissable.

## 10. Aperçu indépendant et test de brouillon

L’aperçu réutilise le décodeur vidéo mais aucun callback de combat. Il ne peut déclencher ni impact, KO, point, phase, énergie, chrono ou reset.

Un seul aperçu actif suffit. Fermeture/remplacement libère lecteur et callbacks.

Validation légère média : présence/type réel, ouverture par le décodeur utilisé, première image exploitable, dimensions/orientation/proportions, pistes attendues, durée et avertissements utiles.

Aucun transcodage automatique et aucun déplacement automatique des jalons historiques selon la durée du fichier.

`TESTER CE SET` fige une révision de brouillon, lance le moteur commun avec cette sélection temporaire, puis revient à l’atelier en restaurant la sélection normale.

Un média obligatoire absent refuse le lancement. Un échec en lecture doit finir de manière bornée sans double impact ni verrou permanent.

## 11. Paramètres de pouvoirs

V1 commence par noms/images/médias tout en gardant les six mécanismes existants.

Les coefficients/montants ne deviennent éditables qu’après l’inventaire Lot 01 et validation par Fab de la liste et des bornes.

Le pack ne peut sélectionner qu’un mécanisme autorisé par le moteur ; il ne peut définir un algorithme, changer le coût canonique v1, déplacer un effet à EOS ou supposer qu’un mécanisme gauche est portable à droite sans audit.

## 12. Tests et non-régression

Conserver tous les tests historiques, puis ajouter :
- équivalence du set canonique ;
- mapping gauche/droite et six pouvoirs ;
- distinction jaune/ZeroWin/verdicts ;
- isolation de deux sessions de sets successifs ;
- invalidation des vieux callbacks/EOS ;
- import/export round-trip + empreintes ;
- pack incomplet, chemin interdit, collision, format incompatible, import interrompu ;
- pause/reprise et annulation du sélecteur Android ;
- copie longue non bloquante pour l’UI ;
- chrono 10 s, retour pouvoir, KO, round, match complet ;
- effet appliqué une seule fois ;
- limites/refus des paramètres ;
- conservation réductions/plafonds/énergie.

Les tests simulés et la CI ne remplacent pas la validation téléphone.

## 13. Packaging

Faire évoluer les listes de ressources vers une source cohérente dérivée du catalogue/manifeste officiel tout en conservant les gardes de présence, taille et empreinte.

Ne pas maintenir plusieurs catalogues manuels contradictoires.

L’icône du lanceur reste `assets/icon/JtrexIcon.png`.

Build Android aux jalons utiles, pas à chaque petite étape.

Aucun merge `main`, aucune Release et aucun AAB sans ordre explicite de Fab.

## 14. Ordre d’implémentation

1. Lot 01 : inventaire du main réellement généré + contrat format v1.
2. Lot 02 : manifeste canonique + résolution centrale + tests d’équivalence.
3. Lot 03 : catalogue + sélection joueur figée/persistante.
4. Lot 04 : stockage, import/export transactionnels.
5. Lot 05 : atelier admin, assistant, aperçus, mode test brouillon.
6. Lot 06 : paramètres de pouvoirs après validation explicite des champs éditables.

Chaque lot synchronise `ordres-de-mission.md`, `brain.md`, `brainmap.md`, `debughistorical.md` et `todo.md` avec seulement les faits utiles.
