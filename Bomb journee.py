# Créé par Sam78, le 23/05/2022 en Python 3.7
import pygame
from random import randint
import time
from timeit import*
pygame.init()
from tkinter import*
from PIL import Image
from PIL import ImageTk
from random import*

def menu():    #creation du menu principale
    menu=Tk()   # tkinter permet d'initialiser une fenetre
    menu.title("Bomb Journee")
    menu.minsize(480,320)            #dans cette partie la nous nous occupons de la taille, couleurs et emplacements du titre
    menu.resizable(width=False,height=False)
    menu.configure(bg="white")
    bombjournee=Image.open("menu.jpg")
    photo=ImageTk.PhotoImage(bombjournee)
    bombjournee2=Label(menu,image=photo,bg="white")
    bombjournee2.pack()
    espace=Frame(menu,height=75,borderwidth=1,bg="white")
    espace.pack()
    def quitter():        #creation de la fonction quitter lorsque on appuie sur la croix rouge (lance le jeu directement après)
        menu.destroy()
    lancer=Button(menu,text="Lancer le jeu",command=quitter,bg="dodgerblue",fg="white",width=50,height=1)
    lancer.pack()       # .pack() permet de placer dans l'ordre indiqué les Frame(boutton ou autres créés au dessus)
    espace.pack()

    def menu2():    #il s'agit de la fenetre qui souvre lorsqu'on clique sur controle (indique les commandes pour jouer au jeu)
        menu.destroy()
        menu2=Tk()
        menu2.title("Contrôles")
        menu2.minsize(300,305)
        menu2.resizable(width=False,height=False)
        menu2.configure(bg="white")
        controle=Image.open("menu2.jpg")
        photo2=ImageTk.PhotoImage(controle)
        controle2=Label(menu2,image=photo2,bg="white")                                                  #même procédé que la première fenetre du menu d'accueil
        controle2.pack()
        menu2.mainloop()
    cmd=Button(menu,text="Contrôles",command=menu2,bg="dodgerblue",fg="white",width=50,height=1)
    espace2=Frame(menu,height=10,borderwidth=1,bg="white")
    espace2.pack()
    cmd.pack()
    menu.mainloop() #affiche la fentre principale (menu)
menu() # appel la fonction menu juste créée au dessus


# Initialisation des variables:


fenetre = pygame.display.set_mode( (580,630) ) # Définition de la taille du terrain de jeu
mur1=pygame.Rect(0, 0, 580, 30)             # initailisation des 4 murs présent autour du terrain (abscisse, ordonnée, longueur, largeur)
mur2=pygame.Rect(0, 550, 580, 40)
mur3=pygame.Rect(0, 0, 30, 580)
mur4=pygame.Rect(550, 0, 30, 580)

#creation des obstacles avec leur coordonées
coord_obstacle=[(70,70),(70,150),(70,230),(70,310),(70,390),(70,470),
(150,70),(150,150),(150,230),(150,310),(150,390),(150,470),
(230,70),(230,150),(230,230),(230,310),(230,390),(230,470),
(310,70),(310,150),(310,230),(310,310),(310,390),(310,470),
(390,70),(390,150),(390,230),(390,310),(390,390),(390,470),
(470,70),(470,150),(470,230),(470,310),(470,390),(470,470)]

hitbox_obstacle=[] #liste qui va contenir les hitbox de tous les obstacles fixes

for i in range (0,len(coord_obstacle)):  # associe à chaque obstacle une hitbox carré de taille 40 sur 40 pixels (en dessinant un rectancgle autour)
     	obstacle=pygame.Rect(coord_obstacle[i], (40,40))
     	hitbox_obstacle.append(obstacle)

pygame.display.set_caption("Terrorist Tycoon") # Définit le titre de la fenêtre du jeu

#creation du joueur 1 ainsi que sa position initiale avec sa hitbox
oussama_photo=pygame.image.load("BenLaden.png")
oussama=pygame.transform.scale(oussama_photo, (30,30))  #modifie le format de la photo ici 30pixels sur 30 pixel
oussama_position=(30,30)
oussama_hitbox=pygame.Rect((oussama_position), (30,30))


#creation du joueur 2 ainsi que sa position initiale avec sa hitbox
bush_photo=pygame.image.load("GeorgeWBush.png")
bush=pygame.transform.scale(bush_photo, (30,30))
bush_position=(520,520)
bush_hitbox=pygame.Rect((bush_position), (30,30))


