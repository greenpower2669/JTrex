# JT-SETS-001 — Lot 01 — Vérification

Date : 2026-10-05
Branche : `feature/dinosaur-sets-v1`
Base : `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`

## Preuves fraîches

- Workflow diagnostic temporaire run #2 : `37339853652` — conclusion `success`.
- Vérification archive officielle : 327992765 octets, SHA-256 `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647` — PASS.
- Main historique attendu : SHA-256 `3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231` — vérifié par le préparateur.
- Main Android généré : SHA-256 `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.
- Suite complète : `python3 -m unittest discover -s tests -v` -> `Ran 38 tests` / `OK`.
- Sous-ensembles présents dans cette suite : 19 phase-integration, 7 round-KO, 5 round-model, 4 orb-presentation, tous PASS.
- Le workflow diagnostic temporaire a été supprimé après collecte des preuves.

## Diff final de produit

Comparaison `ce858fe57...` -> `94e9bac5...` après suppression du workflow temporaire : seuls les cinq fichiers de mémoire et les documents `docs/` diffèrent.

Aucun fichier sous `tools/`, `assets/`, `.github/`, aucun `buildozer.spec` et aucun code produit ne diffère de la base de mission.

## Review Focus Lot 01

1. **Archive / main non canonique : PASS.** Taille + SHA archive imposés avant génération ; SHA du main historique contrôlé par `prepare_android.py`.
2. **Faux paramètre d’équilibrage : PASS.** `deg[21..26]` prouvé comme jalon 181..186 ; `longanim1`, `anim1`, `indexa`, durée MP4 et EOS classés engine-owned/non-paramètres.
3. **Mapping gauche/droite/slots : PASS.** ST gauche slots 1..3 -> états 21..23 ; TR droite slots 4..6 -> états 24..26 ; coûts et médias associés inventoriés.
4. **Événement vs dégâts : PASS.** Les écritures réelles `degg/degd +=/-= pvg/pvd` sont séparées des index de déclenchement `deg`.
5. **Impact déduit de la vidéo : PASS.** L’impact reste dans `anim_1`; `video_complete`/EOS ne font qu’autoriser la suite de présentation/KO et n’appliquent aucun dégât, soin ou énergie.

## Livrables

- `docs/jt-sets-001/lot01-inventory.md`
- `docs/jt-sets-001/format-v1-contract.md`
- `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`
- `docs/superpowers/plans/2026-10-05-jtrex-sets-lot01.md`

## Conclusion

Le Lot 01 remplit son périmètre d’audit/contrat. Il ne constitue pas une validation téléphone et ne modifie aucun comportement de jeu. Le prochain lot prévu par le contrat est Lot 02 : manifeste canonique + résolution centrale + équivalence du set actuel.
