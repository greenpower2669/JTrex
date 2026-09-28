# JTrex / June T-Rex — Brain fonctionnel

## Statut de cette mémoire

Référence documentaire reconstruite avant tout portage Android.

- Mission : documentation uniquement.
- Révision de référence de main : 164d03be77c83f49e1094294f36f860ec183df68.
- Programme étudié : JuneTrex/main.py extrait de la release JTrex.
- SHA-256 du main.py étudié : 3673fb85d12bea18276e485c5956530b4b8c0dda283cacb022e784bfe8c35231.
- Analyse statique : le jeu n'a pas été lancé, testé ni recompilé pendant cette reconstruction.
- Le dossier « June air hockey » présent dans l'archive n'est pas la référence de JTrex.
- Onze variantes historiques de main.py existent dans JuneTrex mais n'ont pas été comparées à la référence.
- Les divergences ou comportements suspects ne sont pas corrigés ici. Ils sont consignés dans debughistorical.md.

## 1. Intention de Fab et identité du jeu

JTrex, aussi nommé June T-Rex, est un jeu d'adresse compétitif à deux camps. Deux joueurs s'affrontent par dinosaures interposés. L'écran regroupe deux ensembles de commandes autour d'une scène de combat commune ; le programme actuel ne construit pas deux caméras indépendantes.

Le cœur voulu par Fab est :

- trois orbes colorés par camp ;
- trois commandes rouge, verte et bleue servant à arrêter les trois orbes dans une fenêtre cible ;
- un score de précision obtenu à partir de la qualité de ces arrêts ;
- le résultat de la comparaison choisit la séquence d'affrontement des dinosaures ;
- une barre d'énergie par camp ;
- trois pouvoirs par camp ;
- certaines confrontations se décident aussi au tapotement ;
- les actions des dinosaures sont actuellement représentées par des séries d'images JPEG lues image par image.

Souhait futur explicitement reporté : retrouver les vidéos originales puis, après validation de Fab, remplacer les séries d'images par de vraies vidéos. Aucun média ne doit être converti, renommé ou remplacé pendant la phase documentaire.

Identifiants historiques :

- camp gauche : g et ST ;
- camp droit : d et TR.

Ne pas inventer le nom complet de ST ou des pouvoirs à partir de leurs seules abréviations.

## 2. États généraux et cycle d'une partie

L'état principal est indexa.

- indexa=0 : menu / insert coin ;
- indexa=1 : phase principale des six orbes ;
- indexa=2,3,4 : confrontation rouge/bleu ;
- indexa=5,6,7 : confrontation jaune ;
- indexa=8 : victoire d'échange du camp gauche ;
- indexa=9 : victoire d'échange du camp droit ;
- indexa=10 : séquence finale ST ;
- indexa=11 : séquence finale TR ;
- indexa=21..26 : six pouvoirs.

Au démarrage :

- musique jtrm0.wav démarrée ;
- deux camps humains ;
- niveaux gauche et droite à 5 ;
- énergie à zéro ;
- six orbes arrêtés ;
- capital de vie de référence de chaque camp : 500 000 000.

Le menu autorise indépendamment, pour chaque camp :

- humain ou ordinateur ;
- niveau S, A, B, C ou D.

Correspondance interne des niveaux :

| Lettre | Valeur |
|---|---:|
| S | 1 |
| A | 2 |
| B | 3 |
| C | 4 |
| D | 5 |

Le bouton Start agit uniquement lorsque indexa==0 et anim1==longanim1[0], soit 11. Son effet direct est indexa=4. Il ne remet pas explicitement anim1 à zéro : la partie démarre donc par l'état 4 avec l'indice hérité du menu. Cette séquence initiale contient un impact partagé avant la phase des orbes.

## 3. Commandes et géométrie

Les quatre couleurs de commande de chaque camp sont :

| Camp | Rouge | Vert | Bleu | Jaune |
|---|---|---|---|---|
| Gauche | gr, orbe 1 | gg, orbe 2 | gb, orbe 3 | gj, confrontation spéciale |
| Droite | dr, orbe 4 | dg, orbe 5 | db, orbe 6 | dj, confrontation spéciale |

Notations de taille :

- W=xmax ;
- H=ymax ;
- mdo=W/19,6 ;
- pgx=W/15 ;
- pgy=H/15.

Taille nominale d'un bouton coloré : W/9,8 × W/9,8.
Taille d'un orbe : mdo × mdo.

Les appuis rouge, vert et bleu arrêtent immédiatement leur orbe dans on_touch_down. Le joueur n'a pas besoin de maintenir le bouton. Le relâchement change seulement l'apparence de la commande et ne relance pas l'orbe.

Les principales zones tactiles sont testées par une distance euclidienne stricte distance < sensibilité. Pour les boutons colorés à l'appui, le rayon est 1,2*mdo.

Les commandes sont dessinées par Rectangle et testées manuellement. Masquer un rectangle par une taille nulle ne désactive donc pas automatiquement son test tactile.

Les différents tests tactiles sont des if indépendants : un même toucher peut être examiné par plusieurs zones successives.

## 4. Phase d'adresse des six orbes

La phase principale correspond à indexa=1.

Coordonnées horizontales :

- gauche : 0,15*pgx ; 0,65*pgx ; 1,00*pgx ;
- droite : 13,25*pgx ; 13,70*pgx ; 14,10*pgx.

Hauteurs initiales par couleur :

- rouge : 8,7*pgy ;
- vert : 4,7*pgy ;
- bleu : 11,7*pgy.

Cible mathématique :

haut[7]=7,7*pgy.

Limites :

- haute : haut[8]=0,8*H ;
- basse : haut[9]=0,25*H.

À chaque appel de colvv, un orbe mobile avance selon :

haut[i] += colvv[i] * colv[i]

Le sens est inversé après dépassement d'une limite. La position n'est pas immédiatement recadrée sur la limite.

colvv est demandé toutes les 0,04 seconde, donc nominalement 25 mises à jour/s. Le pas n'est pas multiplié par le temps réellement écoulé ; la vitesse effective dépend du rythme des callbacks.

Vitesses / pas selon le niveau :

| Niveau | Lettre | Rouge | Vert | Bleu |
|---:|---|---:|---:|---:|
| 1 | S | 35 | 28 | 31 |
| 2 | A | 33 | 25 | 30 |
| 3 | B | 30 | 23 | 27 |
| 4 | C | 29 | 22 | 26 |
| 5 | D | 28 | 20 | 25 |

Ces valeurs sont des pas par callback dans le repère du programme, pas des pixels par seconde.

Le niveau influence les vitesses même pour un camp humain.

Quand les trois orbes d'un camp sont arrêtés :

- asb calcule l'appréciation ;
- stopg ou stopd passe à True.

Quand les six orbes sont arrêtés pendant indexa=1 :

- colpts calcule les deux scores ;
- stopg et stopd sont remis à False ;
- un état de résultat est choisi ;
- anim1=0 ;
- anim1vv=+1.

