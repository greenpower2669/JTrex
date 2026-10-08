# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-07

## Baseline
- Archive canonique : 327992765 octets ; SHA-256 `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- `app/main.py` est généré, jamais source versionnée.
- `deg[21..26]=181..186` = jalons, pas dégâts.

## Effets historiques / Lot 06
- 21 STSF, 23 STTA : dégâts droite ; 24 TRFS, 25 TRPH : dégâts gauche ; défaut brut 1/4.
- 22 Lifestream : soin gauche défaut 1/4, plafonné par dégâts subis, sans énergie/lissage au jalon 182.
- 26 Meteor : dégâts gauche défaut 1/3.
- Lot 06 remplace uniquement ces fractions brutes par six valeurs validées du set.
- Bornes : 10–40 % pour les cinq quarts ; Meteor 15–50 %.
- Lissage et énergie dérivée des attaques restent historiques ; coûts/jalons/chrono/KO/EOS inchangés.
- `parameters:{}` reste canonique/rétrocompatible.

## Incident CI Lot 06
- Android #86 `37576071180` : FAIL avant compilation sur le garde texte obsolète `parameters are closed in v1`.
- Cause : validation statique CI restée au contrat Lot 05.
- RED : `37576362322` ; GREEN : `37576423433`.
- Fix : le garde vérifie `POWER_PARAMETER_SPECS` et `power_effect_fraction`.
- Android #89 `37576480368` : SUCCESS ; 174/174 ; BUILD SUCCESSFUL.
- APK SHA-256 `4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`.

## Règle
CI verte != validation téléphone. Aucun merge `main`, Release ou AAB sans ordre Fab.


## 2026-10-07 — dette UI Lot 06 observée téléphone
Le candidat CI était fonctionnel mais le bouton DINOSAURES 520dp et plusieurs BoxLayout non scrollables rendaient la création/édition peu accessible. Correctif JT-SETS-UI-001 limité à l'UI ; ajouter une garde de régression sur compacité et ScrollView.


## 2026-10-07 — aperçu fermé + bord dinosaure droit
- Cause `Aperçu fermé` : `_open_workshop_preview_popup()` appelait `_close_workshop_preview_popup()` après que `workshop_preview_current/candidate` avait déjà créé et lancé le lecteur ; le lecteur neuf était donc immédiatement stop/unload.
- Correctif : fermer l'ancien aperçu avant de créer le nouveau ; le popup d'affichage ne ferme plus le lecteur qu'il doit montrer.
- Audit APK #90 : les rectangles historiques `jh/jb` portent les animations dinosaures. L'image droite peut être volontairement tronquée ; le correctif ne touche pas au média et pousse seulement le rectangle visible le plus à droite suffisamment hors viewport en MENU.
- Les glyphes `▼` / `✎` n'étaient pas fiables sur l'appareil : libellés ASCII.


## 2026-10-08 — saut d'image dinosaure droit
- Symptôme #93 : première position trop à gauche puis saut vers la droite.
- Cause confirmée : `_guard_menu_right_dinosaur_crop` tournait toutes les 0,05 s après que le moteur historique avait déjà peint le widget.
- Première tentative d'injection recherchait `self.jb.pos` dans `screen_up` : échec de préparation, car l'affectation visuelle est ailleurs dans le source historique.
- Diagnostic CI a confirmé que `screen_up` ne contient que la logique `xb/yb/xbs/ybs`.
- Correctif final : rechercher l'unique affectation `self.jb.pos` dans le source généré complet et la borner directement avant rendu ; condition menu `indexa==0`.
- La préparation CI #100 passe désormais ce patch et les tests moteur généré sont verts.


## 2026-10-08 — dino droit encore trop à gauche
- #100 confirme que le saut a disparu avec le clamp pré-rendu.
- La position restait trop intérieure : l'ancienne marge était plafonnée à 44 et seulement 8 % de la largeur.
- Ajustement ciblé : marge hors écran = 40 % de la largeur du widget, minimum 24. Aucun autre calcul historique modifié.


## 2026-10-08 — audit transparence / géométrie droite
- APK #102 : `self.jh.pos ... #d`, `self.jb ... #g`.
- 31 frames `d` : 320×240, alpha union (21,29)-(320,240), bord droit toujours opaque.
- 31 frames `g` : 320×240, alpha union (0,29)-(299,240), bord droit frame par frame de 174 à 299 ; marge transparente droite 21..146 px.
- Le clamp 40 % de UI-004 bornait le rectangle complet et ne compensait donc pas correctement la marge transparente variable de `g`.
- UI-005 utilise le bord visuel droit conservateur 174/320 et le bord droit du parent, avec 2 % de dépassement parent. Le calcul reste pré-rendu.

## 2026-10-08 — capture : deux dinosaures collés à droite
Capture Fab : aucune animation à gauche ; deux silhouettes à droite. Les quatre push précédents changeaient exclusivement la borne droite `jb`, sans borne du `jh`. Correctif ciblé sur l'autre affectation de position, limité au MENU : `min(x_historique, bord_gauche - 2% largeur_parent)`. Hypothèse de réparation nécessitant validation graphique réelle ; CI statique seule insuffisante.

## 2026-10-08 — sprites inverses sur capture UI-006
Preuve APK : ga alimente jb avec g/g_* et da alimente jh avec d/d_*. g/g_* a pixels opaques a gauche ; d/d_* a pixels opaques a droite. La tete de jh est donc vers la gauche et jb vers la droite. UI-007 inverse les sources MENU, les images initiales et corrige le ratio de bornage droit de 174/320 a 1.0. Test reel telephone encore indispensable.
