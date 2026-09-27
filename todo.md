# JTrex / June T-Rex — TODO

## État actuel

Phase : RECONSTRUCTION DOCUMENTAIRE AVANT PORTAGE ANDROID.

Référence fonctionnelle : JuneTrex/main.py de la release JTrex, SHA-256 3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231.

Révision main servant de référence : 164d03be77c83f49e1094294f36f860ec183df68.

Interdictions actuelles :

- ne modifier aucun code ;
- ne supprimer aucun bloc hérité ;
- ne renommer ou convertir aucun média ;
- ne corriger aucune JT-OBS ;
- ne changer aucun réglage Buildozer/workflow ;
- ne lancer aucun build ni déploiement dans la mission documentaire ;
- ne rechercher/remplacer les vidéos originales qu'après nouvelle autorisation de Fab.

## Terminé dans cette mission documentaire

- [x] Créer le cerveau fonctionnel JTrex dans brain.md.
- [x] Cartographier classes, fonctions, variables, états, callbacks et Android dans brainmap.md.
- [x] Consigner JT-OBS-001 à JT-OBS-026 dans debughistorical.md.
- [x] Séparer constats, conséquences à confirmer et intentions à valider.
- [x] Documenter le moteur air hockey comme héritage encore exécuté.
- [x] Documenter les séries d'images et leurs indices.
- [x] Documenter les deux chronomètres car et car2.
- [x] Documenter l'IA et les cinq niveaux.
- [x] Documenter les six pouvoirs et leur asymétrie.
- [x] Documenter les confrontations rouge/bleu et jaunes.
- [x] Ajouter six organigrammes Mermaid du comportement actuel.
- [x] Enregistrer l'ordre de mission et l'objectif futur Android.

## À valider avec Fab avant toute modification fonctionnelle

- [ ] Nom complet historique de ST si une documentation utilisateur l'exige.
- [ ] Noms complets des six pouvoirs ; ne pas les déduire de sf/ls/ta/fs/ph/ma.
- [ ] Confirmer si le seuil S différent gauche/droite est voulu.
- [ ] Confirmer si les asymétries d'énergie sont voulues.
- [ ] Confirmer le comportement voulu en cas de double KO.
- [ ] Confirmer le comportement voulu de l'IA dans les confrontations au tapotement.
- [ ] Confirmer l'intention de conservation ou de retrait futur du moteur air hockey une fois ses dépendances prouvées.
- [ ] Confirmer le comportement attendu du soin état 22.

## Validation future du jeu de référence — seulement après autorisation

- [ ] Démarrer une partie humain/humain.
- [ ] Vérifier rouge/vert/bleu à gauche et à droite.
- [ ] Arrêter les trois orbes d'un camp avant l'autre.
- [ ] Laisser car2 forcer l'arrêt des six orbes.
- [ ] Comparer un échange gagné à gauche puis à droite.
- [ ] Obtenir une égalité et vérifier l'état jaune.
- [ ] Faire basculer une confrontation avec une puis trois touches d'avance.
- [ ] Vérifier la continuité d'images lors d'un changement de variante.
- [ ] Tester séparément les six pouvoirs.
- [ ] Comparer énergie=60 et énergie>60.
- [ ] Vérifier qu'un pouvoir utilisé ne redevient pas disponible pendant le même combat.
- [ ] Observer le soin avec vie très basse et vie presque pleine.
- [ ] Tester une fin gauche, une fin droite et un double KO.
- [ ] Vérifier le retour menu puis une deuxième partie.
- [ ] Tester les cinq niveaux et les quatre combinaisons humain/ordinateur.
- [ ] Observer l'ordinateur pendant les phases de tapotement.
- [ ] Comparer le score sur plusieurs tailles de fenêtre.
- [ ] Appuyer à l'emplacement d'une commande graphiquement masquée.
- [ ] Vérifier pause/reprise.
- [ ] Vérifier quel main.py le workflow Android sélectionne réellement.

## Préparation future du portage Android — ne pas commencer ici

Ordre recommandé après validation du comportement historique :

1. figer une version de référence reproductible ;
2. sélectionner explicitement JuneTrex/main.py dans le pipeline ;
3. vérifier les ressources sensibles à la casse ;
4. vérifier l'image absente charge tr win 83 sans substitution automatique ;
5. vérifier dimensions/ratios des séries ;
6. décider quelles dépendances du moteur air hockey sont encore nécessaires ;
7. définir une architecture Android qui reproduit d'abord le comportement observé ;
8. conserver les formules de score, dégâts, énergie et timers jusqu'à validation ;
9. ajouter nom/version/icône cohérents ;
10. produire et tester un APK installable ;
11. produire un AAB séparé si la diffusion Play l'exige.