À la fin d'une séquence normale 1x, le jeu revient à indexa=1 et les six colstop repassent à False. Les hauteurs et directions des orbes ne sont pas réinitialisées à chaque échange.

## 5. Score de combat

Pour chaque camp, on calcule trois écarts verticaux :

e_i = abs(haut[i] - haut[7])

Score :

S = max(0, 150 000 000 - e_1^3 - e_2^3 - e_3^3)

Le calcul mesure donc une distance verticale à une coordonnée cible et non une surface réelle de recouvrement avec l'image de la fenêtre.

Comparaison :

- si abs(Sg-Sd) < 20 000 : égalité ;
- sinon le plus grand score gagne.

Le seuil est strict : une différence exactement égale à 20 000 n'est pas une égalité.

Résultat :

- égalité → indexa=7 ;
- gauche gagnante → indexa=8 et degdt=Sg ;
- droite gagnante → indexa=9 et deggt=Sd.

Le montant brut prévu est le score complet du gagnant, pas la différence entre scores.

Exemple : écarts gauches 100/100/100 donnent 147 000 000 ; écarts droits 200/200/200 donnent 126 000 000. La gauche gagne et le montant brut prévu contre la droite est 147 000 000.

Deux scores nuls donnent aussi une égalité.

Les coordonnées de fenêtre interviennent dans le score alors que les constantes restent fixes ; l'indépendance à la résolution n'est donc pas établie.

## 6. Lettres de qualité

asb calcule une appréciation séparée du score de combat.

Dans le cas normal où un minimum strict existe parmi les trois écarts :

1. retenir ce minimum ;
2. calculer la moyenne des trois écarts ;
3. si moyenne > minimum + 5,6, utiliser la moyenne.

Seuils supérieurs stricts :

| Appréciation | Seuil |
|---|---:|
| S gauche | 5,6 |
| S droite | 8 |
| AAA | 32 |
| AA | 52 |
| A | 68 |
| B+ | 96 |
| B | 116 |
| B- | 140 |
| C | 168 |
| D | 208 |
| E | 232 |
| F | 320 |

S joue s.wav.
A/AA/AAA jouent a.wav.
B-/B/B+ jouent b.wav.
C à F n'appellent pas de son d'appréciation dans la logique étudiée.

Deux particularités restent à vérifier en exécution :

- si plusieurs écarts sont ex æquo au minimum, les comparaisons strictes peuvent ne retenir aucun minimum et la variable peut conserver une valeur issue du calcul cubique initial ;
- pour une valeur finale >=320, aucune nouvelle image de lettre n'est assignée.

Les lettres sont masquées et leur source repasse à d.png lorsque anim1>25 hors de la phase 1.

## 7. Confrontations au tapotement

Ces confrontations font partie du gameplay actif et doivent être conservées lors d'un futur portage.

### 7.1 Rouge / bleu — états 2, 3 et 4

Rouge ou bleu augmente le compteur du camp si indexa vaut 2, 3 ou 4 et anim1<84.

Le code n'impose pas d'alternance rouge/bleu. Vert n'augmente pas le compteur.

Si un camp prend une avance strictement positive, indexa repasse d'abord à 4.

Avec plus de deux appuis d'avance :

- gauche : indexa=3 ; deggt=tapg*2 000 000 ; degdt=0 ;
- droite : indexa=2 ; degdt=tapd*2 000 000 ; deggt=0.

Il faut donc au moins trois appuis d'avance.

Les changements d'état conservent anim1 : la séquence peut bifurquer en cours de lecture.

### 7.2 Jaune — états 5, 6 et 7

Jaune augmente le compteur si indexa vaut 5, 6 ou 7 et anim1<127.

Avec une avance strictement positive : indexa=7.

Avec plus de deux appuis d'avance :

- gauche : indexa=5 ; deggt=tapg*2 000 000 ; degdt=0 ;
- droite : indexa=6 ; degdt=tapd*2 000 000 ; deggt=0.

### 7.3 Particularité de l'état 5

L'état 5 utilise les images egtrwin comme l'état 6 mais possède un embranchement spécial.

Lorsque anim1 dépasse 127 :

- anim1=85 ;
- indexa=3 ;
- deggt est ajouté aux dégâts reçus à droite ;
- deggt=0.

Sa limite déclarée 9128 ne doit donc pas être comprise comme une séquence réelle de 9 128 images.

### 7.4 Réinitialisations et ordinateur

Plusieurs appuis rouge, bleu ou jaune hors phase admissible remettent les deux compteurs tapg et tapd à zéro.

Aucune génération automatique de tapotements par l'ordinateur n'a été trouvée dans la référence. L'ordinateur sait arrêter les orbes et utiliser les pouvoirs, mais aucune stratégie de tapotement ne doit lui être inventée.

## 8. Vie et dégâts

Capital initial :

pvg=pvd=500 000 000.

Vie restante :

- gauche = pvg-degg ;
- droite = pvd-degd.

degg et degd sont des dégâts cumulés, pas la vie restante.

Impacts principaux :

| État | Déclenchement | Effet brut |
|---:|---:|---|
| 2 | 88 | degg += degdt |
| 3 | 87 | degd += deggt |
| 4 | 85 | +1 000 000 dégâts aux deux ; +19 énergie aux deux |
| 5 | après 127 | degd += deggt puis passage vers état 3 |
| 6 | 130 | degg += degdt |
| 7 | 129 | +1 000 000 dégâts aux deux ; +19 énergie aux deux |
| 8 | 118 | degd += degdt |
| 9 | 94 | degg += deggt |

Dans le bloc commun, les montants temporaires sont ensuite annulés.

Réduction ordinaire appliquée hors du traitement spécial associé à deg[indexa]==182 :

- degg -= (degg-degg0)/4 ;
- degd -= (degd-degd0)/4 ;
- puis degg0 et degd0 sont mis à jour.

Une hausse positive isolée laisse donc normalement 75 % du montant brut dans les dégâts cumulés.

Exemple : 147 000 000 bruts deviennent 110 250 000 dégâts effectifs.
Un impact partagé de 1 000 000 devient normalement 750 000 dégâts par camp.

affpv ramène périodiquement les dégâts négatifs à zéro, toutes les 0,5 s.

## 9. Énergie

Définir :

ΔG=degg-degg0
ΔD=degd-degd0

Hors de l'état associé à deg[indexa]==182 :

- stamg += ΔD / 4 000 000 ;
- stamd += ΔG / 4 000 000.

Le camp gagne donc de l'énergie à partir des dégâts bruts infligés à l'adversaire.

Règle supplémentaire :

- si ΔD<ΔG et deg[indexa]!=182 : stamg += ΔG/10 000 000 ;
- sinon : stamd += ΔD/10 000 000.

Cette branche n'est pas parfaitement symétrique.

Les états 4 et 7 ajoutent auparavant 19 points aux deux camps.

Bornes :

- énergie négative → 0 ;
- énergie >99 → 100 et indicateur de jauge pleine.

