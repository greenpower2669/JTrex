# JTREX — TODO VIVANT

Dernière consolidation : 2026-10-07

## JT-SETS-001
- [x] Lots 01–05 terminés.
- [x] Fab a validé explicitement les six champs Lot 06 et leurs bornes.
- [x] Contrat Lot 06 enregistré.
- [x] `parameters:{}` rétrocompatible.
- [x] Validation bornes/min/max, bool/NaN/infini/clés étrangères.
- [x] Édition atelier des six coefficients seulement.
- [x] Application au set de session figé / test brouillon.
- [x] Coûts, mécanismes, jalons, énergie dérivée, chrono, KO, score, EOS inchangés.
- [x] Validation patch 173/173.
- [x] Garde CI Lot 06 corrigé en RED→GREEN.
- [x] Android #89 `37576480368` SUCCESS ; 174/174 tests ; BUILD SUCCESSFUL.
- [x] APK 156528315 octets ; SHA-256 `4f40880fae9b3a4cc3a20175216bbd02cda7ab731c261c4ad7ca36449e4039ef`.
- [ ] Validation téléphone réelle du candidat Lot 06.

## État
JT-SETS-001 techniquement complet côté code/CI.

## Interdictions
- Pas de merge `main`.
- Pas de Release automatique.
- Pas d'AAB sans ordre explicite.
- Pas de gameplay dupliqué par set.


## JT-SETS-UI-001 — correction téléphone
- [x] Audit capture + code : bandeau 520dp, catalogue/brouillons/assistant sans scroll.
- [x] Autorisation Fab.
- [x] Sélecteur compact `SET ▼` + ✎ admin.
- [x] Menu atelier + création scrollables.
- [x] Catalogue des sets scrollable.
- [x] Liste des brouillons scrollable.
- [x] Assistant set scrollable + navigation compacte.
- [x] Tests de contrat UI ajoutés.
- [ ] CI Android fraîche + APK à valider sur téléphone.


## JT-SETS-UI-002 — finition téléphone
- [x] Prompt de passation enregistré.
- [x] Sélecteur SET centré et encore compacté.
- [x] Glyphes Android remplacés par `SET v` / `MOD`.
- [x] Boutons atelier/assistant/preview réduits et davantage espacés.
- [x] Cause de l'aperçu fermé corrigée.
- [x] Test première frame/preview vivant ajouté.
- [x] Garde du dinosaure de sélection droit sans recadrer l'asset.
- [x] Test de bord droit hors viewport ajouté.
- [ ] CI Android fraîche.
- [ ] Validation téléphone Fab.


## JT-SETS-UI-003 — dino droit sans saut
- [x] Retour téléphone #93 : tout validé sauf dino droit.
- [x] Timer post-rendu supprimé du runtime.
- [x] Borne déplacée dans l'affectation historique `self.jb.pos` avant rendu.
- [x] Condition limitée au MENU (`indexa==0`).
- [x] `xb/yb`, taille, asset et dinosaure gauche préservés.
- [x] Garde CI : absence de l'ancien timer + présence de la borne générée.
- [x] Préparation Android #100 verte.
- [x] Tests du moteur généré #100 verts.
- [ ] Build APK #100 terminé.
- [ ] Validation téléphone Fab : absence totale de saut.
