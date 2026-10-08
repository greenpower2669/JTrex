# JT-SETS-UI-005 — audit géométrique du dinosaure droit

Date : 2026-10-08

## Contrat
Le dinosaure gauche reste inchangé. Le dinosaure droit doit être borné avant rendu à partir du bord droit réel du parent et du bord visuel droit de son animation. Aucun média, aucune taille, aucune logique de jeu ne sont modifiés.

## Audit des PNG canoniques
Audit des 31 frames de chaque séquence dans l'APK #102 :

- `d/d_*.png` : 320×240 ; bord opaque droit toujours à 320 ; bord opaque gauche varie de 21 à 146.
- `g/g_*.png` : 320×240 ; bord opaque gauche toujours à 0 ; bord opaque droit varie de 174 à 299.
- Les deux séquences sont donc géométriquement miroir.
- `self.jb` utilise la séquence `g` dans le rendu historique.
- Le rectangle complet de `g` contient donc une marge transparente à droite de 21 à 146 px suivant la frame.

Pour éviter qu'une frame précoce paraisse trop près du centre, la borne utilise le bord visuel droit conservateur commun à toute l'animation : `174 / 320 = 0.54375` de la largeur du rectangle.

## Formule
`parent_right = self.x + self.width`

`overhang = self.width * JT_SELECTION_RIGHT_OVERHANG_RATIO`

`target_visual_right = parent_right + overhang`

`visual_right_in_rect = self.jb.size[0] * JT_SELECTION_RIGHT_VISUAL_EDGE_RATIO`

`min_x = target_visual_right - visual_right_in_rect`

Puis le rendu conserve l'animation historique mais ne peut pas passer à gauche de `min_x`.

Paramètres initiaux :
- `JT_SELECTION_RIGHT_VISUAL_EDGE_RATIO = 174/320`
- `JT_SELECTION_RIGHT_OVERHANG_RATIO = 0.02`

Le dépassement est donc lié à la largeur réelle du parent et reste cohérent entre résolutions.

## Invariants
- aucune correction post-rendu ;
- aucune modification de `xb/yb` ;
- aucune modification du dinosaure gauche ;
- aucune modification des PNG ;
- aucune modification du gameplay.