La jauge pleine clignote par alternance de visibilité.
Aucune recharge passive temporelle n'a été trouvée.

## 10. Les six pouvoirs

Condition normale :

- indexa=1 pour l'activation humaine ;
- énergie strictement >60 ;
- pouvoir non déjà utilisé.

Une énergie égale à 60 ne suffit pas.

Coût : 60.

Chaque pouvoir possède un selected indépendant, False au début du combat et True après usage. Les six selected sont réinitialisés au retour menu.

| Camp | Slot | État | Son d'appui | Effet brut à l'impact |
|---|---:|---:|---|---|
| Gauche | 1 | 21 | sf.wav | dégâts droite : pvd/4 |
| Gauche | 2 | 22 | ls.wav | soin gauche : degg -= pvg/4 |
| Gauche | 3 | 23 | ta.wav | dégâts droite : pvd/4 |
| Droite | 1 | 24 | fs.wav | dégâts gauche : pvg/4 |
| Droite | 2 | 25 | ph.wav | dégâts gauche : pvg/4 |
| Droite | 3 | 26 | ma.wav | dégâts gauche : pvg/3 |

Les valeurs sont fondées sur le capital initial, pas sur la vie restante.

Une attaque au quart représente 125 000 000 bruts et normalement 93 750 000 après le traitement ordinaire à 75 %.
L'attaque au tiers représente environ 166 666 666,67 bruts et normalement 125 000 000 après traitement.

La gauche possède un soin ; les trois pouvoirs droits ajoutent des dégâts. Les camps ne sont donc pas symétriques.

Particularité du soin état 22 : il écarte une partie du traitement commun et ne met pas degg0/degd0 à jour comme les autres états. Son interaction avec les dégâts et l'énergie après la séquence doit être vérifiée en exécution. Ne pas documenter « rend exactement 25 % » sans cette réserve.

Les pouvoirs modifient indexa sans remettre explicitement anim1 et anim1vv à zéro. Ils héritent donc de l'indice et éventuellement du sens de lecture précédents.

Indicateurs :

- select/select0.png à select/select15.png : animation visuelle ;
- baboke.wav : disponibilité ;
- une faute babokpbd au lieu de babokepbd apparaît dans une réinitialisation droite ;
- les premier et troisième visuels de pouvoir droit sont associés différemment entre création et affbt, ce qui peut inverser leur représentation sans changer leurs indices d'action.

## 11. Ordinateur et niveaux

Chaque camp peut être contrôlé indépendamment par l'ordinateur.

Pour l'arrêt d'un orbe, colvv calcule la distance à la cible puis appelle computer(distance,niveau).

Première règle : si distance < 2*niveau², l'arrêt est refusé.

Zones de refus :

| Niveau | Refus si distance < |
|---:|---:|
| 1 | 2 |
| 2 | 8 |
| 3 | 18 |
| 4 | 32 |
| 5 | 50 |

Ensuite :

u=distance^0,06
P=u^3-uktens[niveau]

Paramètres ktens :

- niveau 1 : -9 ;
- niveau 2 : -6 ;
- niveau 3 : -9 ;
- niveau 4 : -0,8 ;
- niveau 5 : 2.

Une fraction dérivée de time.time() est multipliée par P. L'arrêt est accepté si la partie entière obtenue vaut int(P/2), int(P/2)+1 ou int(P/2)-1.

Le mécanisme repose donc sur l'horloge plutôt que sur une probabilité indépendante classique.

Les niveaux influencent :

- vitesse/pas des orbes ;
- décision d'arrêt ;
- fréquence potentielle des pouvoirs.

Pouvoirs IA : carupdate les examine pendant indexa=1. computer(10000,niveau) accepte lorsque int(rr(5*niveau))==2, avec énergie>60 et pouvoir disponible/non utilisé.

Les pouvoirs sont examinés dans l'ordre des indices. Une capacité démarrée fait sortir indexa de 1 et empêche les suivantes de démarrer dans le même parcours. Les capacités gauches sont examinées avant les droites.

## 12. Chronomètres

### car2 — saisie des orbes

Valeur de départ : 10.

Chaque seconde, si indexa==1 et qu'au moins un orbe reste mobile :

- car2 diminue ;
- la valeur est affichée ;
- si car2<1, les six orbes sont forcés à l'arrêt par la logique de colvv.

Sinon car2 revient à 10 et son texte est effacé.

### car — temps global actif

Valeur de départ : 100.

Il diminue seulement si indexa==1, stopg==False et stopd==False.

Il ne représente donc pas 100 secondes continues de temps réel.

Si car<0 :

- timeout=True ;
- indexa=0 ;
- car=100.

Aucune comparaison des vies pour déterminer un vainqueur au temps n'a été trouvée.

## 13. Fin de combat et retour menu

mc1 calcule :

compg=pvg-degg
compd=pvd-degd

avant l'avancement de la séquence.

Si compg<1 :

- indexa=11 ;
- anim1=2 ;
- anim1vv=1 ;
- dégâts cumulés remis à zéro.

Si compd<1 :

- indexa=10 ;
- anim1=0 ;
- anim1vv=1 ;
- dégâts cumulés remis à zéro.

Les deux tests sont indépendants et utilisent les compg/compd calculés avant les branches. Si les deux camps tombent simultanément à zéro, la seconde branche prend finalement le dessus et indexa termine à 10.

Pour les états 10 et 11, le retour menu intervient quand anim1==longanim1[indexa]-3 : toutes les dernières images ne sont donc pas garanties d'être jouées.

Au retour indexa=0, affbt réinitialise notamment :

- selected, select et bonus ;
- énergies ;
- indicateurs de jauge pleine ;
- dégâts et références ;
- car.

Les choix humain/ordinateur et niveaux ne sont pas remis à leur défaut dans ce bloc.

La remise à zéro globale est distribuée entre plusieurs méthodes. L'affectation car2=10 dans affbt est locale car car2 n'y est pas déclaré global ; car2 possède néanmoins son mécanisme de réinitialisation dans carupdate.

## 14. Séquences d'images

Les images actives sont adressées par :

préfixe + indice entier + ".jpeg"

| État | Préfixe | Limite déclarée | Événement deg[indexa] | Son |
|---:|---|---:|---:|---|
| 0 | insertcoin/insertcoin_ | 11 | 300 | jtrm0.wav |
| 1 | dinos1/dinos_ | 59 | 180 | jtrm1.wav |
| 2 | chargetr/chargetrwin_ | 128 | 88 | jtrm3.wav |
| 3 | chargest/chargetrwin_ | 128 | 87 | jtrm3.wav |
| 4 | horseg2ko/chargetrwin_ | 105 | 85 | jtrm3.wav |
| 5 | egtrwin/egtrwin_ | 9128 | 800 | jtrm7.wav |
| 6 | egtrwin/egtrwin_ | 152 | 130 | jtrm7.wav |
| 7 | eg2ko/eg2ko_ | 153 | 129 | jtrm7.wav |
| 8 | stwin/stwin_ | 193 | 118 | jtrm8.wav |
| 9 | trwin/trwin_ | 195 | 94 | jtrm9.wav |
| 10 | finishst/finishst_ | 165 | 918 | jtrm10.wav |
| 11 | finishtr/finishtr_ | 104 | 194 | jtrm11.wav |
| 21 | stsf/stsf_ | 242 | 181 | stsf.wav |
| 22 | stls/stls_ | 213 | 182 | stls.wav |
| 23 | stta/stta_ | 238 | 183 | stta.wav |
| 24 | trfs/trfs_ | 232 | 184 | trfs.wav |
| 25 | trph/trph_ | 230 | 185 | trph.wav |
| 26 | trma/trma_ | 239 | 186 | trma.wav |

