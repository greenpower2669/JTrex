# JTREX — JT-SETS-001 — Plan Lot 03

Date : 2026-10-05
Branche : `feature/dinosaur-sets-v1`
Base Lot 03 : `9efad3d0dfaf480aa46e715442d104357969abef`

## Objectif
Ajouter la sélection joueur des sets officiels, persistante au menu et figée pour toute la durée d'un match, sans modifier les règles de gameplay.

## Invariants
- le set canonique `trex_vs_steg` reste le fallback sûr ;
- l'intro de lancement utilise le dernier set persisté valide ;
- changer le set au menu ne rejoue pas l'intro ;
- aucun changement de set pendant un match ;
- tout changement de set invalide lecteurs/callbacks/reprise vidéo de l'ancienne sélection ;
- médias, images et sons identitaires du set utilisent la même sélection figée ;
- aucun import/export, brouillon, atelier 20 touches ou équilibrage dans ce lot ;
- aucun merge `main`, aucune Release, aucun AAB.

## Tâche 1 — catalogue, persistance, session pure Python
Fichiers : `tools/jtrex_sets_runtime.py`, `tests/test_sets_selection.py`.

RED : tests pour catalogue officiel, doublons, persistance valide, fallback canonique sur ID/JSON invalide, écriture atomique, gel de session, refus de sélection pendant session, nouvelle session après retour menu.

GREEN : ajouter une API fermée de catalogue et un gestionnaire de sélection/session sans dépendance Kivy.

## Tâche 2 — intégration media + menu joueur
Fichiers : `tools/jtrex_media_runtime.py`, `tools/jtrex_phase_runtime.py`, tests média/session.

RED : prouver intro=dernier set valide, `begin_session` avant premier ROUND, sélection figée pendant le match, `end_session` au MENU, invalidation génération/reprise lors d'un changement au menu, bouton/menu lisible officiel.

GREEN : le contrôleur média possède le gestionnaire de session, expose le catalogue joueur et maintient un bouton/popup visible seulement au menu. Changer au menu stoppe l'ancien lecteur et remet les marqueurs de reprise à zéro sans rejouer l'intro.

## Tâche 3 — identités pouvoirs set-aware
Fichiers : `tools/prepare_android.py`, `tools/jtrex_media_runtime.py`, tests préparateur/intégration.

RED : le main généré ne doit plus réinjecter les chemins canoniques d'icônes/sons à chaque tick quand un autre set est actif.

GREEN : introduire une table moteur de chemins de pouvoirs initialisée au canon, utilisée par les six icônes ready/used ; au début de session, le contrôleur remplace les six couples d'images, les six sons d'activation et les six fallbacks audio 21..26 depuis la sélection figée.

Les coûts, mécanismes, états et jalons restent inchangés.

## Tâche 4 — non-régression
- test de deux sessions successives avec deux manifests synthétiques ;
- vieux EOS/callback de session A sans effet sur session B ;
- chrono/KO/pouvoirs historiques inchangés ;
- suite complète verte ;
- `prepare_android.py` canonique vert.

## Tâche 5 — Android et clôture
- workflow Android normal sur le HEAD exact ;
- collecter APK + SHA-256 ;
- synchroniser `ordres-de-mission.md`, `brain.md`, `brainmap.md`, `debughistorical.md`, `todo.md` ;
- documenter `docs/jt-sets-001/lot03-verification.md`.

## État d'exécution
- commit produit Lot 03 : `dfad8fbc5ae4678fb5bd704ea38a858116966a5b` ;
- parent direct : `9efad3d0dfaf480aa46e715442d104357969abef` ;
- intégration contrôlée : patch SHA-256 `c44fb521075ce7266a4473aa220b6f8530a91f1eeb197ecaf1a480efc6c8d953`, 77 tests GREEN, `py_compile` GREEN, 12 références `JT_POWER_PATHS` ;
- validation Android finale : en cours sur le même code produit.
