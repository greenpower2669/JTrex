# JTREX — ORDRES DE MISSION VIVANTS

Dernière consolidation : 2026-10-07

## Contrat permanent
1. Ne jamais recoder de mémoire : relire code, tests et preuves Git avant modification.
2. `ordres-de-mission.md` définit le contrat actif ; les autres mémoires restent spécialisées et courtes.
3. Ne pas modifier les règles canoniques historiques sans ordre explicite de Fab.
4. Avant toute annonce de succès : preuve fraîche adaptée.
5. Aucun merge `main`, Release ou AAB sans ordre explicite de Fab.

## Canon gameplay protégé
- 3 orbes/camp ; nouvel échange 10 s ; retour pouvoir = temps restant.
- KO réel seul = round ; deux rounds = match ; vrai nouveau round = énergie 0/0.
- Vie 500000000/camp ; score historique.
- Coûts 60/40/60/60/60/80 ; activation stricte `energy > cost`.
- États 21..26 et jalons 181..186 moteur-owned.
- EOS média n'applique aucun effet gameplay.

## JT-SETS-001 — LOTS 01 À 06 TERMINÉS CODE/CI
Branche : `feature/dinosaur-sets-v1`. Base : `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.

- Lots 01–05 : contrat DATA/MEDIA, runtime/catalogue, sélection/session, stockage ZIP sûr, atelier admin, preview/SAF/test brouillon.
- Lot 06 : six coefficients seulement, approuvés par Fab et bornés :
  - STSF/STTA/TRFS/TRPH : dégâts 0.10..0.40, défaut 0.25 ;
  - Lifestream : soin 0.10..0.40, défaut 0.25 ;
  - Meteor : dégâts 0.15..0.50, défaut 1/3.
- `parameters:{}` reste rétrocompatible = défaut canonique.
- Aucun coût, mécanisme, jalon, chrono, KO, score, énergie dérivée ou EOS éditable.

Preuves Lot 06 :
- produit `8d89c1ed7a70f7e55bac4e6895020a2bbd8995d2` ;
- HEAD CI `d7214bb514e144dfa9191c1d6f3064718b91c570` ;
- validation produit : 173/173 tests ;
- Android #89 `37576480368`, job `112646411728` : SUCCESS, 174/174 tests ;
- APK 156528315 octets, SHA-256 `4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`.

## État
JT-SETS-001 est techniquement complet côté code/CI. Validation téléphone du candidat Lot 06 reste distincte et non enregistrée.
Dernière Release : `v1.0.15-main`.


## JT-SETS-UI-001 — correction téléphone (2026-10-07)
- Autorisé par Fab après validation visuelle du candidat Lot 06.
- Portée UI uniquement : sélecteur compact, atelier/création/catalogue/brouillons/assistant scrollables, raccourci admin ✎.
- Set officiel via ✎ = création d'un brouillon depuis le set ; set utilisateur = modification directe.
- Aucun changement gameplay, coûts, coefficients, phases, KO, score, jalons ou EOS.
- Branche : `feature/dinosaur-sets-v1`.


## JT-SETS-UI-002 — finition téléphone (2026-10-07)
- Demande Fab : centrage/compacité/aération, réparation aperçu, et garde du dinosaure droit volontairement tronqué.
- Ne jamais recadrer/redimensionner l'asset dinosaure : seulement empêcher son rectangle visible le plus à droite d'aller trop à gauche en MENU.
- Cause aperçu : le popup déchargeait le lecteur juste après son démarrage ; fermeture déplacée avant le nouveau preview.
- Libellés spéciaux remplacés par ASCII `SET v` / `MOD` pour éviter les glyphes absents Android.
- Portée UI/preview seulement ; canon gameplay protégé.
- Passation : `docs/jt-sets-001/ui-finish-002-passation.md`.


## JT-SETS-UI-003 — dino droit avant rendu (2026-10-08)
- Retour téléphone #93 : UI/aperçu validés ; seul le dinosaure de sélection droit saute du centre vers la droite.
- Cause : le correctif UI-002 agissait par timer 50 ms après le rendu historique.
- Correction canonique : supprimer le timer runtime et borner l'unique affectation `self.jb.pos` directement dans le `main.py` généré, uniquement quand `indexa==0`.
- Ne pas modifier `xb/yb`, la taille du widget, l'asset volontairement tronqué, ni le dinosaure gauche.
- Aucun gameplay modifié.


## JT-SETS-UI-004 — décalage droit final (2026-10-08)
- Retour téléphone #100 : le bornage pré-rendu est stable, mais le dinosaure droit reste visuellement trop à gauche.
- Correction : conserver le même clamp avant rendu et augmenter uniquement la marge hors écran à `max(24, 40 % de la largeur du widget)`.
- Ne pas toucher au dinosaure gauche, à `xb/yb`, à la taille, à l'asset ou au gameplay.


## JT-SETS-UI-005 — géométrie par bords réels (2026-10-08)
- Contrat Fab : gauche inchangé ; droite calculée depuis le bord droit du parent et le bord visuel droit réel, avant rendu.
- Audit des frames : `g/g_*.png` (utilisé par `self.jb`) contient 21..146 px de transparence à droite ; bord opaque droit conservateur = 174/320.
- Borne droite : bord parent + dépassement réglable de 2 % de la largeur parent, moins le bord visuel interne du rectangle.
- Le correctif 40 % de UI-004 est remplacé par cette géométrie explicite.
- Aucun média, taille, `xb/yb`, dinosaure gauche ou gameplay modifié.

## JT-SETS-UI-006 — correction capture menu (2026-10-08)
- Fab montre deux dinosaures collés à droite et rien à gauche.
- Cause probable : le correctif précédent borne uniquement `self.jb.pos` ; `self.jh.pos` ne possède pas de borne MAX empêchant la traversée vers la droite.
- Correction : borner la X visuelle du rectangle `jh` à `min(x_historique, self.x-0.02*self.width)` dans le MENU seulement. Garder la borne MIN du `jb` inchangée.
- Préserver la X historique quand elle est déjà à gauche, Y, taille, frames, vitesse, gameplay, toutes autres phases.
- Validation source générée/CI puis APK téléphone. Pas de merge main, Release ni AAB sans autorisation.

## JT-SETS-UI-007 — sens des sprites MENU
- Retour Fab capture UI-006 : gauche/droite separes mais visuels tournes vers l'exterieur.
- jh gauche doit recevoir g/g_*, jb droite doit recevoir d/d_* en MENU. Les PNG sont deja des miroirs ; ne pas modifier les medias, seulement les sources.
- Corriger aussi le chargement des premieres images. Hors MENU : conserver ga/da canoniques, gameplay inchange.
- Borne droite du sprite d/d_* calculable avec ratio alpha 1.0. Gauche, Y, tailles inchanges.
- Tests CI, puis APK telephone a valider par Fab. Aucun merge main/Release/AAB.

## JT-SETS-UI-008 — corriger les deux viseurs rouges de menu (2026-10-09)
- Demande Fab : viseur gauche associe au cote droit et viseur droit associe au cote gauche ; corriger les deux simultanement.
- Audit APK UI-007 : `vh` et `vb` utilisent tous deux `viseur.png`, rendus par `screen_up` depuis (xh,yh) et (xb,yb).
- Corriger l'association X des deux rectangles de visee seulement si `indexa==0` : `vh` recoit X visuel de `vb` et inversement, sans echanger leurs Y.
- Ne pas changer xh/yh/xb/yb, mouvement tactile, calcul d'impact, sprites dinos, tailles, gameplay et rendu hors MENU.
- Garde CI, tests du main.py genere, APK debug pour validation telephone. Pas de merge main, Release, ni AAB sans accord Fab.

## JT-SETS-UI-009 — contrat Fab tactile gauche/droite (2026-10-09)
- Zone X [0,W/2[ -> doigt gauche -> coordonnees xh/yh -> viseur vh -> dinosaure jh (GAUCHE).
- Zone X [W/2,W] -> doigt droit -> xb/yb -> viseur vb -> dinosaure jb (DROITE).
- Capture de side au touch_down dans touch.ud, deux doigts simultanes independants, maintien de leur camp pendant les mouvements, X borne a leur moitie.
- Retirer la permutation graphique UI-008 (retablir rendu vh=xh et vb=xb) ; modifier tests de zones d'on_touch_down et d'on_touch_move uniquement en MENU.
- Aucun changement de phase de combat, scores, boutons ou gameplay ; garder orientation/bornage des dinos de UI-007.
- Branch de correctif uniquement, tests du moteur genere et APK debug, validation telephone Fab avant main/Release/AAB.

UI-009 complet : remapper aussi dans screen_up les coordinations xhs<-xh et xbs<-xb pour le MENU, car les vieux gardes historiques xbs gauche / xhs droite bloquent l'interaction; aucun changement en combat.