Modes :

- état 0 : figéf, progression puis fixation à 11 ;
- état 1 : vv, aller-retour ;
- autres états déclarés : 1x avec exceptions décrites plus haut.

Absence inventoriée : horseg2ko/chargetrwin_83.jpeg.
Ne pas combler automatiquement avec une variante de nom sans comparaison visuelle.

dinos1/dinos_0.jpeg a été inspecté en 320×240 ; ne pas généraliser cette dimension à toutes les ressources sans inventaire.

Le Rectangle de scène est dimensionné W×H ; aucune conservation explicite du ratio par bandes n'a été identifiée.

## 15. Synchronisation des séquences

anim_1 est appelé depuis mc1.

L'effet de combat est vérifié lorsque anim1==deg[indexa], avant l'incrément de anim1.

Puis :

- anim1 avance selon anim1vv ;
- les limites/transitions sont traitées ;
- l'image peut être changée ;
- dégâts et énergie sont traités.

En mode aller-retour, le sens s'inverse en haut puis lorsque l'indice redescend sous 1.

Une séquence 1x terminée remet anim1=0, indexa=1 et relance les six orbes.

Le préfixe d'image est mémorisé au début de anim_1. indexa et anim1 peuvent ensuite changer dans le même appel : une image de transition peut donc être construite avec l'ancien préfixe et le nouvel indice.

mc1 est demandé toutes les 0,03 s. Il compare le temps écoulé à 0,06 s :

- si inférieur : anim_1(True), image mise à jour ;
- sinon : anim_1(False), logique avancée sans changement de l'image affichée.

Un callback lent peut donc faire progresser le combat sans montrer l'image correspondante. Il n'existe pas de rattrapage proportionnel du nombre de frames manquées.

## 16. Audio

Deux familles :

- bande-son de séquence ;
- effets courts de boutons, appréciations et pouvoirs.

Quand le nom de bande-son change : arrêt de ma, chargement, lecture, puis choix du mode boucle.

Les états 2 à 7 utilisent une bande-son non bouclée ; les autres branches chargées par le bloc concerné sont bouclées.

Deux variantes partageant le même nom de son n'entraînent pas de rechargement par la condition extérieure, ce qui favorise la continuité lors d'un embranchement.

Le test intérieur combinant plusieurs « différent de » avec OR est logiquement toujours vrai pour les groupes concernés ; il n'ajoute pas de protection effective.

Le volume 0,5 est défini au premier chargement et n'est pas réappliqué explicitement après chaque remplacement de ma.

Les SoundLoader.load ne sont pas systématiquement testés avant .play().

CoreVideo est importé mais aucun lecteur vidéo actif n'est utilisé ; les exemples vidéo sont commentés.

## 17. Héritage air hockey encore exécuté

JTrex conserve un moteur de palet/poignées issu de June air hockey. Il ne doit pas être supprimé au seul motif qu'une partie de ses éléments visuels est masquée.

screen_up est toujours planifié à 0,04 s.

Éléments principaux :

- palet : pavx, pavy, vpavx, vpavy, fpav ;
- poignées : xh/yh et xb/yb ;
- forces fh/fb et accélérations acch/accb ;
- historiques de positions h et b ;
- compteurs/verrous de collision ;
- animations ga, da, pter ;
- scores sch/scb et ancien gagnant ;
- rectangles pavé, vh, vb, jh, jb, gagn, win.

Principes conservés :

- déplacement du palet ;
- ralentissement cubique fp -= fp^3*0,000004 puis zéro sous 1 ;
- force des poignées issue des mouvements tactiles et du temps ;
- plafonnement à 60 ;
- ralentissement après relâchement ;
- rebonds ;
- collisions palet/poignées et poignées/poignées ;
- capture et relâchement temporaire du palet ;
- anciennes conditions de score/remise en jeu.

Le drapeau pbt est forcé à False dans les deux branches du test qui le met à jour ; les anciennes branches de but exigeant pbt=True ne sont donc normalement pas atteintes par ce parcours.

Fonctions/utilitaires associés : calculate_points, tantemps, vectoriser, radc, raddif, collidedif, verifdif, cleanchangecoul.

Points statiques à garder au diagnostic :

- tantemps ne protège pas explicitement le temps nul ;
- vectoriser retourne (0,0) lorsqu'un axe est exactement identique ;
- une branche musicale référence m alors que sa création est commentée ;
- conventions tactiles h/b héritées.

savemc1, vvincrem, restart et certains utilitaires/affichages historiques sont définis mais n'ont pas été identifiés comme planifiés activement. Toujours distinguer « définie », « appelée » et « planifiée ».

## 18. Préparation Android existante

buildozer.spec décrit actuellement :

- title = June T-Rex ;
- package.name = junetrex ;
- package.domain = com.junedady ;
- version = 1.0 ;
- requirements = python3,kivy ;
- orientation = landscape ;
- fullscreen = 1 ;
- android.api = 36 ;
- android.minapi = 21 ;
- android.ndk = 28c ;
- android.ndk_api = 21 ;
- architectures = arm64-v8a et armeabi-v7a ;
- bootstrap = sdl2 ;
- debug = APK ;
- release = AAB.

Ces valeurs sont un constat de configuration, pas une validation de compatibilité.

Le workflow Android :

- télécharge JuneTrex.zip depuis la release ;
- décompresse ;
- cherche le premier main.py ;
- copie le dossier trouvé ;
- y place buildozer.spec ;
- lance un build debug ;
- prévoit APK et log comme artefacts.

L'archive possède plusieurs main.py, dont June air hockey : le choix du « premier main.py » est donc un risque documenté.

La release publique de référence expose JuneTrex.zip, pas un APK installable confirmé.

Le titre runtime mainApp.title vaut « Test » alors que Buildozer indique « June T-Rex ».

Aucune icône Android explicite n'est configurée dans le buildozer.spec étudié.

Pour une future livraison seulement : harmoniser nom/version, ajouter l'icône, produire un APK installable et un AAB distinct si nécessaire, uniquement après autorisation de Fab.

## 19. Principes de préservation pour le futur portage

Le futur portage devra partir de cette référence avant toute simplification.

À conserver tant que Fab n'a pas validé un changement :

