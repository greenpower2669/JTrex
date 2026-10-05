# JTREX — JT-SETS-001 — Contrat de format v1

Date : 2026-10-05
Statut : contrat issu de l’inventaire Lot 01 ; source du futur manifeste Lot 02
Inventaire : `docs/jt-sets-001/lot01-inventory.md`
Design : `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`

## 1. Objet

Le format v1 décrit un **set complet de confrontation** DATA + MEDIA pour le moteur June T-Rex. Il ne contient aucun gameplay exécutable.

Un set fournit :
- deux identités explicites gauche/droite ;
- les ressources audiovisuelles du duo ;
- six présentations de pouvoirs ;
- les métadonnées nécessaires à la validation et au transport.

Le moteur garde toutes les règles de combat, transitions, KO, rounds, chrono, EOS, verrouillages et jalons d’impact.

## 2. Valeurs d’en-tête v1

Valeurs canoniques proposées et figées pour l’implémentation Lot 02 :

```json
{
  "format_version": 1,
  "engine_contract": "jtrex-combat-v1"
}
```

`format_version` décrit la forme du manifeste.

`engine_contract` décrit les règles moteur exigées par le set. Un set v1 n’est utilisable que si l’application annonce explicitement la compatibilité avec `jtrex-combat-v1`.

## 3. Schéma logique fermé

Le manifeste v1 accepte uniquement les champs déclarés ci-dessous. Les champs inconnus sont refusés à l’import, sauf évolution explicite d’une version future.

```text
format_version: integer = 1
set_id: string stable
revision: integer >= 1
display_name: string
engine_contract: string = "jtrex-combat-v1"

catalog:
  thumbnail: asset-id | null

dinosaurs:
  left:
    id: string
    display_name: string
    portrait: asset-id | null
  right:
    id: string
    display_name: string
    portrait: asset-id | null

media:
  intros: [asset-id, ...]
  orbs_background: asset-id
  charge_red_blue: asset-id
  charge_yellow: asset-id
  verdict_draw: asset-id
  verdict_left: asset-id
  verdict_right: asset-id
  finishing_left: asset-id
  finishing_right: asset-id

powers:
  left_1: PowerEntry
  left_2: PowerEntry
  left_3: PowerEntry
  right_1: PowerEntry
  right_2: PowerEntry
  right_3: PowerEntry

PowerEntry:
  label: string
  media: asset-id
  images:
    ready: asset-id
    used: asset-id
  activation_audio: asset-id | null
  legacy_fallback_audio: asset-id | null
  mechanism: engine-mechanism-id
  parameters: object

assets:
  - id: string unique
    path: relative POSIX path
    type: "video" | "image" | "audio"
    size: integer >= 0
    sha256: 64 lowercase hexadecimal characters
```

`set_id` ne code jamais le sens gauche/droite. Même si un identifiant contient `trex_vs_steg`, seuls `dinosaurs.left` et `dinosaurs.right` font autorité.

## 4. Règles d’identifiants et chemins

### `set_id`

- stable entre deux révisions compatibles du même set ;
- ASCII simple recommandé : `[a-z0-9][a-z0-9._-]*` ;
- ne détermine ni les camps ni les mécanismes.

### `asset-id`

- unique dans le manifeste ;
- référence une entrée de `assets` ;
- les rôles média et pouvoirs référencent des identifiants, jamais directement des chemins arbitraires.

### `assets[].path`

- chemin relatif POSIX à la racine du set portable ;
- jamais absolu ;
- aucun `..` ;
- aucune URI `file://`, `content://`, HTTP(S) ou autre schéma ;
- aucun lien symbolique accepté à l’import ;
- les URI Android sélectionnées par l’utilisateur sont copiées dans le brouillon avant d’être référencées.

## 5. Neuf rôles média obligatoires

Le contrat v1 exige exactement les groupes/rôles de présentation suivants :

1. `intros` — collection non vide ;
2. `orbs_background` ;
3. `charge_red_blue` ;
4. `charge_yellow` ;
5. `verdict_draw` ;
6. `verdict_left` ;
7. `verdict_right` ;
8. `finishing_left` ;
9. `finishing_right`.

Le manifeste choisit les ressources. Il ne choisit jamais les états numériques associés, les politiques de boucle ou le moment où ces rôles sont demandés.

## 6. Six pouvoirs obligatoires

Le contrat exige exactement :
- `left_1`, `left_2`, `left_3` ;
- `right_1`, `right_2`, `right_3`.

Chaque entrée fournit le contenu de présentation et une référence à un mécanisme moteur autorisé.

### Images v1

