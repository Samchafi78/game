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

def menu(): #creation du menu principale
    menu=Tk()# tkinter permet de faire le menu
    menu.title("Bomb Journee")
    menu.minsize(480,320)                           #dans cette partie la nous nous occupons de la taille, couleurs et emplacements du titre
    menu.resizable(width=False,height=False)
    menu.configure(bg="white")
    bombjournee=Image.open("menu.jpg")
    photo=ImageTk.PhotoImage(bombjournee)
    bombjournee2=Label(menu,image=photo,bg="white")
    bombjournee2.pack()
    espace=Frame(menu,height=75,borderwidth=1,bg="white")
    espace.pack()
    def quitter():  #creation de la fonction quitter lorsque on quitte la page
        menu.destroy()
    lancer=Button(menu,text="Lancer le jeu",command=quitter,bg="dodgerblue",fg="white",width=50,height=1)
    lancer.pack()
    espace.pack()
    def menu2(): #il s'agit de la partie des instructions du jeux
        menu.destroy()
        menu2=Tk()
        menu2.title("Contrôles")
        menu2.minsize(300,305)
        menu2.resizable(width=False,height=False)
        menu2.configure(bg="white")
        controle=Image.open("menu2.jpg")
        photo2=ImageTk.PhotoImage(controle)
        controle2=Label(menu2,image=photo2,bg="white")
        controle2.pack()
        menu2.mainloop()
    cmd=Button(menu,text="Contrôles",command=menu2,bg="dodgerblue",fg="white",width=50,height=1)
    espace2=Frame(menu,height=10,borderwidth=1,bg="white")
    espace2.pack()
    cmd.pack()
    menu.mainloop()
menu()


# Initialisation des variables
fenetre = pygame.display.set_mode( (580,630) ) # Définition de la taille du terrain de jeu
mur1=pygame.Rect(0, 0, 580, 30)
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
pygame.display.set_caption("Terrorist Tycoon") # Définit le titre de la fenêtre

#creation du joueur 1 ainsi que sa position initiale avec sa hitbox
oussama_photo=pygame.image.load("BenLaden.png")
oussama=pygame.transform.scale(oussama_photo, (30,30))
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


#le positionnement de la bombe au depart est a l'exterieur du terrain dans des coordonnées inconnues
# puis par la suite on la deplacera
bombe_position=(-40, -40)
bombe_photo=pygame.image.load("bomb.png")
bombe=pygame.transform.scale(bombe_photo, (40,40)) # on redefinie le format de l'image 40 pix sur 40 pix
bombe_hitbox=pygame.Rect((bombe_position), (40,40))#hitbox associé a la bombe pour le joueur 1

# on fera de meme pour le joueur 2
bombe2_position=(-40, -40)
bombe2_photo=pygame.image.load("bomb.png")
bombe2=pygame.transform.scale((bombe2_photo), (40,40))
bombe2_hitbox=pygame.Rect((bombe2_position), (40,40))


hitbox_obstacle=[] #liste qui va contenir les hitbox de tous les obstacles fixes

touchesPressees = pygame.key.get_pressed()

#différent temps qui bva permettre l'explosion des bombes
bombepose=0
debut=time.time()
debut2=time.time()


ancien=(-1000,0)
ancien2=(-1000,0)

cri_oussama=pygame.mixer.Sound("7000.wav")
cri_bush=pygame.mixer.Sound("13405.wav")

points1=0
points2=0
arial24 = pygame.font.SysFont("arial",24)
score_J1 = arial24.render("SCORE J1 : "+str(points1),True,pygame.Color(0,0,255))
score_J2 = arial24.render("SCORE J2 : "+str(points2),True,pygame.Color(255,0,0))


for i in range (0,len(coord_obstacle)):
     	obstacle=pygame.Rect(coord_obstacle[i], (40,40))
     	hitbox_obstacle.append(obstacle)


feu_rect_vertical=pygame.Rect((bombe_position[0], bombe_position[1]),(40,40))
feu_rect_horizontal=pygame.Rect((bombe_position[0], bombe_position[1]),(40,40))
feu_rect_vertical2=pygame.Rect((bombe2_position[0]-5, bombe2_position[1]-55),(40,140))
feu_rect_horizontal2=pygame.Rect((bombe2_position[0]-55, bombe2_position[1]-5),(140,40))

winJ1= arial24.render("Oussama (J1) a gagné",True,pygame.Color(0,0,255))
winJ2=arial24.render("Bush (J2) a gagné",True, pygame.Color(255,0,0))