- six orbes et trois couleurs par camp ;
- boutons jaunes et confrontations spéciales ;
- score cubique exact et seuil d'égalité ;
- lettres séparées du score de combat ;
- états 2–7 de tapotement ;
- six pouvoirs et leur asymétrie ;
- chronomètres car et car2 ;
- états finaux 10 et 11 ;
- noms/indices historiques ;
- moteur hérité encore exécuté, au moins jusqu'à compréhension complète de ses dépendances ;
- timing et transitions documentés ;
- séries d'images actuelles tant que les vidéos originales n'ont pas été retrouvées et validées.

Les observations techniques doivent être confirmées par exécution avant toute correction. Voir debughistorical.md.


## 20. Compléments de fidélité issus de l'audit Astra

Ces précisions complètent la transcription afin qu'aucun détail fonctionnel significatif du relais Astra ne reste implicite :

- Au tout premier chargement, jtrm0.wav démarre immédiatement, est bouclé et reçoit initialement un volume de 0,5.
- colv[7], colv[8] et colv[9] suivent une notion de temps dans le programme, mais cette information n'est pas utilisée pour normaliser le déplacement des orbes au temps réellement écoulé.
- choixidh et choixidb servent au suivi tactile hérité ; ils ne constituent pas un verrou général limitant tous les boutons à un seul doigt par camp.
- Les remises à zéro de tapg et tapd provoquées par certains appuis hors phase peuvent être atteintes indirectement parce que des zones tactiles restent testées même lorsque leur rectangle est graphiquement masqué.
- La famille horseg2ko contient des variantes de noms et des fichiers de sauvegarde ; l'absence de chargetrwin_83.jpeg ne doit donc pas être « réparée » par simple renommage sans contrôle visuel.
- La durée réelle de car est aussi influencée par les animations et par l'attente qui suit la fin de saisie d'un camp ; car n'est pas une horloge murale continue.
- L'analyse source n'a pas recalculé le hash global de JuneTrex.zip, n'a pas comparé les onze variantes historiques de main.py et n'a pas vérifié visuellement chaque image de chaque séquence.
- Le comportement décrit reste celui lu dans le code de référence. Toute manifestation exacte à l'écran doit être confrontée au jeu exécuté avant de qualifier une asymétrie ou une anomalie de bug.


## 21. Portage Android JT-ANDROID-001 — invariants

La mission JT-ANDROID-001 autorise uniquement les adaptations nécessaires pour rendre June T-Rex installable et testable sur Android. Elle ne modifie pas les règles décrites dans ce brain.

Pendant cette mission, préserver notamment : formule cubique des scores, seuil d'égalité 20 000, lettres séparées du score, asymétries historiques, vie, dégâts, énergie >60, coût 60, pouvoir unique par combat, tapotements, indices d'impact, IA, chronomètres et séquences d'images.

La validation d'un build ou d'un lancement Android ne vaut pas validation du gameplay par Fab.


## 22. JT-ANDROID-001 — adaptation APK appliquée à la copie de compilation

La préparation Android ne modifie pas la source historique dans l'archive. `tools/prepare_android.py` vérifie d'abord la taille et le SHA-256 de `JuneTrex.zip`, sélectionne explicitement la racine `JuneTrex`, puis vérifie le SHA-256 historique de `main.py`.

Sur la copie de compilation seulement, quatre catégories d'adaptation sont autorisées et appliquées :
- `a.png` → `A.png` pour 4 références ;
- `boutbleu0.png` → `boutBleu0.png` pour 4 références ;
- version runtime `1.0.1` et titre `June T-Rex` ;
- deux traces bornées de démarrage `JT-BOOT` et `JT-START`.

Aucune règle de score, dégâts, énergie, pouvoir, tapotement, IA ou chronomètre n'est modifiée.


## 23. JT-ANDROID-001 — premier build réel

Le premier build Android ciblé a atteint la compilation native après validation complète de la préparation des sources. Il a échoué dans la chaîne de compilation native avant production d'un APK.

Aucun élément de gameplay n'a été exécuté ou invalidé par cet échec.


## 24. JT-ANDROID-001 — hypothèse FAB-DEBUG-001 n°1

Pour traiter l'échec natif `LT_SYS_SYMBOL_USCORE`, une seule modification de chaîne est autorisée pour le prochain essai : ajouter le paquet Ubuntu `libltdl-dev` aux dépendances du workflow.

Cette modification ne touche ni le gameplay, ni main.py, ni les médias, ni buildozer.spec.


## 25. JT-ANDROID-001 — résultat de l'essai libltdl-dev

L'ajout de `libltdl-dev` a permis au build de franchir le blocage `LT_SYS_SYMBOL_USCORE`. Cette erreur n'apparaît plus dans le run #8.

Le build a ensuite progressé jusqu'à un nouveau blocage interne de la chaîne Python/pip de python-for-android. Aucun comportement du jeu n'a été exécuté ni modifié.


## 26. JT-ANDROID-001 — hypothèse FAB-DEBUG-001 n°2

Le test suivant conserve toute la chaîne du run #8 et modifie uniquement la création du venv temporaire de python-for-android : ajout de `--clear` à `python -m venv`.

Le but est de tester l'hypothèse Astra d'un mélange de fichiers pip entre passages successifs par architecture. Aucune version de pip ou de Python n'est changée pour cet essai.


## 27. JT-ANDROID-001 — premier APK construit

Le run #9 a produit avec succès le premier APK Android de validation de June T-Rex.

Ce succès valide la chaîne de compilation utilisée pour ce candidat, mais pas encore l'exécution réelle ni le gameplay sur le téléphone de Fab.

APK : `JuneT-Rex-1.0.1-debug.apk`.


## 28. Mission vidéo / icône — intake médias

Fab a fourni cinq nouvelles ressources sur `main`, à importer sans fusion globale :
- `JtrexIcon.png` ;
- `JTrexintro1.mp4` ;
- `JTrexintro2.mp4` ;
- `JTrexintro3.mp4` ;
- `StegVsTrexvaetviensremolace.mp4`.

La mission autorise trois évolutions ciblées : une intro aléatoire unique par lancement, le remplacement de l'icône provisoire, et un premier essai vidéo sur une attente historique clairement identifiée.

Le point fonctionnel candidat pour la vidéo Steg/T-Rex est l'état `indexa=1`, seule séquence historique documentée en mode `vv` aller-retour (`dinos1/dinos_`). Ce rattachement doit être confirmé par inspection du code et du média avant remplacement effectif.


## 29. JT-MEDIA-001 — intégration vidéo candidate 1.0.2

L'intégration autorisée conserve le moteur historique et remplace seulement l'affichage de l'attente `indexa=1` par la vidéo fournie. La logique `anim_1` continue de progresser ; les orbes, scores, timers, dégâts et transitions ne dépendent pas du média.