#creation de 3 obstacles ennemies qui se deplacent d'une maniere autonome
fantome_photo=pygame.image.load("Fantome.png")
fantome=pygame.transform.scale(fantome_photo, (30,30))
fantome_position=(35,515)
fantome_hitbox=pygame.Rect((fantome_position), (30,30))

fantome2_photo=pygame.image.load("Fantome.png")
fantome2=pygame.transform.scale(fantome2_photo, (30,30))
fantome2_position=(115,115)
fantome2_hitbox=pygame.Rect((fantome2_position), (30,30))

fantome3_photo=pygame.image.load("Fantome.png")
fantome3=pygame.transform.scale(fantome3_photo, (30,30))
fantome3_position=(355,355)
fantome3_hitbox=pygame.Rect((fantome3_position), (30,30))


#le positionnement de la bombe au depart est a l'exterieur du terrain
bombe_position=(-40, -40)
bombe_photo=pygame.image.load("bomb.png")
bombe=pygame.transform.scale(bombe_photo, (40,40)) # on redefinie le format de l'image 40 pix sur 40 pix
bombe_hitbox=pygame.Rect((bombe_position), (40,40))#hitbox associé a la bombe pour le joueur 1

# on fera de meme pour le joueur 2
bombe2_position=(-40, -40)
bombe2_photo=pygame.image.load("bomb.png")
bombe2=pygame.transform.scale((bombe2_photo), (40,40))
bombe2_hitbox=pygame.Rect((bombe2_position), (40,40)) #hitbox associé a la bombe pour le joueur 2


touchesPressees = pygame.key.get_pressed()

#différent temps qui bva permettre l'explosion des bombes
bombepose=0
debut=time.time()
debut2=time.time()


ancien=(-1000,0) # variables qui nous seront utile plus tard pour la pose des bombes des 2 joueurs
ancien2=(-1000,0)

cri_oussama=pygame.mixer.Sound("7000.wav") # initalisation des variable utile pour lancer un son quand le joueur en question se fait toucher
cri_bush=pygame.mixer.Sound("13405.wav")

# initialisation des variables pour le systeme de points:
points1=0             # nombre de points au départ
points2=0
arial24 = pygame.font.SysFont("arial",24)     # taille et type de police qui sera utilser dans tous ce qui est affichage de texte durant la phase de jeu


winJ1= arial24.render("Oussama (J1) a gagné",True,pygame.Color(0,0,255)) # variable qui va permettre d'afficher le texte en question selon le joueur lorsqu'il gagne
winJ2=arial24.render("Bush (J2) a gagné",True, pygame.Color(255,0,0))



def dessiner(): # Procédure d'affichage du terrain
    global fenetre, continuer, obstacle, bush_hitbox, dernièretouche, touchePressees, start, debut2,winJ1,winJ2
    fenetre.fill( (96, 96, 96) )         # couleur du background de la fenetre (ici gris)

    # dessin des mur avec leur couleur:
    pygame.draw.rect(fenetre, (253, 241, 184), mur1)
    pygame.draw.rect(fenetre, (253, 241, 184), mur2)
    pygame.draw.rect(fenetre, (253, 241, 184), mur3)
    pygame.draw.rect(fenetre, (253, 241, 184), mur4)

    #systeme de point qui va s'afficher en fonction de la police défini avant
    score_J1 = arial24.render("SCORE J1 : "+str(points1),True,pygame.Color(0,0,200))
    score_J2 = arial24.render("SCORE J2 : "+str(points2),True,pygame.Color(230,0,0))
    fenetre.blit(score_J1,(10,600)) #.blit permet de disposer ici la variable score_J1 (qui est du texte) sur la fenetre de jeu selon les cordonnées indiqué (10 en abscisse en 600 en ordonnée)
    fenetre.blit(score_J2,(400,600))

    for i in range (0,len(coord_obstacle)): # dessine tous les obstacles en bleu (défini au dessus par la liste d'obstacle)
         obstacle=pygame.Rect(coord_obstacle[i], (40,40))
         pygame.draw.rect(fenetre, (115, 194, 251),obstacle)


    if points1==5:
        fenetre.blit(winJ1,(170,275))  # affiche le message de victoire selon les coordonnées indiquée au boute de 5 points


    if points2==5:
        fenetre.blit(winJ2,(200,275))

    pygame.display.flip()      # cette commande permet de mettre à jour l'affichage de la fenetre pygame du jeu (rafraichissement)


