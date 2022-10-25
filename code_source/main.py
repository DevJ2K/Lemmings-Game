########################################################################################################################
#LES MODULES
########################################################################################################################
from tkinter import * #type: ignore
import random
import json
import logging
from lemmings_class import *
import pygame
from pathlib import Path
from time import sleep


########################################################################################################################
#TOUS LES SONS
########################################################################################################################
pygame.init()
start_sound = pygame.mixer.Sound("sons/accueil.wav")
start_sound.set_volume(0.5)

background_song = pygame.mixer.Sound("sons/background_game.wav")
background_song.set_volume(0.4)

death_sound = pygame.mixer.Sound("sons/death.wav")
death_sound.set_volume(0.4)

portail = pygame.mixer.Sound("sons/portail.wav")
portail.set_volume(0.4)

changement_couleur = pygame.mixer.Sound("sons/changement_couleur.wav")
changement_couleur.set_volume(0.4)

click_effect = pygame.mixer.Sound("sons/click-sound.wav")
click_effect.set_volume(0.8)


########################################################################################################################
#CONFIGURATION DU LOGGING
########################################################################################################################
logging.basicConfig(level=logging.DEBUG,
                    filename="game.log",
                    filemode="w",
                    encoding="utf_8",
                    format='%(asctime)s - %(levelname)s - %(message)s')


########################################################################################################################
#CREATION DE LA FENÊTRE
########################################################################################################################
width = 1100 + 400
height = 600
window=Tk()
window.configure(bg="#000000")
window.title("LEMMINGS GAME")
window.iconbitmap("textures/t1.ico")
window.geometry(f'{str(width)}x{str(height)}')
window.resizable(width=False, height=False)


########################################################################################################################
#CREATION DU FOND DE MENU
########################################################################################################################
image_main_menu = PhotoImage(file="textures/background/main_menu.png")
canva_background = Canvas(window, width=width, height=height, bg="#000000", highlightthickness=0)
canva_background.place(x=0, y=0)
image_location = canva_background.create_image(0, 0, image=image_main_menu, anchor=NW)
#démarage du song en fond
start_sound.play(-1, 0, 1000)
#Can de jeu
can1=Canvas(window,bg="black",width=width,height=height)


########################################################################################################################
#FONCTION D'IMPORT DE MAP ET TEXTURES + Dico texture/map
########################################################################################################################
def recup_textures(name="none_texture.gif") -> PhotoImage:
    """Recuperer la texture mis en parametre dans le fichier all_textures.json

    Args:
        name (str): nom du fichier dans le dictionnaire du fichier all_textures.json. Defaults to "none_texture.gif".

    Returns:
        PhotoImage: image de la texture choisie
    """
    with open("textures/all_textures.json", "r") as f:
        dico_all_textures = json.load(f)
        return PhotoImage(file=f"textures/{dico_all_textures[name]}")


def recup_map(numero: int) -> list:
    """Recuperer la matrice de la map n°x

    Args:
        numero (int): numero de map

    Returns:
        list: la matrice de la map
    """
    with open(f"maps/map{numero}.json", "r") as f:
        current_map = json.load(f)
        return current_map


#dictionnairte des maps et textures
dico={"SOL":recup_textures("vide"), "VID":recup_textures("vide"), "S__":recup_textures("vide"), "SP1":recup_textures("vide"), "SP2":recup_textures("vide")}

dico_bg_img = {
    "game_1":   PhotoImage(file="textures/background/game_1.gif"),
    "game_2":   PhotoImage(file="textures/background/game_2.gif"),
    "game_3":   PhotoImage(file="textures/background/game_3.gif"),
    "game_4":   PhotoImage(file="textures/background/game_4.gif"),
    "game_5":   PhotoImage(file="textures/background/game_5.gif"),
    "end_game_background": PhotoImage(file="textures/background/end_game.png"),
    "game_over": PhotoImage(file="textures/background/game_over.png")
}

########################################################################################################################
#Infos in-game
########################################################################################################################
info_menu = PhotoImage(file="textures/background/infos_menu.png")
canva_info =  Canvas(window, width=width, height=height, bg="#FFFFFF", highlightthickness=0)
image_info_menu = canva_info.create_image(0, 0, image=info_menu, anchor=NW)

lemming_life_label = Label(window, text="0", bg="#03005C", fg="white", relief="groove", width=3, font=("Impact", 14))
lemming_dead_label = Label(window, text="0", bg="#03005C", fg="white", relief="groove", width=3,font=("Impact", 14))
lemming_arrived_label = Label(window, text="0", bg="#03005C", fg="white", relief="groove", width=3,font=("Impact", 14))