def dessiner(): # Procédure d'affichage du serpent
    global fenetre, continuer, obstacle, bush_hitbox, dernièretouche, touchePressees, start, debut2,winJ1,winJ2
    fenetre.fill( (96, 96, 96) )
    pygame.draw.rect(fenetre, (253, 241, 184), mur1)
    pygame.draw.rect(fenetre, (253, 241, 184), mur2)
    pygame.draw.rect(fenetre, (253, 241, 184), mur3)
    pygame.draw.rect(fenetre, (253, 241, 184), mur4)
    score_J1 = arial24.render("SCORE J1 : "+str(points1),True,pygame.Color(0,0,200))
    score_J2 = arial24.render("SCORE J2 : "+str(points2),True,pygame.Color(230,0,0))
    fenetre.blit(score_J1,(10,600))
    fenetre.blit(score_J2,(400,600))

    for i in range (0,len(coord_obstacle)):
         obstacle=pygame.Rect(coord_obstacle[i], (40,40))
         pygame.draw.rect(fenetre, (115, 194, 251),obstacle)


    if points1==5:
        fenetre.blit(winJ1,(170,275))


    if points2==5:
        fenetre.blit(winJ2,(200,275))

    pygame.display.flip()


def personnage():
    global fenetre, oussama, bombe, bombe2, start
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0
    fenetre.blit(oussama, oussama_position)
    fenetre.blit(bush,bush_position)
    fenetre.blit(fantome,fantome_position)
    fenetre.blit(fantome2,fantome2_position)
    fenetre.blit(fantome3,fantome3_position)
    fenetre.blit(bombe, (bombe_position[0],bombe_position[1]))
    fenetre.blit(bombe2, (bombe2_position[0],bombe2_position[1]))
    pygame.display.flip()
    pygame.display.flip()


def gererClavierEtSouris():
    global continuer, oussama_position, bombe_position,bombe2_position, temps,  bush_position, bush_hitbox, oussama_hitbox, coord_obstacle, obstacle, dernièretouche, touchesPressees, afficher, ancien, coord_obstacle, debut2, ancien2,afficher2
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0