Au lancement de l'application, une seule intro est choisie uniformément parmi les trois MP4. Les callbacks de gameplay ne sont planifiés qu'après sa fin ou après un repli de sécurité. La musique historique du menu est différée jusqu'à cette transition afin de ne pas se superposer à l'audio de l'intro.

La vidéo d'attente conserve le son historique du jeu : sa propre piste audio est muette. Les images JPEG historiques restent empaquetées et servent de repli si le lecteur vidéo ne fournit pas de frame.


## 30. JT-MEDIA-001 — cible Python vidéo

Le run #11 a confirmé que le candidat vidéo atteint la compilation de ffpyplayer, mais ffpyplayer 4.5.1 échoue contre les API C de Python 3.14.2. Le gameplay JTrex n'est pas en cause.

Le test suivant conserve le même p4a et la même recette FFmpeg 6.1.2, mais fixe le Python cible à 3.11.13, version stable historique de la même lignée p4a et adaptée au code C généré de ffpyplayer 4.5.1.


## 2026-09-28 — FAB-DEBUG-001 / JT-MEDIA-001

- Décision Astra appliquée sur la branche `port/android-first-apk` : cible Android et host Python figés ensemble sur 3.12.14.
- Requirement attendu : `python3==3.12.14,hostpython3==3.12.14,kivy,ffpyplayer`.
- ffpyplayer 4.5.1, FFmpeg 6.1.2 et le commit p4a existant restent inchangés.
- Le préparateur Android contient encore une garde héritée imposant Python 3.11.13 ; conformément au protocole mono-correction, elle n'est pas modifiée dans ce run. Le résultat réel du workflow doit déterminer le prochain ordre de mission.


### Résultat réel du run #13 — 2026-09-28

- Commit construit : `0f73b3d31d4dc242daecb102f4c18579c8413627`.
- GitHub Actions : run #13, ID `36355762409`, job `108723048564`.
- Échec à l'étape `Verify and prepare JuneTrex sources`, avant installation Buildozer/p4a et avant compilation ffpyplayer.
- Erreur discriminante : `RuntimeError: Python cible doit rester figé sur 3.11.13 pour ffpyplayer.`
- Le pin 3.12.14 présent dans `buildozer.spec` n'a donc pas encore été transmis à p4a ; les versions effectives python3/hostpython3 3.12.14 et le Cython isolé ne peuvent pas être prouvés sur ce run.
- Artefact disponible : `JuneTrex-Android-Diagnostics` (ID `10943932232`).
- Aucun APK 1.0.2 produit. Lecture vidéo et gameplay non testés.
- Conformément à FAB-DEBUG-001, aucune seconde correction fonctionnelle n'est ajoutée à ce run.


## 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — alignement préparation Python 3.12.14

- Suite autorisée après le run #13 : la garde de préparation et son reporting sont alignés de Python 3.11.13 vers Python 3.12.14.
- La garde reste active : elle exige toujours explicitement la présence du pin attendu dans `requirements` et lève une exception en cas d'écart.
- `buildozer.spec` reste inchangé : `python3==3.12.14,hostpython3==3.12.14,kivy,ffpyplayer`.
- Cette modification ne prouve pas encore la version Python effectivement compilée ; la preuve doit venir des journaux p4a du prochain run.
- Aucun changement de ffpyplayer, FFmpeg, p4a, Cython, médias, runtime ou gameplay.


### Résultat réel du run #14 — 2026-09-28

- Commit construit : `393e1612fa98d04cd5d69c33eae140caf693c8d2`.
- GitHub Actions : run #14, ID `36356865568`, job `108726222221`.
- `Verify and prepare JuneTrex sources` : SUCCÈS ; la garde 3.12.14 est franchie.
- p4a demande explicitement `python3 3.12.14` et `hostpython3 3.12.14`, puis télécharge pour les deux le tag CPython `v3.12.14.tar.gz`.
- Le workflow conserve toutefois une variable d'environnement héritée `VERSION_hostpython3=3.11.13` ; elle est consignée comme incohérence de diagnostic, sans correction dans ce run. Les traces p4a de recette/source indiquent bien 3.12.14 pour hostpython3.
- p4a prévoit les architectures `armeabi-v7a, arm64-v8a` et commence par construire Python cible pour `armeabi-v7a`.
- Premier nouveau blocage : CPython 3.12.14 échoue dans `Modules/grpmodule.c` sur Android/armeabi-v7a : `setgrent`, `getgrent` et `endgrent` sont non déclarées ; `getgrent` entraîne aussi une conversion int→pointeur invalide.
- `python3` pour `arm64-v8a` n'est pas atteint ; la compilation de `ffpyplayer` n'est pas atteinte.
- Les erreurs historiques `_PyLong_AsByteArray` et `_PyGen_SetStopIterationValue` n'apparaissent pas dans ce run, mais leur disparition dans ffpyplayer n'est pas prouvée puisque ffpyplayer n'a pas été compilé.
- Aucun APK 1.0.2 produit. Artefact diagnostic : `JuneTrex-Android-Diagnostics`, ID `10944283554`.
- Aucun correctif supplémentaire appliqué conformément à FAB-DEBUG-001.


## 2026-09-28 — JT-MEDIA-001 / FAB-DEBUG-001 — grp Android API 21

- Cause retenue après le run #14 : CPython 3.12.14 tente de construire le module standard `grp` pour la cible Android API native 21 alors que `grp_getgrall_impl` utilise `setgrent`, `getgrent` et `endgrent`, indisponibles sur cette cible.
- Correction Astra autorisée : patcher uniquement la recette `python3` cible de p4a afin de définir `py_cv_module_grp=n/a` lorsque `self.version == '3.12.14'` et `ndk_api < 26`.
- Le hostpython3 Linux n'est pas concerné par cette exclusion.
- Le patch est conservé dans `tools/patches/p4a-python312-grp-api21.patch` et appliqué reproductiblement par le workflow après `p4a-venv-clear.patch`.
- `buildozer.spec` reste inchangé avec python3/hostpython3 3.12.14. L'export historique `VERSION_hostpython3=3.11.13` reste volontairement inchangé pour isoler cet essai.
- Hypothèse encore à tester : le Python cible doit franchir `grp`, puis seulement ensuite ffpyplayer pourra être évalué.


### Résultat réel du run #15 — 2026-09-28