def personnage(): # Procédure d'affichage des personnage et fantomes sur la fenetre de jeu grace à la commande .blit
    global fenetre, oussama, bombe, bombe2, start
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre --<> le jeu s'arrete
            continuer = 0
    fenetre.blit(oussama, oussama_position)
    fenetre.blit(bush,bush_position)
    fenetre.blit(fantome,fantome_position)
    fenetre.blit(fantome2,fantome2_position)
    fenetre.blit(fantome3,fantome3_position)
    fenetre.blit(bombe, (bombe_position[0],bombe_position[1])) # pour le moment l'affichage des bombes de chaque joueur se fait en dehors de la fentre (coordonnées: -40, -40) voir plus haut pour l'initialisation de leur variable et leurs hitbox
    fenetre.blit(bombe2, (bombe2_position[0],bombe2_position[1]))
    pygame.display.flip()
    pygame.display.flip() # reutilisation de cette même commande à la suite afin de doubler le taux de rafraichissment et faire disparaitre le flicker des personnages


def gererClavierEtSouris():
    global continuer, oussama_position, bombe_position,bombe2_position, temps,  bush_position, bush_hitbox, oussama_hitbox, coord_obstacle, obstacle, dernièretouche, touchesPressees, afficher, ancien, coord_obstacle, debut2, ancien2,afficher2
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0


