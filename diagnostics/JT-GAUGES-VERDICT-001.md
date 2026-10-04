# JT-GAUGES-VERDICT-001 — restitution des confrontations et verdicts après jauges

Date : 2026-10-03
Branche : `port/android-first-apk`
Base vérifiée au démarrage : `abc0701b21d4c7d37b5a2f11351483c725738802`
Commit test RED : `ad62d52a5d91461cff4b54f5050a2fb2489888ca`
Commit correctif construit : `02269f17ce0c9d00ac1aff1f08838d17a9175c6d`
Run Android : #58 / `37120140189`

## Cause prouvée

Le moteur historique calculait déjà correctement le vainqueur et appliquait les conséquences propres aux jauges, puis revenait à `indexa=1`. Le contrôleur de phases 1.0.12 interprétait alors immédiatement cet état comme retour vers PRE_ROUND/attente. Aucun verdict vidéo 8/9 n'était demandé entre la fin logique de la jauge et ce retour : le résultat visuel était donc escamoté.

Ce n'était pas un recalcul erroné du vainqueur et, avant correctif, ce n'était pas non plus un lecteur 8/9 démarré puis interrompu : le verdict n'était tout simplement jamais demandé.

Les états historiques moteur 8/9 ne peuvent pas être réutilisés directement comme étape logique de sortie de jauge, car ils correspondent aux verdicts d'échange des orbes et possèdent leurs propres impacts historiques. Les exécuter après une jauge appliquerait des conséquences supplémentaires ou doubles.

## Rouge / bleu

Chemin historique :

`4 (confrontation RB)` → taps rouge/bleu → `3` si ST gagne ou `2` si TR gagne → conséquence historique propre à la jauge → `1`.

Chemin corrigé de présentation :

`4` → décision moteur `3` ST / `2` TR → conséquence historique unique → moteur `1` → `GAUGE_VERDICT` → présentation média uniquement `8` ST / `9` TR → vrai EOS → PRE_ROUND → ROUND/START → ROUND_ACTIVE.

Le moteur reste réellement à `indexa=1` pendant `GAUGE_VERDICT`. Les orbes, entrées et chronos restent gelés.

## Jaune

Chemin historique :

`7 (départage jaune)` → taps jaunes → `5` si ST gagne ou `6` si TR gagne. Le chemin ST poursuit historiquement `5 → 3 → 1`; le chemin TR finit `6 → 1`. Les conséquences historiques sont appliquées avant le retour à 1.

Chemin corrigé de présentation :

`7` → décision moteur `5` ST / `6` TR → conséquence historique unique → moteur `1` → `GAUGE_VERDICT` → présentation média uniquement `8` ST / `9` TR → vrai EOS → PRE_ROUND → suite normale.

Les cas neutres 4/7 ne demandent aucun verdict ST/TR supplémentaire et conservent leur comportement historique.

## Médias utilisés

- ST : `assets/combat/Stegtrexresultstegwin.mp4`
- TR : `assets/combat/Stegtrexresulttrexwin.mp4`

Le mapping 8/9 sert ici uniquement à sélectionner le média existant. Il n'est pas injecté dans `engine["indexa"]`.

## Implémentation

`tools/jtrex_phase_runtime.py` :

- ajout de la phase gelée `GAUGE_VERDICT` ;
- mapping de présentation `{2:9, 3:8, 5:8, 6:9}` ;
- maintien de l'état moteur réel à 1 ;
- sélection du média verdict via le contrôleur existant ;
- libération uniquement au vrai EOS du lecteur correspondant ;
- garde génération/lecteur conservée ;
- repli borné en cas d'échec média ;
- aucun effet de combat, débit/crédit d'énergie ou recalcul au moment de l'EOS.

Aucun changement à la formule de score, au seuil d'égalité, aux dégâts, au soin, aux probabilités IA, aux gains d'énergie, aux coûts, au pruning, aux médias ni à la chaîne native Android.

## TDD et validation

Le test a été écrit avant le correctif. Run #57 : 19 tests exécutés, quatre échecs attendus, exactement les quatre verdicts demandés. La phase observée était PRE_ROUND au lieu de GAUGE_VERDICT.

Après le correctif, run #58 : l'étape `Exercise actual generated engine and presentation phases` est verte avec 19 tests. Cas couverts :

- rouge/bleu victoire ST ;
- rouge/bleu victoire TR ;
- jaune victoire ST ;
- jaune victoire TR ;
- média correct ;
- aucune phase d'orbes intercalée pour décider le résultat ;
- dégâts inchangés pendant la présentation et après EOS ;
- chronos/orbes gelés durant le verdict ;
- reprise PRE_ROUND après EOS ;
- cas neutres conservés par les tests historiques.

Le run Android #58 s'est terminé `success`, y compris `Build debug APK`, collecte et upload.

## APK du run #58

- fichier : `JuneT-Rex-1.0.12-debug.apk`
- taille : `148269448` octets
- SHA-256 : `fcab869588ee611947c2f262f8e0b76f4af86282342f857a04140ea34018697a`
- SHA confirmé identique au `SHA256SUMS.txt` produit par le workflow.
- artifact GitHub : `11272809174` (`JuneT-Rex-1.0.12-debug`)

Le code/tests/build sont validés. La restitution visuelle/sonore et le ressenti de séquence restent à valider par Fab sur téléphone. Aucun merge `main` et aucune release ne sont effectués par cette mission.
