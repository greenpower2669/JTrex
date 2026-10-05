# JT-SETS-001 — Lot 01 — Inventaire prouvé

Date : 2026-10-05
Mission : `JT-SETS-001`
Branche : `feature/dinosaur-sets-v1`
Base de mission : `ce858fe57b395c2a52967dc0e8acdd92ff6aa81e`

## 1. Baseline reproductible

### Source d’autorité

Le `app/main.py` Android n’est pas une source versionnée. Il est généré à partir de l’archive historique officielle `JuneTrex.zip` par `tools/prepare_android.py`.

Archive officielle, Release/tag `JTrex` :
- taille : `327992765` octets ;
- SHA-256 : `f73ca1fd5e96ca6e11df5987bda8b2e59ebac26b1beb23fe34883b15bee66647`.

Source historique `main.py` attendue par le préparateur :
- SHA-256 : `3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231`.

Main Android réellement préparé avec le code courant de la branche :
- SHA-256 : `5e1a25b3d149bc82a7bad7361760c3f53574d4898c43479456a389b83b84c68f`.

Le rapport `app/android-preparation.json` produit par la chaîne confirme les trois empreintes ci-dessus et indique notamment Python cible `3.12.14`, version application `1.0.15`, numeric version `115` et package `com.junedady.junetrex`.

### Exécution de preuve

Le conteneur de travail de cette session ne pouvait pas résoudre GitHub pour un `git clone` / `curl` direct. Ruling d’exécution : utiliser un workflow GitHub Actions temporaire sur la branche de mission afin d’exécuter exactement la génération contre la Release officielle, puis supprimer ce workflow avant clôture du Lot 01. Coût si ce choix était erroné : une différence d’environnement d’audit ; mitigation : même OS CI Ubuntu 24.04 que la chaîne Android et même `tools/prepare_android.py`, avec contrôle préalable taille/SHA de l’archive.

Workflow temporaire : `JT-SETS-001 Lot01 Diagnostic`.

Preuves fraîches :
- run #1 : `37339520665` — GREEN ;
- run #2 : `37339853652` — GREEN ;
- head du run #2 : `4b883f6e1fad5003426b598fbed0036a890039f3` ;
- vérification `ce858fe57b...` ancêtre de HEAD : PASS ;
- vérification taille/SHA archive : PASS ;
- préparation `JuneTrex.zip -> app/main.py` : PASS ;
- artefact de preuve run #2 : `JT-SETS-001-Lot01-Evidence`, id `11358400072`, SHA-256 d’artefact `734651b6f532aa6079f543ff2e1a27fce83fbb512fd542877466ab46eada5c21`.

Commande canonique exécutée :

```text
python3 tools/prepare_android.py --archive JuneTrex.zip --output app --spec buildozer.spec
```

`JuneTrex.zip` et `app/` restent des produits temporaires de génération et ne doivent pas être ajoutés au dépôt.

### Baseline de tests

Commande exécutée dans le run diagnostic :

```text
python3 -m unittest discover -s tests -v
```

Résultat : `Ran 38 tests` — `OK`.

Les tests comprennent notamment les gardes de taille des médias, le média d’attente canonique, le chrono orbes, les phases, le contrat KO/rounds et le modèle de round.

Deux `SyntaxWarning: invalid decimal literal` provenant du source historique généré sont visibles dans le harness ; ils n’ont provoqué aucun échec de test et ne sont pas modifiés dans ce lot d’audit.

## 2. Statut après Task 1

Baseline générée et tests prouvés. Aucun runtime de sets, manifeste actif, menu, import/export, atelier, gameplay ou asset n’a été modifié par Task 1.
