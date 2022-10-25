# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:22:16 2021

@author: jeffa
"""
from random import randint 
from time import sleep

class Personnage:
    """classe du personnages héros"""
    
    def __init__(self,jeu_en_cours,x,y,d,image1,image2):
        self.je = jeu_en_cours #rattache le personnage à un jeu
        self.y = y  #ligne du perso
        self.x = x  #colonne du perso
        self.d = d #int de valeur 0 ou 1, droite=0 gauche =1
        self.droite = image1  #image1 = un str qui donne le nom de l'image à utiliser
        self.gauche = image2  #image2 = un str qui donne le nom de l'image à utiliser      
        self.tableau_image = [self.droite,self.gauche]  #le tableau des différentes images du jeu     
      
    def get_x(self):
        """renvoie la ligne du perso"""
        return self.x
    
    def get_y(self):
        """renvoie la colonne du perso"""
        return self.y
    
    def get_direction(self):
        """renvoie la direction du perso"""
        return self.d
        
    def set_image_droite(self,image):
        """change l'image droite du perso"""
        self.droite = image
        self.tableau_image = [self.droite,self.gauche] 
        
    def set_image_gauche(self,image):
        """change l'image gauche du perso"""   
        self.gauche = image
        self.tableau_image = [self.droite,self.gauche] 
        
    def affiche_lem(self):
        """affiche un lemmings dans le jeu en cours"""
        self.perso=self.je.can.create_image(self.x*50,self.y*50,image=self.tableau_image[self.d],anchor="nw")
        
    def deplace_droite(self):
        """deplace le perso d'une colonne à droite"""
        self.x = self.x + 1
        self.je.can.coords(self.perso,self.x*50,self.y*50) 
        
    def deplace_gauche(self):
        """deplace le perso d'une colonne à gauche"""    
        self.x = self.x - 1
        self.je.can.coords(self.perso,self.x*50,self.y*50) 
        
    def deplace_bas(self):
        """deplace le perso d'une ligne en bas"""    
        self.y = self.y + 1
        self.je.can.coords(self.perso,self.x*50,self.y*50)    
    
    def set_direction(self,d):
        """change la direction du personnage et son image
        0 : gauche
        1 : droite """
        self.d = d
        self.je.can.itemconfig(self.perso,image=self.tableau_image[self.d])
        
    def efface_image(self):
        """efface l'image d'un perso du canevas"""
        self.je.can.delete(self.perso)



class Jeu :
    def __init__(self,matrice,dico,canevas,cases):
        """crée le niveau à partie de son dictionnaire, sa matrice et son canevas"""
        self.lemmings =[]  #aucun lemmings en jeu
        self.matrice = matrice  #matrice du jeu
        self.longueur = len(self.matrice[0])
        self.hauteur = len(self.matrice)  #taille de la map
        self.dict = dico  #dictionnaire de la map du jeu
        self.can = canevas  #canevas où se situe le jeu
        self.cases_interdites = cases  #type list
        
        #création de la matrice des booléens indiquant si une case est True ou False
        self.matrice_bool=[[True for j in range(self.longueur)] for i in range(self.hauteur)]
        for i in range(self.hauteur):
            for j in range(self.longueur):
                if self.matrice[i][j] in self.cases_interdites :
                    self.matrice_bool[i][j] = False
                
    def dessine_matrice(self):
        """dessine la matrice dans le canevas choisi"""
        for i in range(self.hauteur):
            for j in range(self.longueur):
                self.can.create_image(50*j,50*i,image=self.dict[self.matrice[i][j]],anchor="nw")
              
    def get_case(self,perso):
        """renvoie la lettre de la case où est le perso"""
        return self.matrice[perso.y][perso.x]
        
    def get_case_droite(self,perso) :
        """renvoie la lettre de la case à droite du perso"""
        return self.matrice[perso.y][perso.x + 1]
    
    def get_case_gauche(self,perso) :
        """renvoie la lettre de la case à gauche du perso"""
        return self.matrice[perso.y][perso.x - 1]
    
    def get_case_bas(self,perso) :
        """renvoie la lettre de la case en dessous du perso"""
        return self.matrice[perso.y + 1][perso.x]
    
    def get_cases_interdites(self):
        """renvoie la liste des cases interdites"""
        return self.cases_interdites
    
    def ajoute_cases_interdites(self,lettre:str):
        """ajoute une case interdite""" 
        self.cases_interdites.append(lettre)
        
    def enleve_cases_interdites(self,lettre:str):
        """enleve une case interdite""" 
        while lettre in self.cases_interdites :
            self.cases_interdites.remove(lettre)
        
    def get_liste_perso(self):
        """renvoie la liste des persos dans le jeu"""
        return self.lemmings
        
    def ajoute_liste_perso(self,perso):
        """ajoute un perso dans la liste des persos"""
        self.lemmings.append(perso)
        
    def enleve_liste_perso(self,perso):
        """enlève un perso à la liste des persos"""
        del self.lemmings[self.lemmings.index(perso)]
    
    def get_matrice(self):
        """renvoie la matrice du jeu"""
        return self.matrice
    
    def get_dico(self):
        """renvoie le dico du jeu"""
        return self.dico  # type: ignore
    
    def set_canvas(self,can):
        """change le canvas du jeu"""
        self.canvas = can
        
    def set_matrice(self,matrice):
        """change la matrice du jeu"""
        self.matrice = matrice
        
    def set_dico(self,dico):
        """change le dictionnaire qui dessine la map"""
        self.dict = dico
        
    def changement_nature_case(self,perso):
        """change la case du perso de True à False ou de False à True"""
        self.matrice_bool[perso.y][perso.x] = not (self.matrice_bool[perso.y][perso.x])
    
    def get_nature_case(self,perso)->bool :
        """renvoie la nature de la case où est le perso"""
        return self.matrice_bool[perso.y][perso.x]
    
    def get_nature_case_droite(self,perso)->bool :
        """renvoie la nature de la case de droite du perso"""
        return self.matrice_bool[perso.y][perso.x + 1]
    
    def get_nature_case_gauche(self,perso)->bool :
        """renvoie la nature de la case de gauche du perso"""
        return self.matrice_bool[perso.y][perso.x - 1]
    
    def get_nature_case_dessous(self,perso)->bool :
        """renvoie la nature de la case en dessous du perso"""
        return self.matrice_bool[perso.y + 1][perso.x]
    
    def change_case(self,l,c,lettre):
        """change l'image de la case à la colonne c
        à la ligne l en fonction de la lettre
        change la lettre dans la matrice"""
        self.matrice[l][c] = lettre
        self.can.create_image(50*l,50*c,image=self.dict[lettre],anchor="nw")
              
       