########################################################################################################################
#FONCTION EN JEU
########################################################################################################################
#DEPLACEMENT
########################################################################################################################
def deplace(perso) -> None:
    """deplace un perso en suivant les règles du jeu lemmings

    Args:
        perso (Personnage): l'instance de la classe Personnage()
    """
    global nbr_arrives_en_cours, nbr_vivant_en_cours, nbr_mort_en_cours
    try:
        key = perso.droite.cget("file")
        key = Path(key).stem

        if niveau.get_case(perso) == "SP1": #Case spéciale n°1 : Change la tenue du personnage qui passe sur la case spéciale
            changement_couleur.play()

            if int(key[-1]) < 4:
                perso.set_image_gauche(recup_textures(f"zombieD_t{int(key[-1])+1}"))
                perso.set_image_droite(recup_textures(f"zombieG_t{int(key[-1])+1}"))
            else:
                perso.set_image_gauche(recup_textures(f"zombieD_t1"))
                perso.set_image_droite(recup_textures(f"zombieG_t1"))

            perso.affiche_lem()

        if niveau.get_case(perso) == "SP2": #Case spéciale n°2 : Met le personnage qui passe sur la case spéciale à l'envers
            perso.set_image_gauche(recup_textures(f"zombieD{key[2:]}_turned"))
            perso.set_image_droite(recup_textures(f"zombieG{key[2:]}_turned"))
            perso.affiche_lem()

        if niveau.get_case(perso) == "S__": #Case d'arrivée
            portail.play()
            textured_lemmings[f"zombie{key[2:]}"] += 1

            niveau.changement_nature_case(perso)
            perso.efface_image()
            niveau.enleve_liste_perso(perso)
            lemmings_alive.append(perso)
            
            nbr_vivant_en_cours -= 1
            nbr_arrives_en_cours += 1
            lemming_life_label['text'] = nbr_vivant_en_cours
            lemming_arrived_label['text'] = nbr_arrives_en_cours
            
            
        elif niveau.get_nature_case_dessous(perso):
            niveau.changement_nature_case(perso)
            perso.deplace_bas()
            niveau.changement_nature_case(perso)
            
        elif perso.get_direction() == 0:
            if niveau.get_nature_case_gauche(perso) == False:
                perso.set_direction(1)

            elif niveau.get_nature_case_gauche(perso) == True:
                niveau.changement_nature_case(perso)
                perso.deplace_gauche()
                niveau.changement_nature_case(perso)
            
        elif perso.get_direction() == 1:
            if niveau.get_nature_case_droite(perso) == False:
                
                perso.set_direction(0)


            elif niveau.get_nature_case_droite(perso) == True:
                niveau.changement_nature_case(perso)
                perso.deplace_droite()
                niveau.changement_nature_case(perso)

        if perso.get_direction() == 0 and perso.get_x() < 0:
            death_sound.play()
            logging.info("Un lemming est mort.")
            perso.efface_image()
            niveau.enleve_liste_perso(perso)
            niveau.changement_nature_case(perso)
            nbr_mort_en_cours += 1
            nbr_vivant_en_cours -= 1
            lemming_life_label['text'] = nbr_vivant_en_cours
            lemming_dead_label['text'] = nbr_mort_en_cours
        
    except IndexError:
        death_sound.play()
        logging.info("Un lemming est mort.")
        perso.efface_image()
        niveau.enleve_liste_perso(perso)
        niveau.changement_nature_case(perso)
        nbr_mort_en_cours += 1
        nbr_vivant_en_cours -= 1
        lemming_life_label['text'] = nbr_vivant_en_cours
        lemming_dead_label['text'] = nbr_mort_en_cours
    

########################################################################################################################
#FONCTION NOUVEAU NIVEAU
########################################################################################################################
niveau_number = 1

def new_niveau(number: int) -> Jeu:
    """Creer une instance du niveau n°x

    Args:
        number (int): numéro de niveau

    Returns:
        Jeu: Instance de la classe Jeu
    """
    global can_game
    background_game1 = can_game.create_image(0, 0, image=dico_bg_img[f"game_{number}"], anchor=NW)
    ma_matrice=recup_map(niveau_number)
    return Jeu(ma_matrice,dico,can_game,["SOL"])


can_game = Canvas(window, width=width-400, height=height, bg="#FF00FF", highlightthickness=0) 
niveau = new_niveau(1)

########################################################################################################################
#DEMARRER LE NIVEAU
########################################################################################################################