L’inventaire prouve deux états d’icône spécifiques au pouvoir :
- `ready` : équivalent historique `*1.png`, slot non encore utilisé ;
- `used` : équivalent historique `*0.png`, slot déjà utilisé.

L’aura animée de disponibilité `select/select0..15.png` reste **engine-owned** en v1. Elle n’est pas fournie par chaque pouvoir.

### Audio v1

`activation_audio` correspond au son court déclenché au lancement du pouvoir.

`legacy_fallback_audio` correspond au son historique de scène utilisé par le moteur comme repli avant qu’une vraie frame MP4 permette d’activer l’audio natif. Il peut être `null` pour un futur set si la politique de validation l’autorise, mais le profil canonique le renseigne.

## 7. Mécanismes moteur v1

Pour la première implémentation, les mécanismes sont **fixés par slot**. Le format n’autorise pas encore le déplacement d’un mécanisme gauche vers la droite ni l’inverse.

Identifiants v1 :

| Entrée | Mechanism ID | Effet canonique interne |
| --- | --- | --- |
| `left_1` | `left_slot_1_target_damage` | état 21, brut `pvd/4` |
| `left_2` | `left_slot_2_self_heal` | état 22, soin brut `pvg/4` |
| `left_3` | `left_slot_3_target_damage` | état 23, brut `pvd/4` |
| `right_1` | `right_slot_1_target_damage` | état 24, brut `pvg/4` |
| `right_2` | `right_slot_2_target_damage` | état 25, brut `pvg/4` |
| `right_3` | `right_slot_3_target_damage` | état 26, brut `pvg/3` |

Ces identifiants sont des sélecteurs vers du code moteur déjà présent. Ils ne contiennent ni formule ni callback dans le pack.

## 8. Paramètres d’équilibrage : fermés pour v1 initial

L’inventaire a prouvé six fractions candidates, mais Fab doit encore valider la liste des champs éditables et leurs bornes au Lot 06.

Jusqu’à cette validation :

```json
"parameters": {}
```

est la seule valeur autorisée pour chaque `PowerEntry` dans l’implémentation initiale.

Les valeurs canoniques restent dans le moteur :
- left_1 : `1/4` vie max cible ;
- left_2 : `1/4` vie max propre en soin ;
- left_3 : `1/4` vie max cible ;
- right_1 : `1/4` vie max cible ;
- right_2 : `1/4` vie max cible ;
- right_3 : `1/3` vie max cible.

Un changement futur de ces valeurs devra préserver les interactions historiques de dégâts, soin, plafonnement et énergie ; il ne pourra pas être traité comme une simple valeur visuelle.

## 9. Frontière SET-OWNED / ENGINE-OWNED

### SET-OWNED v1

- `set_id`, `revision`, `display_name` ;
- identités et noms gauche/droite ;
- portrait/vignette optionnels ;
- choix des neuf rôles média ;
- labels de pouvoirs ;
- MP4 des six pouvoirs ;
- images `ready` / `used` ;
- audio d’activation et fallback éventuel ;
- inventaire d’assets avec taille et SHA-256.

### ENGINE-OWNED — jamais modifiable par le pack

- états `indexa` et transitions ;
- mapping des phases ;
- trois orbes par camp ;
- nouvel échange = 10 secondes ;
- retour de pouvoir = temps restant ;
- KO, rounds, deux victoires et finishing final ;
- vies initiales canoniques ;
- score et seuil d’égalité ;
- coûts `60/40/60/60/60/80` ;
- condition stricte `énergie > coût` ;
- énergie fractionnaire ;
- `selected` et réarmement ;
- jalons `deg[21..26]=181..186` ;
- `anim1`, `longanim1`, `indexa` ;
- formules de dégâts/soin v1 initial ;
- gains d’énergie dérivés des dégâts ;
- lissage/plafonnement historiques ;
- politique `loop` / `play_to_end` ;
- première frame et bascule audio ;
- EOS et protections de génération/callbacks ;
- aspect-fit intros / aspect-fill combat ;
- masques HUD et protections tactiles.

## 10. Profil canonique v1 — mapping sans déplacement d’assets

Le premier set officiel conserve les ressources à leurs emplacements actuels. Le futur résolveur Lot 02 fournit l’adaptation logique sans migration massive des fichiers.

Profil proposé :

```text
set_id = trex_vs_steg
revision = 1
display_name = Steg vs T-Rex
engine_contract = jtrex-combat-v1

dinosaurs.left.id = st
dinosaurs.left.display_name = Steg
dinosaurs.right.id = tr
dinosaurs.right.display_name = T-Rex
```

Les noms d’affichage ci-dessus sont des données de catalogue ; les identités moteur restent `ST` gauche et `TR` droite. Le nom de `set_id` ne change pas cet ordre.

