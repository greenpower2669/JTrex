# JTrex / June T-Rex — Ordres de mission

## ODM-JTREX-001 — Reconstruction documentaire avant portage Android

### Statut

MISSION DOCUMENTAIRE.

Cette mission crée la mémoire durable du projet. Elle ne constitue pas une autorisation de modifier le jeu.

### Autorité et rôles

Fab dirige le projet et valide le comportement sur téléphone.

La reconstruction fonctionnelle fournie par Astra sert de source documentaire pour la transcription dans :

- brain.md ;
- brainmap.md ;
- debughistorical.md ;
- todo.md ;
- ordres-de-mission.md.

Le travail doit respecter l'esprit FAB Copilot et le protocole FAB Human Sol Slaves : préserver l'intention de Fab, transmettre une connaissance vérifiable, distinguer ce qui est observé de ce qui est supposé, et ne pas transformer une mission documentaire en correction autonome.

### Références

Dépôt :
https://github.com/greenpower2669/JTrex

Révision main :
164d03be77c83f49e1094294f36f860ec183df68

Release :
https://github.com/greenpower2669/JTrex/releases/tag/JTrex

Archive :
https://github.com/greenpower2669/JTrex/releases/download/JTrex/JuneTrex.zip

Programme de référence :
JuneTrex/main.py

SHA-256 :
3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231

Le main.py de « June air hockey » n'est pas la référence JTrex.

### Objectif fonctionnel à mémoriser

JTrex est un jeu d'adresse compétitif à deux camps avec :

- trois orbes rouge/vert/bleu par camp ;
- arrêt des orbes par trois boutons de couleur ;
- comparaison de précision ;
- séquences de dinosaures image par image ;
- confrontations spéciales au tapotement ;
- vie ;
- énergie ;
- trois pouvoirs par camp ;
- modes humain/ordinateur indépendants ;
- cinq niveaux indépendants ;
- deux chronomètres ;
- états de fin et retour menu.

La référence exacte des règles et formules est dans brain.md.
La localisation technique de ces règles est dans brainmap.md.

### Objectif futur

Préparer à terme un portage Android propre et installable.

Ce futur portage devra d'abord reproduire le comportement historique validé avant toute simplification.

Livraison future attendue, lorsque Fab l'autorisera :

- nom/version cohérents ;
- icône Android ;
- APK installable 📦 ;
- AAB séparé si nécessaire pour la diffusion 📦.

### Souhait futur médias

Fab souhaite retrouver les vidéos originales et remplacer plus tard les séries d'images par de vraies vidéos.

Ce souhait est reporté.

Interdictions actuelles :

- ne pas rechercher activement ces vidéos dans cette mission ;
- ne pas convertir les JPEG en vidéos ;
- ne pas supprimer les séries ;
- ne pas modifier les timings ;
- ne pas fusionner des embranchements ;
- ne pas inventer une vidéo de remplacement.

### Interdiction de coder

Pendant ODM-JTREX-001 :

- aucune modification de main.py ;
- aucune modification de main.kv ;
- aucune modification de buildozer.spec ;
- aucune modification du workflow Android ;
- aucune modification de ressource ;
- aucune correction des observations JT-OBS ;
- aucun build ;
- aucun déploiement ;
- aucune publication de release.

Seuls les fichiers documentaires du cerveau du projet peuvent être créés ou mis à jour.

### Mémoire obligatoire

brain.md doit décrire le jeu et ses règles.

brainmap.md doit expliquer où ces règles se trouvent et comment elles s'enchaînent techniquement.

debughistorical.md doit conserver les anomalies et incertitudes sans les déclarer corrigées.

todo.md doit décrire l'état réel, les validations à faire et le prochain geste.

Aucune mémoire antérieure ne doit être écrasée silencieusement lors des mises à jour futures. En cas de divergence de référence, conserver l'historique et signaler explicitement la nouvelle source.

### Organigrammes obligatoires

La brainmap doit conserver des diagrammes distincts pour :

1. menu et cycle complet ;
2. arrêt des orbes et comparaison ;
3. embranchements rouge/bleu ;
4. embranchements jaunes ;
5. disponibilité/utilisation/effet des pouvoirs ;
6. fin de combat et retour menu.

Ces schémas doivent représenter le programme actuel, y compris ses exceptions. Ils ne doivent pas remplacer la réalité par un comportement idéal.

### Registre d'observations

JT-OBS-001 à JT-OBS-026 sont des observations documentaires.

Certaines asymétries peuvent être volontaires. Une observation ne devient un bug à corriger qu'après validation de Fab.

### Passation

À la fin de cette mission documentaire :

- le cerveau fonctionnel existe ;
- la cartographie technique existe ;
- le registre des observations existe ;
- le TODO sépare documentation, validation et portage futur ;
- aucun code n'a été touché.

Toute phase suivante exige un nouvel ordre explicite de Fab.


### Contrôle de complétude documentaire

Après création initiale des mémoires, une relecture croisée avec le relais Astra a été effectuée pour vérifier la fidélité de transcription.

Les détails qui restaient implicites ont été rendus explicites dans brain.md et brainmap.md, notamment le suivi tactile choixidh/choixidb, colv[7..9], les limites exactes du hash et de l'inventaire, les variantes de ressources horseg2ko et certaines nuances de l'héritage tactile.

Ce contrôle reste strictement documentaire : aucun code, média, build, workflow ou comportement n'a été modifié.


## JT-ANDROID-001 — Premier APK installable de June T-Rex

### Statut
MISSION ACTIVE SUR BRANCHE DÉDIÉE — PHASE 1 : DOSSIER ASTRA.

Branche : `port/android-first-apk`
SHA de départ : `379ae278f2199cad26f1746c418512f47e04d106`

Objectif : produire un premier APK 📦 installable et fidèle au jeu historique, puis un AAB 📦 distinct si la chaîne le permet. La validation finale du gameplay appartient à Fab sur téléphone.

Rôles :
- Fab dirige, arbitre les changements de comportement et teste sur téléphone.
- Astra analyse les extraits/données ciblés et prépare les corrections nécessaires.
- Sol prépare les sources, applique les corrections validées, gère Git, build, livraison et mémoires.

Invariants : ne pas réécrire le jeu, ne pas rééquilibrer, ne pas moderniser globalement, ne pas ajouter d'IA de tapotement, ne pas remplacer les séquences par des vidéos et ne pas supprimer le moteur Air Hockey hérité sans preuve et ordre distinct.

Source de jeu : asset `JuneTrex.zip` de la release/tag `JTrex`, racine explicitement `JuneTrex`. Ne jamais dépendre de « latest » ni du premier `main.py` trouvé.

Adaptations autorisées : compatibilité Android, chemins/casse des ressources, configuration/workflow, identité/version/icône, diagnostics bornés et corrections ciblées d'un blocage Android démontré.

La branche ne doit pas être fusionnée automatiquement dans main avant retour de Fab.
