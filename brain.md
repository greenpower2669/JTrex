# JTREX — BRAIN VIVANT

Dernière consolidation : 2026-10-05

## Mission active
JT-SETS-001 est autorisée par Fab.
Branche : `feature/dinosaur-sets-v1`.
Base : `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`.
Design : `docs/superpowers/specs/2026-10-05-jtrex-dinosaur-sets-design.md`.

But : plusieurs sets de confrontations DATA + MEDIA, un seul moteur de gameplay, set canonique inchangé.

## Canon gameplay
- 3 orbes par camp ; nouvel échange = 10 s.
- Retour de pouvoir = temps restant.
- KO réel seul = victoire de round ; 2 rounds = match.
- Nouveau vrai round : énergie gauche/droite = 0.
- Vie : 500000000 par camp.
- Score : `max(0,150000000-Σe³)` ; égalité si différence < 20000.
- Coûts slots 1..6 : 60/40/60/60/60/80.
- Activation : énergie strictement > coût ; énergie fractionnaire.
- Effets appliqués une seule fois, jamais à EOS.

## Architecture actuelle vérifiée
- `JuneTrex.zip` -> `tools/prepare_android.py` -> `app/main.py` généré.
- `tools/jtrex_phase_runtime.py` : phases, rounds, KO, chrono.
- `tools/jtrex_media_runtime.py` : intros/scènes, EOS, boucle attente, admin 20 touches.
- `app/main.py` n’est pas versionné.
- `prepare_android.py` centralise actuellement les coûts et `MEDIA_ASSETS`.
- `jtrex_phase_runtime.py` injecte aujourd’hui ZeroWin dans le catalogue global : point à découpler pendant JT-SETS-001.

## Cible JT-SETS-001
- manifeste fermé/versionné ;
- catalogue officiel + sets utilisateur ;
- résolveur logique central ;
- sélection figée pendant un match ;
- import/export ZIP transactionnel et DATA-ONLY ;
- atelier derrière les 20 touches ;
- aperçus sans callbacks gameplay ;
- paramètres de pouvoirs seulement après inventaire et validation Fab.

## État Android publié/candidat
- Dernière Release : `v1.0.15-main`.
- Build #78 / `37245309424` : CI verte.
- APK candidat SHA-256 : `2fe8016dc3dd98d1c6303fd88c02c04e497490407489636789e291ae20fa0f23`.
- Validation téléphone complète non enregistrée au démarrage de JT-SETS-001.

## Méthode
Relire code/tests/preuves ; synchroniser les cinq mémoires à chaque changement utile ; pas de merge `main` ni Release sans Fab.