- Commit construit : `b7323fdb940b9be6e47e31f1ceed8d1094adc31c`.
- GitHub Actions : run #15, ID `36360940843`, job `108737876412`.
- Le patch `tools/patches/p4a-python312-grp-api21.patch` est appliqué avec succès par le workflow.
- La recette python3 cible journalise : `JT-MEDIA-001: target grp unavailable below Android API 26`.
- Pour le hostpython Linux, le configure conserve `checking for stdlib extension module grp... yes` et `Modules/grpmodule.c` est compilé : comportement attendu, le patch ne vise pas hostpython.
- Pour le Python Android cible armeabi-v7a, le configure journalise `checking for stdlib extension module grp... n/a`.
- Aucun `Modules/grpmodule.c` cible Android n'est compilé ; le blocage `setgrent/getgrent/endgrent` du run #14 est franchi.
- Le build progresse ensuite jusqu'à `Building ffmpeg for armeabi-v7a` avec FFmpeg 6.1.2.
- Première nouvelle erreur discriminante : `libavcodec/vulkan_av1.c:183:43: error: incompatible pointer to integer conversion initializing 'VkVideoSessionParametersKHR' ... with 'void *'`, sur `.videoSessionParametersTemplate = NULL`.
- La même phase signale ensuite dans `libavcodec/vulkan_decode.c` des affectations `NULL` incompatibles vers `VkImageView`.
- La commande configure FFmpeg observée contient notamment `--enable-hwaccels`.
- `python3` pour arm64-v8a n'est pas atteint ; FFmpeg arm64-v8a n'est pas atteint.
- ffpyplayer 4.5.1 est téléchargé/préparé pour armeabi-v7a, mais sa phase `Building ffpyplayer` n'est pas atteinte.
- Les erreurs `_PyLong_AsByteArray` et `_PyGen_SetStopIterationValue` sont absentes du log, sans valeur probante pour ffpyplayer puisqu'il n'a pas été compilé.
- Aucun APK 1.0.2 produit. Artefact diagnostic : `JuneTrex-Android-Diagnostics`, ID `10945787341`.
- Aucun second correctif appliqué dans cette tentative.


## 2026-09-28 — JT-MEDIA-001 — exclusion Vulkan FFmpeg 6.1.2

- Suite autorisée après le run #15 : conserver FFmpeg 6.1.2 et ajouter uniquement `--disable-vulkan` dans la recette `tools/p4a-ffmpeg-6.1.2.py`.
- `--enable-hwaccels` est conservé afin de ne pas désactiver les autres accélérations matérielles.
- Objectif : empêcher la construction de la famille Vulkan qui a échoué sur armeabi-v7a avec les handles Vulkan initialisés par `NULL`.
- Les décodeurs logiciels AAC/H.264, le démuxeur MOV/MP4, Python 3.12.14, ffpyplayer 4.5.1, p4a figé, NDK/API, architectures, médias et gameplay restent inchangés.
- Hypothèse à vérifier au prochain run : `CONFIG_VULKAN=0` et poursuite de FFmpeg sans compiler les objets Vulkan responsables.


### Run #16 — résultat réel (2026-09-28)
- Commit construit : `e88bd93ec0a7d9b34b2d4f64eb10b3627d230149`; run #16 ID `36364807323`.
- FFmpeg 6.1.2 : `--disable-vulkan` transmis sur arm64-v8a et armeabi-v7a ; AAC/H.264 et démuxer MOV conservés.
- FFmpeg et ffpyplayer 4.5.1 atteignent le postbuild sur les deux architectures.
- Absence des erreurs `_PyLong_AsByteArray` et `_PyGen_SetStopIterationValue`.
- APK produit : `JuneT-Rex-1.0.2-debug.apk`, SHA-256 `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a`.
- Compilation validée ; lecture vidéo, fluidité et gameplay restent à valider par Fab sur téléphone.


### Premier crash téléphone — diagnostic ouvert — 2026-09-28

Constat Fab : l'application affiche le logo Kivy puis se ferme. La compilation du run #16 est réussie, mais le démarrage applicatif, l'intro vidéo et le gameplay ne sont pas validés.

APK identifié :
- fichier transmis : `JuneT-Rex-1.0.2-debug.apk` ;
- build GitHub Actions : run #16, ID `36364807323` ;
- commit construit : `e88bd93ec0a7d9b34b2d4f64eb10b3627d230149` ;
- version : `1.0.2` ;
- versionCode / numeric-version : `102` ;
- package : `com.junedady.junetrex` ;
- SHA-256 vérifié sur l'artefact réellement téléchargé : `8743980ff87fc13c9a534de7d5de07c561e2c2b9312852893fb5c943ddb23c4a` ;
- ABIs contenues dans l'APK : `arm64-v8a` et `armeabi-v7a`.

Limite actuelle : aucun accès ADB au téléphone de Fab dans cette session et aucun environnement Android compatible disponible ici pour reproduire le lancement. Le crash n'est donc pas reproduit et sa cause reste inconnue.

Marqueurs disponibles dans les sources préparées : `[JT-BOOT]`, `[JT-START]`, `[JT-INTRO] chosen=`, `[JT-INTRO] begin=`, `[JT-INTRO] gameplay enabled`. Sans logcat du lancement réel, aucun de ces marqueurs ne peut être déclaré comme dernier marqueur atteint.

Diagnostic à poursuivre uniquement avec un journal de lancement complet (Python, Java et natif). Ne pas attribuer le crash à la vidéo, ffpyplayer, FFmpeg, Kivy ou une ressource avant la première erreur fatale observée.


### Crash téléphone 1.0.2 — preuve bugreport reçue — 2026-09-28

Rapport téléphone reçu : `bugreport-a57xnaeea-BP4A.251205.006-2026-09-28-10-54-03.zip`.

Identité de l'appareil et de l'installation vérifiée dans le bugreport :
- modèle : `SM-A576B` ;
- Android : 16, build `BP4A.251205.006` ;
- ABI réellement utilisée : `arm64-v8a` ;
- package installé : `com.junedady.junetrex` ;
- version : `1.0.2` ; versionCode : `102` ; minSdk 21 ; targetSdk 36 ;
- application installée en mode debuggable ; APK signing version 2.

Lancement pertinent observé à 10:53:39 : process `16365`. PythonActivity atteint `onCreate`, `onStart`, `onResume`, crée sa SurfaceView puis lance `SDL_main` et `Initializing Python for Android`.

Dernières traces Python avant terminaison :
```text
10:53:40.440 python: Initializing Python for Android
10:53:40.440 python: Setting additional env vars from p4a_env_vars.txt
10:53:40.440 python: Changing directory to '/data/user/0/com.junedady.junetrex/files/app'
10:53:40.442 python: Preparing to initialize python
10:53:40.442 python: _python_bundle dir exists
10:53:40.442 python: set wchar paths...
10:53:40.506 python: Python initialization failed:
10:53:40.506 python: failed to get the Python codec of the filesystem encoding
10:53:40.506 python: Python for android ended.
```

Le processus meurt ensuite à 10:53:40.604. Aucun marqueur `[JT-BOOT]`, `[JT-START]` ou `[JT-INTRO]` n'apparaît dans le bugreport : le code applicatif `main.py` n'est donc pas atteint. Le crash ne peut pas être attribué aux vidéos, à l'intro ou au gameplay à ce stade.

La même erreur `failed to get the Python codec of the filesystem encoding` est répétée sur plusieurs autres tentatives de lancement dans le rapport, ce qui confirme un échec reproductible de l'initialisation CPython sur l'appareil.

