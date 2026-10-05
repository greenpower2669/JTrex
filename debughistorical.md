# JTREX — DEBUG HISTORICAL VIVANT

Dernière consolidation : 2026-10-05

## Rôle
Conserver uniquement les faits de diagnostic encore utiles à JT-SETS-001 et les protections canoniques. Historique intégral : `archive/memories/2026-10-04-pre-main-merge/debughistorical.md`.

## Baseline vérifiée
- `main` au démarrage JT-SETS-001 : `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
- Parent fonctionnel : `976344c39dec9bb88ef8f7e18e703f2ed2659d07`.
- Build #78 / `37245309424` : CI verte.
- Validation téléphone complète non enregistrée dans les mémoires.
- Dernière Release : `v1.0.15-main`.

## Résolus — ne pas rouvrir sans preuve
### Bootstrap Android / zlib
Ancien crash natif résolu ; préserver la chaîne Python 3.12.14 / FFmpeg 6.1.2 / ffpyplayer 4.5.1.

### KO / rounds / chrono / énergie
- verdict de jauge != victoire de round ;
- KO réel seul incrémente un round ;
- deux rounds terminent le match ;
- nouvel échange = `car2=10` + stops nettoyés ;
- retour pouvoir = temps restant ;
- vrai nouveau round = énergie 0/0.

### Média
- wait canonique : `assets/combat/StegTrexPlageVideoenboucledesorbes.mp4` ;
- EOS wait sans gameplay ;
- pouvoirs/finishings protégés jusqu’à EOS réel si requis.

## Points de risque JT-SETS-001
1. `app/main.py` n’est pas versionné : l’inventaire doit porter sur le fichier généré depuis `JuneTrex.zip`.
2. `jtrex_phase_runtime.py` ajoute actuellement ZeroWin dans le dictionnaire global `SCENES` : avec plusieurs sets, éviter toute mutation globale susceptible de fuir entre sessions/aperçus.
3. `MEDIA_ASSETS` est une garde réelle testée par taille : la migration vers manifests ne doit pas supprimer cette preuve.
4. Changer de set doit invalider lecteurs/callbacks/générations sans permettre à un ancien EOS d’agir sur une nouvelle session.
5. Les aperçus admin ne doivent jamais réutiliser les callbacks combat.
6. Paramètres de dégâts/soins peuvent modifier indirectement l’énergie ; aucun champ d’équilibrage ne sera exposé sans inventaire et validation Fab.

## Règle
Aucune régression déclarée ou corrigée sans reproduction/preuve fraîche. Tests CI != validation téléphone.