def play_niveau(number: int) -> None:
    """Permet de jouer le niveau n°x

    Args:
        number (int): numéro de niveau
    """
    global niveau_number, niveau, lemmings_alive, nbr_vivant_en_cours, nbr_mort_en_cours, nbr_arrives_en_cours

    logging.info(f"Le Niveau n°{number} est en cours...")
    lemmings_alive = []
    niveau = new_niveau(niveau_number)
    niveau.dessine_matrice()
    
    for i in textured_lemmings:

        while textured_lemmings[i] > 0:
            new_user = Personnage(niveau,random.choice([1, 5, 17]),0,0,recup_textures(f"zombieG{i[6:]}"), recup_textures(f"zombieD{i[6:]}"))

            lemmings_alive.append(new_user)
            textured_lemmings[i] -= 1


    for perso in lemmings_alive:
        niveau.ajoute_liste_perso(perso)
        perso.affiche_lem()
        
    lemmings_alive = []

    while niveau.get_liste_perso() != []:
        sleep(vitesse_lemmings)
        for elt in niveau.get_liste_perso():

                deplace(elt)

        window.update()

    niveau_number += 1
    
    sleep(1)
    try:
        nbr_vivant_en_cours = len(lemmings_alive)
        nbr_mort_en_cours = 0
        nbr_arrives_en_cours = 0
        
        lemming_life_label['text'] = nbr_vivant_en_cours
        lemming_dead_label['text'] = nbr_mort_en_cours
        lemming_arrived_label['text'] = nbr_arrives_en_cours
        play_niveau(niveau_number)
    except KeyError:
        print("fin du jeu")
        canva_background = Canvas(window, width=width, height=height, bg="#000000", highlightthickness=0)
        canva_background.place(x=0, y=0)
        if nbr_vivant_en_cours > 0:
            image_location = canva_background.create_image(0, 0, image=dico_bg_img["end_game_background"], anchor=NW)
            lemming_restant = Label(window, text=nbr_vivant_en_cours, bg="#5853F8", fg="white", relief="groove", bd=5, width=3, font=("Impact", 30))
            lemming_restant.place(x=870, y=435)
            logging.info(f"Bravo, tu as terminé avec '{nbr_vivant_en_cours}' lemmings !")
        else:
            image_location = canva_background.create_image(0, 0, image=dico_bg_img["game_over"], anchor=NW)
            logging.info(f"Tes lemmings '{nbr_lemmings}' sont morts.")


########################################################################################################################
#VALEURS PAR DEFAUT
########################################################################################################################
lemmings_alive = []

vitesse_lemmings = 0.1

nbr_lemmings = 10

nbr_vivant_en_cours = 0
nbr_mort_en_cours = 0
nbr_arrives_en_cours = 0

lemming_life_label['text'] = nbr_vivant_en_cours
lemming_dead_label['text'] = nbr_mort_en_cours
lemming_arrived_label['text'] = nbr_arrives_en_cours


textured_lemmings = {
    "zombie_t1": 0,
    "zombie_t2": 0,
    "zombie_t3": 0,
    "zombie_t4": 0,

    "zombie_t1_turned": 0,
    "zombie_t2_turned": 0,
    "zombie_t3_turned": 0,
    "zombie_t4_turned": 0    
}


########################################################################################################################
#FONCTION DANS LE MENU
########################################################################################################################
def playFonc() -> None:
    """Fonction pour accéder aux paramètres
    """
    global texture_number, pack_texture

    click_effect.play()
    texture_number = 1
    pack_texture = recup_textures(f"zombie_t{texture_number}")
    personnage_canvas.create_image(0, 0, image=pack_texture, anchor=NW)
    settings_frame['bg'] = personnage_frame_button['bg'] = lemmings_frame['bg'] = list_color[texture_number-1]

    main_frame_button.pack_forget()    
    
    settings_frame.pack(expand=YES)

    return_button.place(x=0, y=0)

    
def backFonc() -> None:
    """Retour à l'écran d'accueil
    """
    click_effect.play()
    return_button.place_forget()
    settings_frame.pack_forget()
    main_frame_button.pack(expand=YES)




def start_game() -> None:
    """Lancer la partie
    """
    global nbr_vivant_en_cours, niveau
    click_effect.play()
    start_sound.stop()
    textured_lemmings[f"zombie_t{texture_number}"] = nbr_lemmings

    settings_frame.destroy()
    lemmings_frame.destroy()
    return_button.destroy()
    personnage_canvas.destroy()
    personnage_frame_button.destroy()
    canva_background.destroy()

    can_game.place(x=0, y=0)

    nbr_vivant_en_cours = nbr_lemmings
    
    canva_info.place(x=1100, y=0)

    can1.place(x=0,y=0)

    lemming_life_label.place(x=1100+275, y=179)
    lemming_dead_label.place(x=1100+275, y=280)
    lemming_arrived_label.place(x=1100+280, y=385)

    background_song.play(-1, 0, 1000)
    
    play_niveau(1)


def remove_lemmings() -> None:
    """Retirer des lemmings
    """
    global nbr_lemmings
    click_effect.play()
    nbr_lemmings = nbr_lemmings - 1 if nbr_lemmings > 5 else 5
    nbr_lemmings_text['text'] = nbr_lemmings