#L'association des touches du clavier en fonctions des deplacements des joueurs
    touchesPressees = pygame.key.get_pressed()

    # Touche uniquement pour le joueur 1:
    if touchesPressees[pygame.K_SPACE] == True:  # touche qui permet au joueur 1 de poser ses bombes
        global ancien, debut
        afficher=True
        bombe_position=oussama_position
        bombe_position=(bombe_position[0]-(bombe_position[0]%40-30),bombe_position[1]-(bombe_position[1]%40-30)) # permet de centrer les bombes dans chaque case du terrain comme dans un quadrillage (l'espace entre 2 obstacle est de 40 pixels d'ou le %40 pour centrer)


        for rect in range(len(coord_obstacle)):
           if bombe_hitbox.colliderect(hitbox_obstacle[rect]) or bombe_position[0]==550 : # permet aux bombes de ne pas être dans les obstacles en detectant les collisions entre les hitbox des bombes et des obstacles fixes ou losqu'on essaye de poser un bombes sur le bord du terrain (tout à droite)
                bombe_position=(bombe_position[0]-40,bombe_position[1]) # on retire 40 pixel pour qu'elle soit poser sur le terrain et pas en dehors
           if bombe_position[1]==550: # même cas lorsqu'on est tout en bas du terrain pour ne pas poser les bombes en dehors
                bombe_position=(bombe_position[0],bombe_position[1]-40)

        ancien=(bombe_position)
        temps2=time.time()-debut2
        if temps2>=3 or temps2<0: # regle le temps pour que l'explosion se fasse au bout de 3 seconde
            debut2=time.time()   # permet de redémarrer le compteur de l'explosion de la bombe sinon la 2eme fois qu'on pose une bombe l'explosion est instantanée et pas au bout de 3 seconde d'apparition


    if touchesPressees[pygame.K_RIGHT]==True and oussama_position[0]<520 : # déplcement vers la droite
        test_oussama_position=pygame.Rect((oussama_position[0] + 5 , oussama_position[1]),(30,30))  # cette ligne test la position futur du joueur c'est a dire on regarde si la prochaine position du joueur vers la droite
        if test_oussama_position.collidelist(hitbox_obstacle) != -1 : # s'il y a collision avec la futur position et un obstacle
            oussama_position=(oussama_position[0]  , oussama_position[1]) # le perso bouge pas
        else:
	        oussama_position=(oussama_position[0] + 5 , oussama_position[1]) # sinon il bouge de 5 pixel et sa hitbox le suit
	        oussama_hitbox=pygame.Rect((oussama_position), (30,30))


    if touchesPressees[pygame.K_LEFT] == True and oussama_position[0]>30: # deplacement vers la gauche
        test_oussama_position=pygame.Rect((oussama_position[0] - 5 , oussama_position[1]),(30,30)) # même procédé que la doite
        if test_oussama_position.collidelist(hitbox_obstacle)!=-1:
            oussama_position=(oussama_position[0]  , oussama_position[1])
        else:
            oussama_position=(oussama_position[0] - 5 , oussama_position[1])
            oussama_hitbox=pygame.Rect((oussama_position),(30,30))


    if touchesPressees[pygame.K_UP]== True and oussama_position[1]>30: #déplacement vers le haut
        test_oussama_position=pygame.Rect((oussama_position[0], oussama_position[1] - 5),(30,30)) # même procédé que la doite
        if test_oussama_position.collidelist(hitbox_obstacle)!=-1:
            oussama_position=(oussama_position[0] , oussama_position[1])
       	else:
            oussama_position=(oussama_position[0] , oussama_position[1] - 5)
       	    oussama_hitbox=pygame.Rect((oussama_position), (30,30))


    if touchesPressees[pygame.K_DOWN]== True and oussama_position[1]<520: #déplacement vers le bas
   	    test_oussama_position=pygame.Rect((oussama_position[0], oussama_position[1] + 5),(30,30)) # même procédé que la doite
   	    if test_oussama_position.collidelist(hitbox_obstacle)!=-1 :
             oussama_position=(oussama_position[0], oussama_position[1])
   	    else:
       	     oussama_position=(oussama_position[0] , oussama_position[1] + 5)
             oussama_hitbox=pygame.Rect((oussama_position), (30,30))



    # Touche de déplacement uniquement pour le joueur 2: (exactement même procédé que le joueur 1 sauf que les touches utilisé sont a,s,d,w car python ne comprend que le clavier QWERTY)
    if touchesPressees[pygame.K_a]==True and bush_position[0]>30 : # déplacement vers la gauche
        test_bush_position=pygame.Rect((bush_position[0] - 5 , bush_position[1]),(30,30))
        if test_bush_position.collidelist(hitbox_obstacle) != -1 :
                	bush_position=(bush_position[0] , bush_position[1])
        else:
            bush_position=(bush_position[0] - 5 , bush_position[1])
            bush_hitbox=pygame.Rect((bush_position), (30,30))

    if touchesPressees[pygame.K_s]==True and bush_position[1]<520 : #déplacement vers le bas
    	test_bush_position=pygame.Rect((bush_position[0] , bush_position[1]+5),(30,30))
    	if test_bush_position.collidelist(hitbox_obstacle) != -1:
            	bush_position=(bush_position[0] , bush_position[1])
    	else:
            	bush_position=(bush_position[0] , bush_position[1]+5)
    	bush_hitbox=pygame.Rect((bush_position), (30,30))

    if touchesPressees[pygame.K_d] == True and bush_position[0]<520 : #déplacement vers la droite
    	test_bush_position=pygame.Rect((bush_position[0] + 5 , bush_position[1]),(30,30))
    	if test_bush_position.collidelist(hitbox_obstacle) != -1 :
            	bush_position=(bush_position[0], bush_position[1])
    	else:
        	bush_position=(bush_position[0] + 5 , bush_position[1])
        	bush_hitbox=pygame.Rect((bush_position), (30,30))


    if touchesPressees[pygame.K_w]== True and bush_position[1]>30: #déplacement vers le haut
    	test_bush_position=pygame.Rect((bush_position[0] , bush_position[1]-5),(30,30))
    	if test_bush_position.collidelist(hitbox_obstacle) != -1 :
            	bush_position=(bush_position[0] , bush_position[1])
    	else:
            	bush_position=(bush_position[0] , bush_position[1]-5)
    	bush_hitbox=pygame.Rect((bush_position), (30,30))

    # touche pour la pose de bombe du joueur 2 (exactement même procédé que pour le joueur 1)
    if touchesPressees[pygame.K_x]== True :
            afficher2=True
            bombe2_position=(bush_position)
            bombe2_hitbox=pygame.Rect((bombe2_position), (40,40))
            bombe2_position=(bombe2_position[0]-(bombe2_position[0]%40-30),bombe2_position[1]-(bombe2_position[1]%40-30))

            for rect in range(len(coord_obstacle)):
                if bombe2_hitbox.colliderect(hitbox_obstacle[rect]) or bombe2_position[0]==550 :
                    bombe2_position=(bombe2_position[0]-40,bombe2_position[1])
                if bombe2_position[1]==550:
                    bombe2_position=(bombe2_position[0],bombe2_position[1]-40)

            temps=time.time()-debut
            if temps>=3 or temps<0:
                debut=time.time()
            ancien2=(bombe2_position)