#L'association des touches sur les deplacements
    touchesPressees = pygame.key.get_pressed()
    if touchesPressees[pygame.K_SPACE] == True:
        global ancien, debut
        afficher=True
        bombe_position=oussama_position
        bombe_position=(bombe_position[0]-(bombe_position[0]%40-30),bombe_position[1]-(bombe_position[1]%40-30))

        #partie qui permet que les bombes ne soient pas dans les obstacles en detectant les collisions entre elles avec leurs hitbox
        for rect in range(len(coord_obstacle)):
           if bombe_hitbox.colliderect(hitbox_obstacle[rect]) or bombe_position[0]==550 :
                bombe_position=(bombe_position[0]-40,bombe_position[1])
           if bombe_position[1]==550:
                bombe_position=(bombe_position[0],bombe_position[1]-40)

        ancien=(bombe_position)
        temps2=time.time()-debut2
        if temps2>=3 or temps2<0:
            debut2=time.time()
    if touchesPressees[pygame.K_RIGHT]==True and oussama_position[0]<520 :
         	test_oussama_position=pygame.Rect((oussama_position[0] + 5 , oussama_position[1]),(30,30))
         	if test_oussama_position.collidelist(hitbox_obstacle) != -1 :
         	  oussama_position=(oussama_position[0] - 0.001 , oussama_position[1])
         	else:
         	  oussama_position=(oussama_position[0] + 5 , oussama_position[1])
         	  oussama_hitbox=pygame.Rect((oussama_position), (30,30))
    if touchesPressees[pygame.K_LEFT] == True and oussama_position[0]>30:
         	 test_oussama_position=pygame.Rect((oussama_position[0] - 5 , oussama_position[1]),(30,30))
         	 if test_oussama_position.collidelist(hitbox_obstacle)!=-1:
                   oussama_position=(oussama_position[0] + 0.001 , oussama_position[1])
         	 else:
                  oussama_position=(oussama_position[0] - 5 , oussama_position[1])
                  oussama_hitbox=pygame.Rect((oussama_position),(30,30))
    if touchesPressees[pygame.K_UP]== True and oussama_position[1]>30:
         	test_oussama_position=pygame.Rect((oussama_position[0], oussama_position[1] - 5),(30,30))
         	if test_oussama_position.collidelist(hitbox_obstacle)!=-1:
            	 oussama_position=(oussama_position[0] , oussama_position[1] + 0.001)
         	else:
            	 oussama_position=(oussama_position[0] , oussama_position[1] - 5)
         	oussama_hitbox=pygame.Rect((oussama_position), (30,30))
    if touchesPressees[pygame.K_DOWN]== True and oussama_position[1]<520:
        	test_oussama_position=pygame.Rect((oussama_position[0], oussama_position[1] + 5),(30,30))
        	if test_oussama_position.collidelist(hitbox_obstacle)!=-1 :
                	oussama_position=(oussama_position[0], oussama_position[1] - 0.001)
        	else:
                	oussama_position=(oussama_position[0] , oussama_position[1] + 5)
        	oussama_hitbox=pygame.Rect((oussama_position), (30,30))
    if touchesPressees[pygame.K_a]==True and bush_position[0]>30 :
        test_bush_position=pygame.Rect((bush_position[0] - 5 , bush_position[1]),(30,30))
        if test_bush_position.collidelist(hitbox_obstacle) != -1 :
                	bush_position=(bush_position[0] + 0.001 , bush_position[1])
        else:
            bush_position=(bush_position[0] - 5 , bush_position[1])
            bush_hitbox=pygame.Rect((bush_position), (30,30))
    if touchesPressees[pygame.K_s]==True and bush_position[1]<520 :
    	test_bush_position=pygame.Rect((bush_position[0] , bush_position[1]+5),(30,30))
    	if test_bush_position.collidelist(hitbox_obstacle) != -1:
            	bush_position=(bush_position[0] , bush_position[1]-0.001)
    	else:
            	bush_position=(bush_position[0] , bush_position[1]+5)
    	bush_hitbox=pygame.Rect((bush_position), (30,30))
    if touchesPressees[pygame.K_d] == True and bush_position[0]<520 :
    	test_bush_position=pygame.Rect((bush_position[0] + 5 , bush_position[1]),(30,30))
    	if test_bush_position.collidelist(hitbox_obstacle) != -1 :
            	bush_position=(bush_position[0] - 0.001 , bush_position[1])
    	else:
        	bush_position=(bush_position[0] + 5 , bush_position[1])
        	bush_hitbox=pygame.Rect((bush_position), (30,30))
    if touchesPressees[pygame.K_w]== True and bush_position[1]>30:
    	test_bush_position=pygame.Rect((bush_position[0] , bush_position[1]-5),(30,30))
    	if test_bush_position.collidelist(hitbox_obstacle) != -1 :
            	bush_position=(bush_position[0] , bush_position[1]+0.001)
    	else:
            	bush_position=(bush_position[0] , bush_position[1]-5)
    	bush_hitbox=pygame.Rect((bush_position), (30,30))
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
    if oussama_hitbox.collidelist(hitbox_obstacle):
        dernieretouche=False


continuer = True
while continuer:

     personnage()
     pygame.time.Clock().tick(25)
     dessiner()
     gererClavierEtSouris()

# déplacement fantome 1:
     if fantome_position[1]>35 and fantome_position [0]==35:
         	 test_fantome_position=pygame.Rect((fantome_position[0], fantome_position[1] - 5),(30,30))
         	 if test_fantome_position.collidelist(hitbox_obstacle)!=-1:
                   fantome_position=(fantome_position[0] , fantome_position[1]+0.001)
         	 else:
                  fantome_position=(fantome_position[0] , fantome_position[1] - 5 )
                  fantome_hitbox=pygame.Rect((fantome_position),(30,30))

     elif fantome_position[0]<515 and fantome_position [1]==35:
         	 test_fantome_position=pygame.Rect((fantome_position[0] + 5, fantome_position[1]),(30,30))
         	 if test_fantome_position.collidelist(hitbox_obstacle)!=-1:
                   fantome_position=(fantome_position[0] - 0.001, fantome_position[1])
         	 else:
                  fantome_position=(fantome_position[0] + 5 , fantome_position[1] )
                  fantome_hitbox=pygame.Rect((fantome_position),(30,30))

     elif fantome_position[1]<515 and fantome_position[0]==515:
         	 test_fantome_position=pygame.Rect((fantome_position[0], fantome_position[1] + 5),(30,30))
         	 if test_fantome_position.collidelist(hitbox_obstacle)!=-1:
                   fantome_position=(fantome_position[0] , fantome_position[1]+0.001)
         	 else:
                  fantome_position=(fantome_position[0] , fantome_position[1] + 5 )
                  fantome_hitbox=pygame.Rect((fantome_position),(30,30))

     elif fantome_position[0]>35 and fantome_position [1]==515:
         	 test_fantome_position=pygame.Rect((fantome_position[0] - 5, fantome_position[1]),(30,30))
         	 if test_fantome_position.collidelist(hitbox_obstacle)!=-1:
                   fantome_position=(fantome_position[0] + 0.001, fantome_position[1])
         	 else:
                  fantome_position=(fantome_position[0] - 5 , fantome_position[1] )
                  fantome_hitbox=pygame.Rect((fantome_position),(30,30))