def add_lemmings() -> None:
    """Ajouter des lemmings
    """
    global nbr_lemmings
    click_effect.play()
    nbr_lemmings = nbr_lemmings + 1 if nbr_lemmings < 30 else 30
    nbr_lemmings_text['text'] = nbr_lemmings
    

########################################################################################################################
pack_texture = recup_textures("zombie_t1")
texture_number = 1
list_color = ["#A9A69D", "#ACA6AD", "#B07E7C", "#636363"]

def leftChangePersonnage() -> None:
    """Changer de personnage vers la gauche
    """
    global texture_number, personnage_canvas, pack_texture
    click_effect.play()
    if texture_number > 1:
        texture_number -= 1
        pack_texture = recup_textures(f"zombie_t{texture_number}")
        personnage_canvas.create_image(0, 0, image=pack_texture, anchor=NW)

    else:
        texture_number = 4
        pack_texture = recup_textures(f"zombie_t{texture_number}")
        personnage_canvas.create_image(0, 0, image=pack_texture, anchor=NW)

    settings_frame['bg'] = personnage_frame_button['bg'] = lemmings_frame['bg'] = list_color[texture_number-1]


def rightChangePersonnage() -> None:
    """Changer de personnage vers la droite
    """
    global texture_number, personnage_canvas, pack_texture
    click_effect.play()
    if texture_number < 4:
        texture_number += 1
        pack_texture = recup_textures(f"zombie_t{texture_number}")
        personnage_canvas.create_image(0, 0, image=pack_texture, anchor=NW)

    else:
        texture_number = 1
        pack_texture = recup_textures(f"zombie_t{texture_number}")
        personnage_canvas.create_image(0, 0, image=pack_texture, anchor=NW)

    settings_frame['bg'] = personnage_frame_button['bg'] = lemmings_frame['bg'] = list_color[texture_number-1]

########################################################################################################################
#LES BOUTONS
########################################################################################################################
main_frame_button = Frame(window, bg="#000000")

play_button = Button(main_frame_button, text="Jouer", bg="#D2D2D2", fg="black", relief="groove", width=10, font=("Constantia", 20), command=playFonc)
leave_button = Button(main_frame_button, text="Quitter", bg="#2388BE", fg="white", relief="groove",width=10,font=("Constantia", 20), command=window.quit)
return_button = Button(window, text="Retour", bg="#2388BE",fg="white",relief="groove", highlightthickness=0,  height=1, font=("Caladea", 12), command=backFonc)

play_button.grid(row=0)
leave_button.grid(row=1)
main_frame_button.pack(expand=YES)


########################################################################################################################
#LES FRAMES
########################################################################################################################
settings_frame = Frame(window, bg="#A9A69D", bd=5, highlightbackground="black", highlightthickness=5)

personnage_frame_button = Frame(settings_frame, bg="#A9A69D")
lemmings_frame = Frame(settings_frame, bg="#A9A69D")
personnage_canvas = Canvas(settings_frame, width=200, height=200, bg="#FFF", highlightthickness=0)

personnage_canvas.grid(column=0, row=0)
lemmings_frame.grid(column=0, row=1)
personnage_frame_button.grid(column=0, row=2)



########################################################################################################################
#LES FLECHES DE MENU
########################################################################################################################
flecheGauche = Button(personnage_frame_button, text="<", bg="#2388BE", fg="white", relief="groove", width=5, font=("Californian FB", 15), command=leftChangePersonnage)
flecheGauche.grid(column=0, row=0)

valider = Button(personnage_frame_button, text="JOUER", bg="#2388BE", fg="white", relief="groove", width=9, font=("Californian FB", 15), command=start_game)
valider.grid(column=1, row=0)

flecheDroite = Button(personnage_frame_button, text=">", bg="#2388BE", fg="white", relief="groove", width=5, font=("Californian FB", 15), command=rightChangePersonnage)
flecheDroite.grid(column=2, row=0)

########################################################################################################################
remove_lemming_button = Button(lemmings_frame, text="<", bg="#2388BE", fg="white", relief="groove", width=5, font=("Californian FB", 15), command=remove_lemmings)
remove_lemming_button.grid(column=0, row=0)

nbr_lemmings_text = Label(lemmings_frame, text=f"{nbr_lemmings}", bg="#2388BE", fg="white", relief="groove", width=9, font=("Californian FB", 15))
nbr_lemmings_text.grid(column=1, row=0)

add_lemming_button = Button(lemmings_frame, text=">", bg="#2388BE", fg="white", relief="groove", width=5, font=("Californian FB", 15), command=add_lemmings)
add_lemming_button.grid(column=2, row=0)


########################################################################################################################
#lancement de la boucle tkinter   
########################################################################################################################
window.mainloop()