continuer = True
while continuer: # Fait appel à toutes les fonctions ci dessus

     personnage()
     pygame.time.Clock().tick(25)
     dessiner()
     gererClavierEtSouris()

# déplacement fantome 1:
     if fantome_position[1]>35 and fantome_position [0]==35:
            fantome_position=(fantome_position[0] , fantome_position[1] - 5 )
            fantome_hitbox=pygame.Rect((fantome_position),(30,30))

     elif fantome_position[0]<515 and fantome_position [1]==35:
            fantome_position=(fantome_position[0] + 5 , fantome_position[1] )
            fantome_hitbox=pygame.Rect((fantome_position),(30,30))

     elif fantome_position[1]<515 and fantome_position[0]==515:
            fantome_position=(fantome_position[0] , fantome_position[1] + 5 )
            fantome_hitbox=pygame.Rect((fantome_position),(30,30))

     elif fantome_position[0]>35 and fantome_position [1]==515:
            fantome_position=(fantome_position[0] - 5 , fantome_position[1] )
            fantome_hitbox=pygame.Rect((fantome_position),(30,30))


# déplacement fantome 2:
     if fantome2_position[1]<435 and fantome2_position[0]==115:
            fantome2_position=(fantome2_position[0] , fantome2_position[1] + 5 )
            fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))


     elif fantome2_position[1]>115 and fantome2_position [0]==435:
            fantome2_position=(fantome2_position[0] , fantome2_position[1] - 5 )
            fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))


     elif fantome2_position[0]<435 and fantome2_position [1]==435:
            fantome2_position=(fantome2_position[0] + 5 , fantome2_position[1] )
            fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))

     elif fantome2_position[0]>115 and fantome2_position [1]==115:
            fantome2_position=(fantome2_position[0] - 5 , fantome2_position[1] )
            fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))

# déplacement fantome 3:
     if fantome3_position[1]>195 and fantome3_position [0]==195:
            fantome3_position=(fantome3_position[0] , fantome3_position[1] - 5 )
            fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))

     elif fantome3_position[0]<355 and fantome3_position [1]==195:
            fantome3_position=(fantome3_position[0] + 5 , fantome3_position[1] )
            fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))

     elif fantome3_position[1]<355 and fantome3_position[0]==355:
            fantome3_position=(fantome3_position[0] , fantome3_position[1] + 5 )
            fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))

     elif fantome3_position[0]>195 and fantome3_position [1]==355:
            fantome3_position=(fantome3_position[0] - 5 , fantome3_position[1] )
            fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))




    # temps qui permet d'afficher la bombe puis la faire exploser 3sec apres puis le feu qui dure 3 secondes pour le joueur 1
     temps2=time.time()-debut2
     if temps2<3 and temps2>=0: # entre 0 et 3 seconde après la pose de la bombe, la bombe est simplement affichée sur le terrain
        pass

     if temps2>=3 and temps2<=6: # Entre 3 et 6 secondes après avoir appuyer si la touche espace l'explosion se déclenche
        feu_rect_vertical=pygame.Rect((ancien[0], ancien[1]-40),(40,120))  # crée un rectancle vertical avec comme centre la bombe
        feu_rect_horizontal=pygame.Rect((ancien[0]-40, ancien[1]),(120,40)) # crée un rectancle horizontal avec comme centre la bombe
        pygame.draw.rect(fenetre, (0, 0, 200), feu_rect_horizontal) # dessine les 2 rectangles
        pygame.draw.rect(fenetre, (0, 0, 200), feu_rect_vertical)
        bombe_position=(-50,-50) # la bombe repart à sa position en dehors du terrain

        # on force pygame à redessiner les murs et obstacle pour ne pas voir l'explosion en croix
        pygame.draw.rect(fenetre, (253, 241, 184), mur1)
        pygame.draw.rect(fenetre, (253, 241, 184), mur2)
        pygame.draw.rect(fenetre, (253, 241, 184), mur3)
        pygame.draw.rect(fenetre, (253, 241, 184), mur4)
        for i in range (0,len(coord_obstacle)):
         obstacle=pygame.Rect(coord_obstacle[i], (40,40))
         pygame.draw.rect(fenetre, (115, 194, 251),obstacle)

     else: # l'explosion en croix repart en dehors du terrain une fois 6 secondes écoulées
        feu_rect_vertical=pygame.Rect((-50,-50),(30,130))
        feu_rect_horizontal=pygame.Rect((-50,-50),(130,30))
        pygame.draw.rect(fenetre, (253, 241, 184), feu_rect_horizontal)
        pygame.draw.rect(fenetre, (253, 241, 184), feu_rect_vertical)

    # même procédé d'explosion pour le joueur 2
     temps=time.time()-debut
     if temps<3 and temps>=0:
        pass
     if temps>=3 and temps<=6:
        feu_rect_vertical2=pygame.Rect((ancien2[0], ancien2[1]-40),(40,120))
        feu_rect_horizontal2=pygame.Rect((ancien2[0]-40, ancien2[1]),(120,40))
        pygame.draw.rect(fenetre, (200, 0, 0), feu_rect_horizontal2)
        pygame.draw.rect(fenetre, (200, 0, 0), feu_rect_vertical2)
        bombe2_position=(-50,-50)

        pygame.draw.rect(fenetre, (253, 241, 184), mur1)
        pygame.draw.rect(fenetre, (253, 241, 184), mur2)
        pygame.draw.rect(fenetre, (253, 241, 184), mur3)
        pygame.draw.rect(fenetre, (253, 241, 184), mur4)

        for i in range (0,len(coord_obstacle)):
         obstacle=pygame.Rect(coord_obstacle[i], (40,40))
         pygame.draw.rect(fenetre, (115, 194, 251),obstacle)
     else:
        feu_rect_vertical2=pygame.Rect((-50,-50),(30,130))
        feu_rect_horizontal2=pygame.Rect((-50,-50),(130,30))
        pygame.draw.rect(fenetre, (200, 0,0), feu_rect_horizontal2)
        pygame.draw.rect(fenetre, (200, 0,0), feu_rect_vertical2)