# déplacement fantome 2:
     if fantome2_position[1]<435 and fantome2_position[0]==115:
         	 test_fantome2_position=pygame.Rect((fantome2_position[0], fantome2_position[1] + 5),(30,30))
         	 if test_fantome2_position.collidelist(hitbox_obstacle)!=-1:
                   fantome2_position=(fantome2_position[0] , fantome2_position[1]+0.001)
         	 else:
                  fantome2_position=(fantome2_position[0] , fantome2_position[1] + 5 )
                  fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))


     elif fantome2_position[1]>115 and fantome2_position [0]==435:
         	 test_fantome2_position=pygame.Rect((fantome2_position[0], fantome2_position[1] - 5),(30,30))
         	 if test_fantome2_position.collidelist(hitbox_obstacle)!=-1:
                   fantome2_position=(fantome2_position[0] , fantome2_position[1]+0.001)
         	 else:
                  fantome2_position=(fantome2_position[0] , fantome2_position[1] - 5 )
                  fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))


     elif fantome2_position[0]<435 and fantome2_position [1]==435:
         	 test_fantome2_position=pygame.Rect((fantome2_position[0] + 5, fantome2_position[1]),(30,30))
         	 if test_fantome2_position.collidelist(hitbox_obstacle)!=-1:
                   fantome2_position=(fantome2_position[0] - 0.001, fantome2_position[1])
         	 else:
                  fantome2_position=(fantome2_position[0] + 5 , fantome2_position[1] )
                  fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))

     elif fantome2_position[0]>115 and fantome2_position [1]==115:
         	 test_fantome2_position=pygame.Rect((fantome2_position[0] - 5, fantome2_position[1]),(30,30))
         	 if test_fantome2_position.collidelist(hitbox_obstacle)!=-1:
                   fantome2_position=(fantome2_position[0] + 0.001, fantome2_position[1])
         	 else:
                  fantome2_position=(fantome2_position[0] - 5 , fantome2_position[1] )
                  fantome2_hitbox=pygame.Rect((fantome2_position),(30,30))