## Médias futurs

Après stabilisation du portage seulement :

- [ ] Retrouver les vidéos originales.
- [ ] Établir une table vidéo ↔ séquence d'images.
- [ ] Comparer timing, événements d'impact, audio et embranchements.
- [ ] Faire valider par Fab.
- [ ] Remplacer progressivement les séries, sans perte des états 2–7 ni des bifurcations.

## Prochain geste

Ne rien coder à partir de cette seule reconstruction.

Le prochain geste autorisable est une phase de validation d'exécution de la référence historique ou un nouvel ordre de mission explicite de Fab.


## Audit de complétude du relais Astra

- [x] Relire le relais Astra contre les cinq mémoires.
- [x] Rendre explicites choixidh/choixidb.
- [x] Rendre explicite le rôle temporel non normalisant de colv[7..9].
- [x] Conserver les limites de provenance : hash main.py seulement, variantes historiques non comparées, séries non toutes vérifiées visuellement.
- [x] Consigner les variantes/sauvegardes horseg2ko sans substitution automatique.
- [x] Conserver les nuances du suivi tactile hérité.
- [x] Confirmer qu'aucune correction de code ni validation d'exécution n'a été effectuée.


## JT-ANDROID-001 — Premier APK installable

État : DOSSIER ASTRA EN PRÉPARATION / AUCUN CODE MODIFIÉ.

- [x] Lire les cinq mémoires à la référence actuelle.
- [x] Vérifier que main est sur `379ae278f2199cad26f1746c418512f47e04d106`.
- [x] Créer `port/android-first-apk` depuis cette référence.
- [x] Lire le buildozer.spec actuel.
- [x] Lire le workflow Android actuel.
- [x] Vérifier les métadonnées de la release/tag JTrex et le digest de JuneTrex.zip.
- [x] Confirmer que le workflow actuel dépend de `releases/latest` et du premier `main.py`.
- [ ] Faire valider/proposer par Astra les modifications Android ciblées.
- [ ] Appliquer uniquement les modifications proposées et justifiées.
- [ ] Construire l'APK 📦.
- [ ] Installer/exécuter si un environnement compatible est disponible ; sinon marquer « à valider par Fab ».
- [ ] Préparer l'AAB 📦 si la chaîne le permet.
- [ ] Publier une préversion de test seulement après contrôles.

Prochain geste : transmettre à Astra le dossier ciblé JT-ANDROID-001. Aucun gameplay ne doit être modifié.


## JT-ANDROID-001 — patch Astra appliqué

- [x] Ajouter `tools/prepare_android.py`.
- [x] Figer la release source `JTrex` et la racine `JuneTrex`.
- [x] Vérifier archive et main historique par empreintes avant adaptation.
- [x] Préparer les corrections de casse uniquement sur la copie de compilation.
- [x] Passer le candidat à version 1.0.1 / numeric version 101.
- [x] Configurer l'icône provisoire `pter/pter0.png`.
- [x] Conserver JT-OBS-003 sans remplacement d'image.
- [x] Remplacer le workflow par le build APK ciblé et diagnostics bornés.
- [ ] Examiner le résultat réel de GitHub Actions.
- [ ] Relever Buildozer et python-for-android réellement utilisés.
- [ ] Si APK produit : vérifier taille, SHA-256, package/version/architectures/signature avec les outils disponibles.
- [ ] Rapporter à Astra les logs/diagnostics et le commit exact.
- [ ] Validation téléphone par Fab.
- [ ] AAB après stabilisation APK.


## JT-ANDROID-001 — résultat run #7

- [x] Préparation archive/main vérifiée.
- [x] Buildozer et python-for-android réellement identifiés.
- [x] Diagnostic complet récupéré.
- [ ] Corriger l'échec native libffi/autoreconf uniquement après proposition Astra.
- [ ] Relancer un scénario identique après une seule correction discriminante.
- [ ] Produire l'APK 📦.
- [ ] Vérifier statiquement package/version/architectures/signature.
- [ ] Faire valider sur téléphone par Fab.

Blocage actuel précis :
`configure.ac:215: error: possibly undefined macro: LT_SYS_SYMBOL_USCORE`.

Prochain geste : transmettre à Astra le run #7, les révisions d'outillage et cette première erreur pertinente.


## JT-ANDROID-001 — FAB-DEBUG-001 essai n°1

- [x] Hypothèse unique reçue : ajouter `libltdl-dev`.
- [x] Limiter la modification à `.github/workflows/android.yml`.
- [ ] Relancer le même build.
- [ ] Vérifier si `autoreconf` franchit `LT_SYS_SYMBOL_USCORE`.
- [ ] Si nouvelle erreur : consigner uniquement la première nouvelle erreur discriminante.