Inspection statique de l'APK du run #16 : `libpybundle.so` contient `_python_bundle/stdlib.zip`, et cette archive contient bien le paquet `encodings` (122 entrées) ainsi que `codecs.pyc`. Le diagnostic ne doit donc pas être simplifié en « encodings absent » sans analyse supplémentaire ; il s'agit d'un échec de chargement/initialisation du codec de filesystem pendant le démarrage CPython.

Aucune correction n'est appliquée dans cette étape de diagnostic.


## 2026-09-28 — FAB-DEBUG-001 — diagnostic bootstrap Python

- Relecture du bugreport existant : aucune exception Python détaillée n'est présente autour du PID 16365 ; aucun traceback, ModuleNotFoundError, ImportError, ZipImportError ni bad magic number n'est journalisé.
- Les échecs de chargement libpython3.14.so et libpython3.13.so sont des essais de détection ; libpython3.12.so est ensuite chargée avec succès avant SDL_main.
- Essai diagnostique autorisé par Astra : patcher uniquement le start.c du bootstrap p4a figé pour rendre visible l'exception sous-jacente à Py_InitializeFromConfig.
- Le patch journalise Py_GetVersion, les module_search_paths réellement fournis, l'existence/lisibilité/taille de stdlib.zip, status.func/status.err_msg, puis capture immédiatement PyErr_GetRaisedException sous Python 3.12 et journalise type/message/cause/contexte avec parcours borné.
- En cas d'échec d'initialisation, le bootstrap retourne un statut d'échec sans continuer vers les appels applicatifs Python.
- Ce patch est strictement diagnostique et ne signifie pas que le crash est corrigé.


### Run #17 — application du patch diagnostique non testée
Le run #17 (ID 36410139322) s'est arrêté avant compilation : `git apply --check` a signalé `corrupt patch ...:113`. Aucun diagnostic Python n'a donc été exécuté. Correction appliquée ensuite : uniquement les compteurs/en-têtes des hunks du même patch, sans changer son contenu fonctionnel.


### Run #18 — APK diagnostique produit

- Commit construit : `7fa5e4bd32ae02dbe88b8eb74e04e73b0a834986`.
- GitHub Actions : run #18, ID `36410518782`, conclusion `success`.
- Le patch bootstrap diagnostique est visible dans `p4a-patch.txt` avec les marqueurs `P4A_DIAG`.
- Le `start.c` du bootstrap est effectivement compilé pour `arm64-v8a` et `armeabi-v7a`.
- APK diagnostique produit : `JuneT-Rex-1.0.2-debug.apk`.
- SHA-256 vérifié : `fbc4a1d0f72cf677591e4a4ffb366db9237377c5f5c3574d6f7ca025249d8e64`.
- Artefact APK : ID `10965620909`. Artefact diagnostics : ID `10965760827`.
- Ce succès valide uniquement la construction du diagnostic ; il ne valide pas le démarrage Python ni la correction du crash.


### Run #18 — bugreport téléphone : cause sous-jacente exposée

Nouveau rapport Fab : `bugreport-a57xnaeea-BP4A.251205.006-2026-09-28-14-23-12.zip`.

Le diagnostic natif P4A_DIAG fonctionne et révèle de façon reproductible :
- Python natif : 3.12.14.
- `stdlib.zip` existe, est lisible, taille 3 850 556 octets.
- `module_search_paths` contient bien `_python_bundle/stdlib.zip` puis `_python_bundle/modules`.
- `status.func=init_fs_encoding`.
- `status.err_msg=failed to get the Python codec of the filesystem encoding`.
- exception levée : `ZipImportError: can't decompress data; zlib not available`.
- contexte : `ImportError: dlopen failed: cannot locate symbol "PyExc_MemoryError" referenced by ".../_python_bundle/modules/zlib.cpython-312.so"`.

Inspection ELF de l'APK diagnostique arm64-v8a :
- `zlib.cpython-312.so` est présent et déclare `PyExc_MemoryError` comme symbole GLOBAL UND.
- ses dépendances NEEDED sont `libz.so`, `libdl.so`, `libc.so` ; `libpython3.12.so` n'est pas NEEDED.
- `libpython3.12.so` exporte bien `PyExc_MemoryError` comme symbole GLOBAL.
- `libmain.so` dépend bien de `libpython3.12.so`.

La cause immédiate du bootstrap est donc établie : le module d'extension zlib ne peut pas résoudre un symbole Python au chargement, ce qui rend zlib indisponible ; zipimport ne peut alors pas décompresser `stdlib.zip`, ce qui fait échouer `init_fs_encoding`.

Aucun correctif n'est appliqué dans cette étape.


## 2026-09-28 — FAB-DEBUG-001 — visibilité globale de libpython

Contrôle préalable effectué sur l'APK réellement testé du run #18 :
- arm64-v8a : `DT_FLAGS_1 = NOW`, sans `GLOBAL` ; `PyExc_MemoryError` exporté GLOBAL.
- armeabi-v7a : `DT_FLAGS_1 = NOW`, sans `GLOBAL` ; `PyExc_MemoryError` exporté GLOBAL.
- aucun `DT_SONAME` explicite n'est présent dans `libpython3.12.so` sur ces deux ABI ; ce constat préexiste au nouvel essai et n'est pas corrigé dans cette mission.

Hypothèse Astra autorisée : ajouter uniquement `-Wl,-z,global` à la liaison de `libpython3.12.so` pour Python cible 3.12.14, afin d'obtenir `DF_1_GLOBAL` / `FLAGS_1: GLOBAL` sans ajouter de DT_NEEDED à zlib.

Le patch local est `tools/patches/p4a-python312-libpython-global.patch`. Le contexte du premier hunk a été ajusté mécaniquement à la source p4a figée, qui n'a pas la ligne vide présente dans le texte Astra ; les lignes fonctionnelles sont inchangées.


### Run #19 — DF_1_GLOBAL matérialisé dans l'APK

- Commit construit : `e0c374fe7f436ea12ef07a9676916033cd5f6fcf`.
- GitHub Actions : run #19, ID `36437050585`, conclusion `success`.
- APK produit : `JuneT-Rex-1.0.2-debug.apk`.
- SHA-256 : `945f795bce1b925ac981df48bbd3781d73d5816927ef4356ce00e2875068a241`.
- Artefact APK : ID `10977123002`; diagnostics : ID `10976803216`.
- Le log de build contient `-Wl,-z,global` dans la liaison de libpython3.12.so pour arm64-v8a et armeabi-v7a.
- Inspection ELF de l'APK final :
  - arm64-v8a : `DT_FLAGS_1 = NOW GLOBAL`;
  - armeabi-v7a : `DT_FLAGS_1 = NOW GLOBAL`;
  - `PyExc_MemoryError` reste exporté GLOBAL sur les deux ABI.
- Aucun `DT_SONAME` explicite n'est présent dans le libpython final, comme au run #18 ; ce point préexistant n'est pas modifié dans cette hypothèse.
- Le build valide la matérialisation de DF_1_GLOBAL uniquement. Le bootstrap Python et [JT-BOOT] restent à valider sur le téléphone.