### Rôles média du profil canonique

```text
intros = JTrexintro1, JTrexintro2, JTrexintro3
orbs_background = StegTrexPlageVideoenboucledesorbes
charge_red_blue = Chargestegtrexchargerougebleucorrected
charge_yellow = Stegtrexegalitechargeboutonjaune
verdict_draw = Zerowinstegtrexsurleschargedejaugejauneetbleuetrouge
verdict_left = Stegtrexresultstegwin
verdict_right = Stegtrexresulttrexwin
finishing_left = steg-finishing-trex
finishing_right = trex-finishing-steg
```

### Pouvoirs du profil canonique

| Entrée | Label v1 | Média | Images | Audio activation | Fallback | Mécanisme |
| --- | --- | --- | --- | --- | --- | --- |
| `left_1` | Sanctuary Force | `stsf-sanctuary-force.mp4` | `stsf1.png` / `stsf0.png` | `sf.wav` | `stsf.wav` | `left_slot_1_target_damage` |
| `left_2` | Lifestream | `stls-lifestream.mp4` | `sth1.png` / `sth0.png` | `ls.wav` | `stls.wav` | `left_slot_2_self_heal` |
| `left_3` | Tornado Attack | `stta-tornado-attack.mp4` | `stta1.png` / `stta0.png` | `ta.wav` | `stta.wav` | `left_slot_3_target_damage` |
| `right_1` | Fire Storm | `trfs-fire-storm.mp4` | `trfs1.png` / `trfs0.png` | `fs.wav` | `trfs.wav` | `right_slot_1_target_damage` |
| `right_2` | Phoenix Attack | `trph-phoenix-attack.mp4` | `trph1.png` / `trph0.png` | `ph.wav` | `trph.wav` | `right_slot_2_target_damage` |
| `right_3` | Meteor Attack | `trma-meteor-attack.mp4` | `trma1.png` / `trma0.png` | `ma.wav` | `trma.wav` | `right_slot_3_target_damage` |

Les tailles et SHA-256 exacts des MP4 et images sont figés dans `lot01-inventory.md` et doivent être recopiés dans le manifeste canonique réel du Lot 02. Les fichiers historiques générés depuis `JuneTrex.zip` ne deviennent pas pour autant des dépendances cachées d’un export utilisateur : un export portable devra embarquer toutes les ressources spécifiques au set.

## 11. Validation des assets

Toute ressource référencée doit avoir :
- un `id` unique ;
- un type attendu ;
- une taille déclarée ;
- un SHA-256 déclaré ;
- des octets réellement présents et vérifiés.

Une extension seule ne suffit pas à valider le type. La validation média complète Android est traitée dans les lots I/O/atelier ; le contrat v1 exige déjà l’intégrité taille + empreinte.

Les gardes actuelles `MEDIA_ASSETS` et tests de taille restent des preuves de référence tant qu’elles ne sont pas remplacées par une source cohérente dérivée du catalogue/manifeste officiel.

## 12. Sécurité du format

Un set v1 ne peut contenir :
- Python ;
- KV ;
- script ;
- module natif ;
- pickle ;
- expression exécutable ;
- import dynamique ;
- URL de téléchargement à exécuter ;
- chemin hors racine du pack.

Le manifeste ne peut ni redéfinir un état ni fournir une formule.

## 13. Complétude v1 — contrôle Lot 01

- [x] exactement deux côtés `left` / `right` ;
- [x] collection `intros` + huit rôles de combat/présentation = neuf groupes/rôles requis ;
- [x] exactement six entrées de pouvoirs ;
- [x] metadata asset `id/path/type/size/sha256` obligatoire ;
- [x] `set_id` indépendant de l’ordre gauche/droite ;
- [x] ZeroWin fait partie des ressources obligatoires du contrat ;
- [x] aucune règle de phase/KO/EOS/impact exposée comme donnée de pack ;
- [x] coûts canoniques et condition `energy > cost` restent moteur-owned ;
- [x] paramètres d’équilibrage désactivés tant que Fab ne les valide pas ;
- [x] profil canonique mappé sans déplacement massif d’assets.

## 14. Sortie attendue du Lot 02

À partir de ce contrat, le Lot 02 pourra créer :
- le schéma/validateur runtime minimal ;
- `assets/sets/catalog.json` ;
- `assets/sets/trex_vs_steg/manifest.json` ;
- le résolveur rôle logique -> ressource réelle ;
- l’adaptation du runtime média sans mutation globale de `SCENES` ;
- les tests d’équivalence du set canonique.

Aucun de ces composants runtime n’est créé dans le Lot 01.