# tous les cas possible de collision entre l'un des 2 persos et les explosions de bombes qui engendre un gain de point selon le cas grace à la commande .colliderect
     if feu_rect_horizontal.colliderect(bush_hitbox) and afficher:
        points1+=1
        afficher=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        #cri_bush.play()
     if feu_rect_vertical.colliderect(bush_hitbox) and afficher:
        points1+=1
        afficher=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        #cri_bush.play()

     if feu_rect_horizontal.colliderect(oussama_hitbox) and afficher:
        points2+=1
        afficher=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        #cri_oussama.play()
     if feu_rect_vertical.colliderect(oussama_hitbox)and afficher:
        points2+=1
        afficher=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        #cri_oussama.play()



     if feu_rect_horizontal2.colliderect(bush_hitbox) and afficher2:
        points1+=1
        afficher2=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        #cri_bush.play()
     if feu_rect_vertical2.colliderect(bush_hitbox) and afficher2:
        points1+=1
        afficher2=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        #cri_bush.play()

     if feu_rect_horizontal2.colliderect(oussama_hitbox) and afficher2:
        points2+=1
        afficher2=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        #cri_oussama.play()
     if feu_rect_vertical2.colliderect(oussama_hitbox)and afficher2:
        points2+=1
        afficher2=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        #cri_oussama.play()


     if fantome_hitbox.colliderect(bush_hitbox) or fantome2_hitbox.colliderect(bush_hitbox) or fantome3_hitbox.colliderect(bush_hitbox):
        points1+=1
        afficher=False
        bush_position=(520,520)
        fantome_position=(35,515)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        #cri_bush.play()
     if fantome_hitbox.colliderect(oussama_hitbox) or fantome2_hitbox.colliderect(oussama_hitbox) or fantome3_hitbox.colliderect(oussama_hitbox):
        points2+=1
        afficher=False
        oussama_position=(30,30)
        fantome_position=(35,515)
        oussama_hitbox=pygame.Rect((oussama_position),(30,30))
        #cri_oussama.play()

     if points1==5:  # fin du jeu si un des joueurs obtient 5 point et rappelle la fonction dessiner qui indique d'afficher le message de victoire
        dessiner()
        pygame.time.wait(5000)
        continuer=False
     if points2==5:
        dessiner()
        pygame.time.wait(5000)
        continuer=False




pygame.quit() # fermeture du jeu à la fin du programme
