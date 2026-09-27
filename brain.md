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