# déplacement fantome 3:
     if fantome3_position[1]>195 and fantome3_position [0]==195:
         	 test_fantome3_position=pygame.Rect((fantome3_position[0], fantome3_position[1] - 5),(30,30))
         	 if test_fantome3_position.collidelist(hitbox_obstacle)!=-1:
                   fantome3_position=(fantome3_position[0] , fantome3_position[1]+0.001)
         	 else:
                  fantome3_position=(fantome3_position[0] , fantome3_position[1] - 5 )
                  fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))

     elif fantome3_position[0]<355 and fantome3_position [1]==195:
         	 test_fantome3_position=pygame.Rect((fantome3_position[0] + 5, fantome3_position[1]),(30,30))
         	 if test_fantome3_position.collidelist(hitbox_obstacle)!=-1:
                   fantome3_position=(fantome3_position[0] - 0.001, fantome3_position[1])
         	 else:
                  fantome3_position=(fantome3_position[0] + 5 , fantome3_position[1] )
                  fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))

     elif fantome3_position[1]<355 and fantome3_position[0]==355:
         	 test_fantome3_position=pygame.Rect((fantome3_position[0], fantome3_position[1] + 5),(30,30))
         	 if test_fantome3_position.collidelist(hitbox_obstacle)!=-1:
                   fantome3_position=(fantome3_position[0] , fantome3_position[1]+0.001)
         	 else:
                  fantome3_position=(fantome3_position[0] , fantome3_position[1] + 5 )
                  fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))

     elif fantome3_position[0]>195 and fantome3_position [1]==355:
         	 test_fantome3_position=pygame.Rect((fantome3_position[0] - 5, fantome3_position[1]),(30,30))
         	 if test_fantome3_position.collidelist(hitbox_obstacle)!=-1:
                   fantome3_position=(fantome3_position[0] + 0.001, fantome3_position[1])
         	 else:
                  fantome3_position=(fantome3_position[0] - 5 , fantome3_position[1] )
                  fantome3_hitbox=pygame.Rect((fantome3_position),(30,30))

    # temps qui permet d'afficher la bombe puis la faire exploser 3sec apres puis le feu qui dure 3 secondes

     temps=time.time()-debut
     if temps<3 and temps>=0:
        pass
     if temps>=3 and temps<=6:

        #permet d'eviter le flicker en forcant pygame de redessiner par dessus les obstacles deja dessinés
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

     temps2=time.time()-debut2
     if temps2<3 and temps2>=0:
        pass

     if temps2>=3 and temps2<=6:
        feu_rect_vertical=pygame.Rect((ancien[0], ancien[1]-40),(40,120))
        feu_rect_horizontal=pygame.Rect((ancien[0]-40, ancien[1]),(120,40))
        pygame.draw.rect(fenetre, (0, 0, 200), feu_rect_horizontal)
        pygame.draw.rect(fenetre, (0, 0, 200), feu_rect_vertical)
        bombe_position=(-50,-50)
        pygame.draw.rect(fenetre, (253, 241, 184), mur1)
        pygame.draw.rect(fenetre, (253, 241, 184), mur2)
        pygame.draw.rect(fenetre, (253, 241, 184), mur3)
        pygame.draw.rect(fenetre, (253, 241, 184), mur4)
        for i in range (0,len(coord_obstacle)):
         obstacle=pygame.Rect(coord_obstacle[i], (40,40))
         pygame.draw.rect(fenetre, (115, 194, 251),obstacle)
     else:
        feu_rect_vertical=pygame.Rect((-50,-50),(30,130))
        feu_rect_horizontal=pygame.Rect((-50,-50),(130,30))
        pygame.draw.rect(fenetre, (253, 241, 184), feu_rect_horizontal)
        pygame.draw.rect(fenetre, (253, 241, 184), feu_rect_vertical)

     if feu_rect_horizontal.colliderect(bush_hitbox) and afficher:
        points1+=1
        afficher=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        cri_bush.play()
     if feu_rect_vertical.colliderect(bush_hitbox) and afficher:
        points1+=1
        afficher=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        cri_bush.play()

     if feu_rect_horizontal.colliderect(oussama_hitbox) and afficher:
        points2+=1
        afficher=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        cri_oussama.play()
     if feu_rect_vertical.colliderect(oussama_hitbox)and afficher:
        points2+=1
        afficher=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        cri_oussama.play()



     if feu_rect_horizontal2.colliderect(bush_hitbox) and afficher2:
        points1+=1
        afficher2=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        cri_bush.play()
     if feu_rect_vertical2.colliderect(bush_hitbox) and afficher2:
        points1+=1
        afficher2=False
        bush_position=(520,520)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        cri_bush.play()

     if feu_rect_horizontal2.colliderect(oussama_hitbox) and afficher2:
        points2+=1
        afficher2=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        cri_oussama.play()
     if feu_rect_vertical2.colliderect(oussama_hitbox)and afficher2:
        points2+=1
        afficher2=False
        oussama_position=(30,30)
        oussama_hitbox=pygame.Rect((oussama_position), (30,30))
        cri_oussama.play()


     if fantome_hitbox.colliderect(bush_hitbox) or fantome2_hitbox.colliderect(bush_hitbox) or fantome3_hitbox.colliderect(bush_hitbox):
        points1+=1
        afficher=False
        bush_position=(520,520)
        fantome_position=(35,515)
        bush_hitbox=pygame.Rect((bush_position),(30,30))
        cri_bush.play()
     if fantome_hitbox.colliderect(oussama_hitbox) or fantome2_hitbox.colliderect(oussama_hitbox) or fantome3_hitbox.colliderect(oussama_hitbox):
        points2+=1
        afficher=False
        oussama_position=(30,30)
        fantome_position=(35,515)
        oussama_hitbox=pygame.Rect((oussama_position),(30,30))
        cri_oussama.play()

     if points1==5:
        dessiner()
        pygame.time.wait(5000)
        continuer=False
     if points2==5:
        dessiner()
        pygame.time.wait(5000)
        continuer=False




pygame.quit()
