# PASSATION — JTREX / JT-SETS-UI-002

Date : 2026-10-07  
Repo : `greenpower2669/JTrex`  
Branche : `feature/dinosaur-sets-v1`  
Base téléphone avant ce lot : `15d2c5ef037d9875c384082058ee2ef2f41ccbee`  
Build précédent validé CI : Android #90, run `37637464474`, SUCCESS.

## Demande téléphone de Fab

1. Centrer le sélecteur de set.
2. Réduire encore les boutons et les textes ; conserver la lisibilité mais éviter les pavés pleine largeur.
3. Aérer davantage l'atelier.
4. Réparer APERÇU ACTUEL / APERÇU REMPLACEMENT : la capture affichait `Aperçu fermé`.
5. Le dinosaure de sélection placé à droite utilise volontairement une image dont le corps est tronqué au bord droit. Ne PAS modifier, recadrer ou redimensionner l'asset. Empêcher seulement ce dinosaure d'aller trop à gauche afin que le bord tronqué reste hors écran.

## Audit frais

- Le bug aperçu est déterministe : `_workshop_preview_current_action()` démarrait le décodeur, puis `_open_workshop_preview_popup()` appelait immédiatement `_close_workshop_preview_popup()`, ce qui déchargeait le lecteur fraîchement créé.
- L'APK #90 contient les rectangles historiques `jh` / `jb` ; leurs sources animées incluent `g/g_*.png` et `d/d_*.png`. Le garde de cadrage vise uniquement le rectangle visible le plus à droite en MENU et ne doit jamais ramener à l'écran un rectangle volontairement caché.
- Les glyphes `▼` et `✎` sont mal rendus sur le téléphone ; utiliser des libellés ASCII `SET v` et `MOD`.

## Portée autorisée

UI/preview seulement dans `tools/jtrex_media_runtime.py` + tests associés.  
Aucun changement de gameplay, dégâts, soin, coûts, énergie, score, KO, rounds, états 21..26, jalons 181..186, EOS ou médias.

## Correctif appliqué

- groupe `SET v <nom>` + `MOD` centré ;
- dimensions plus compactes ;
- boutons atelier/assistant/preview plus étroits et plus aérés ;
- fermeture d'un ancien aperçu AVANT de démarrer le nouveau, jamais après ;
- statut `Chargement vidéo…` tant que la première frame n'est pas reçue ;
- garde MENU du dinosaure droit : conserver son bord droit au-delà du viewport avec petite marge de sécurité, sans toucher à l'asset ni à sa taille ;
- tests de régression : preview reste playing + première frame visible, sélecteur centré, bord tronqué du dinosaure au-delà du viewport ;
- nettoyage du timer et du bouton MOD au shutdown.

## Commits code

- `3f4bdd546a0f20c1f860db654e4af33b20f81e03` — preview, centrage, garde dinosaure ;
- `42567738fab1c5cd3ccdf5f6012f0e100db8c616` — compacité/aération atelier ;
- `2768aca290722aec246b0ceae22c88bb4fca5d77` — tests de régression.

## Interdictions

- aucun merge `main` ;
- aucune Release ;
- aucun AAB ;
- ne pas modifier les images dinosaures ;
- ne pas dupliquer le moteur par set.

Suite : attendre la CI Android fraîche, puis validation téléphone Fab.
