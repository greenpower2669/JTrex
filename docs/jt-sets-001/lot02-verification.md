# JT-SETS-001 — Lot 02 — vérification

Date : 2026-10-05
Branche : `feature/dinosaur-sets-v1`

## Périmètre livré
- Runtime DATA-only fermé : `tools/jtrex_sets_runtime.py`.
- Catalogue officiel : `assets/sets/catalog.json`.
- Manifeste canonique : `assets/sets/trex_vs_steg/manifest.json`.
- 41 assets canoniques inventoriés avec taille + SHA-256.
- `tools/prepare_android.py` valide et embarque catalogue/manifeste/runtime depuis la même source de vérité.
- `jtrex_media_runtime.py` conserve les policies moteur et résout les chemins par rôles logiques du set sélectionné.
- ZeroWin est une scène moteur normale ; `jtrex_phase_runtime.py` ne mute plus un `SCENES` global.
- Aucun paramètre d'équilibrage n'est ouvert : `parameters:{}` reste fermé en v1.

## Preuves TDD / intégration
Cycle Lot 02 :
- RED initial : 18 tests Lot 02 échouaient avant le runtime/catalogue/manifeste.
- GREEN ciblé : 8 tests contrat, puis packaging/résolution/CI.
- Suite complète : 56 tests / 56 OK.

Run d'intégration `37378554085` : GREEN.
- Reconstruction du patch par SHA exacte.
- Archive `JuneTrex.zip` vérifiée : 327992765 octets, SHA-256 `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- `prepare_android.py` : canon `trex_vs_steg`, 41 assets.
- Main préparé conservé : SHA-256 `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.
- `Ran 56 tests` -> `OK`.
- Aucun `__pycache__`/`.pyc` poussé.

## Git produit
- Commit produit : `017d611cf798d4713af8039ee6962d1fe6729fd2` — `feat: resolve canonical JTrex set media from manifest`.
- Workflow Android exact restauré : commit `ee8cf297830e1f40d984ab6b1706733eff22e5d7`, blob `c22bcf40038889318a3cab7c25d6c8c78dd87c49`, SHA-256 `3f4a83e9a0c35f7f361917fdbacfe6cadf3c41369519e0dcfc6a2a764bf00b13`.
- Les workflows de transfert/reconstruction Lot 02 ont été retirés du tree final.
- `main` non modifiée ; aucune Release créée.

## Android final
- Run #80 `37379193862` : GREEN sur le HEAD exact.
- Toutes les étapes sont GREEN : préparation, contrat, 56 tests moteur, toolchain, p4a, build, collecte et uploads.
- Artefact APK `11375685200` (`JuneT-Rex-1.0.15-debug`).
- APK : 156461520 octets ; SHA-256 `182e1b8f72f269a7e3f3f24895e37fe23a1b3ade9e77949d14500827c13c320c`.
- Artefact diagnostics `11375670152`.

## Équivalence canonique vérifiée
- mêmes intros, orbes, charge rouge/bleue, jaune, verdicts, six vidéos pouvoirs et deux finishings ;
- mêmes états moteur et mêmes policies `loop` / `play_to_end` ;
- coûts 60/40/60/60/60/80 et condition stricte `energy > cost` inchangés ;
- impacts pouvoirs toujours déclenchés par le jalon historique, jamais par EOS ;
- chrono/rounds/KO/finishing historique inchangés dans les tests d'intégration ;
- ZeroWin conserve sa sémantique mais sans mutation globale du catalogue média.

## Hors Lot 02
Le Lot 02 ne fournit pas encore : menu de choix joueur, persistance du set sélectionné, changement de set en session, import/export ZIP, atelier 20 touches, ni paramètres d'équilibrage modifiables. Ces sujets restent Lots 03 à 06.
