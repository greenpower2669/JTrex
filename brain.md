# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-05

## Mission active
JT-SETS-001 sur `feature/dinosaur-sets-v1` ; base `main@ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
But : plusieurs sets DATA + MEDIA, un seul moteur, set canonique équivalent.

## Lots acquis
### Lot 01
- Inventaire, contrat v1 et preuves dans `docs/jt-sets-001/`.
- Archive canonique : 327992765 octets, SHA `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.
- Main préparé SHA `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.

### Lot 02
- `tools/jtrex_sets_runtime.py` = contrat/résolveur DATA-only fermé.
- `assets/sets/catalog.json` + `assets/sets/trex_vs_steg/manifest.json` = source officielle, 41 assets taille+SHA.
- `prepare_android.py` et runtime média consomment cette source de vérité.
- Policies `loop`/`play_to_end`, états, EOS, jalons, coûts et gameplay restent moteur-owned.
- ZeroWin ne mute plus le catalogue global.
- Commit produit `017d611cf798d4713af8039ee6962d1fe6729fd2` ; run `37378554085` = 56/56 OK.
- Workflow Android exact au commit `ee8cf297830e1f40d984ab6b1706733eff22e5d7`, blob `c22bcf40038889318a3cab7c25d6c8c78dd87c49`.
- APK final : run #80 `37379193862` GREEN ; artefact APK `11375685200` ; `JuneT-Rex-1.0.15-debug.apk` = 156461520 octets, SHA-256 `182e1b8f72f269a7e3f3f24895e37fe23a1b3ade9e77949d14500827c13c320c`.

## Canon gameplay
- 3 orbes/camp ; nouvel échange 10 s ; retour pouvoir conserve le temps.
- KO réel seul ; 2 rounds = match ; vrai nouveau round énergie 0/0.
- Vie 500000000/camp ; score historique inchangé.
- Coûts 60/40/60/60/60/80 ; disponibilité `energy > cost`.
- Impacts au jalon historique ; EOS n'applique aucun effet supplémentaire.

## Format v1
- manifeste fermé/versionné DATA-only ; left/right explicites ; 9 rôles média ; 6 pouvoirs ; assets id/path/type/size/SHA-256 ;
- aucun Python/KV/script/formule ; `parameters:{}` fermé jusqu'au Lot 06.

## Prochain geste
Lot 03 : catalogue/menu joueur, sélection persistante, set figé pendant le match, fallback sûr sur le canon. Pas de merge `main` ni Release sans Fab.
