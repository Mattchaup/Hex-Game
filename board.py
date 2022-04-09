from tkinter import*
from math import sqrt

class Grille:
    def __init__(self,color1,color2,defaultColor,cornerColor,offX,offY,coef):
        self.color1 = color1
        self.color2 = color2
        self.defC = defaultColor
        self.cornerColor = cornerColor
        self.offX = offX
        self.offY = offY
        self.coef = coef
        self.allCoor = []
        self.board = [[0 for i in range(11)]for j in range(11)]
        self.bordMulticolor = []

    def afficherGrille(self,surface):
        #offsetx, offset y , coef
        x = self.offX
        y = self.offY
        s = self.coef

        for j in range(13):
            for i in range(13):
                color = self.defC
                if (i == 0 and j ==0) or (i ==12 and j == 12):
                    pass
                else:
                    if (i==0 and j==12) or (i==12 and j ==0):
                        color = self.cornerColor
                    elif j == 0 or j == 12:
                        color = self.color1
                    elif i == 0 or i == 12:
                        color = self.color2
                    else:
                        self.allCoor.append((x+i*sqrt(3)*s+s,y+s+(j*s*1.5),i-1,j-1))
                    marque = surface.create_polygon( x+(i*sqrt(3)*s),y+0.5*s+(j*s*1.5),
                                            x+sqrt(3)/2*s+(i*sqrt(3)*s),y+(j*s*1.5),
                                            x+sqrt(3)*s+(i*sqrt(3)*s),y+0.5*s+(j*s*1.5),
                                            x+sqrt(3)*s+(i*sqrt(3)*s),y+1.5*s+(j*s*1.5),
                                            x+sqrt(3)/2*s+(i*sqrt(3)*s),y+2*s+(j*s*1.5),
                                            x+(i*sqrt(3)*s),y+1.5*s+(j*s*1.5),
                                            outline = 'black',fill = color)

                    if color == "#000001": #Le bord est Multicolor
                        self.bordMulticolor.append(marque)
            x+=sqrt(3)/2*s
    
    def afficherCoor(self,surface):
        x = self.offX
        y = self.offY
        s = self.coef

        lettre = ["A","B","C","D","E","F","G","H","I","J","K"]
        nbr = [str(i) for i in range(1,12)]

        for i in range(len(lettre)):
            surface.create_text(sqrt(3)/2*s+sqrt(3)*s*(i+1),y+s,text=lettre[i],fill = self.defC)
            surface.create_text(sqrt(3)/2*s+5*sqrt(3)*s+sqrt(3)*s*(i+2),y+19*s,text=lettre[i],fill = self.defC)
        
        for j in range(len(nbr)):
            surface.create_text(x+sqrt(3)*s+sqrt(3)/2*j*s,y+2.5*s+j*1.5*s,text=nbr[j],fill= self.defC)
            surface.create_text(x+13*sqrt(3)*s+sqrt(3)/2*j*s,y+2.5*s+j*1.5*s,text=nbr[j],fill= self.defC)

    def printBoard(self):
        print("------------------------------------")
        for ligne in self.board:
            print(ligne)
    
    def fillTab(self,x,y,name):
        self.board[y][x] = name
    
    def isTouching(self,x,y,name):
        """
        Dans le schéma suivant, les 2 sont les cases adjacentes au 1.
        [0, 0, 2, 2, 0]
        [0, 2, 1, 2, 0]
        [0, 2, 2, 0, 0]
        """
        allTouch = []
        if y > 0:
            if self.board[y-1][x] == name:
                allTouch.append((x,y-1))
            if x < 10:
                if self.board[y-1][x+1] == name:
                    allTouch.append((x+1,y-1))
        if y < 10:
            if self.board[y+1][x] == name:
                allTouch.append((x,y+1))
            if x > 0:
                if self.board[y+1][x-1] == name:
                    allTouch.append((x-1,y+1))
        if x < 10:
            if self.board[y][x+1] == name:
                allTouch.append((x+1,y))
        if x > 0:
            if self.board[y][x-1] == name:
                allTouch.append((x-1,y))
        return allTouch
    
    def dejaVisite(self,allVisite,x,y):
        #On vérifie que ne visite pas une case qu'on a déjà visité avant
        for coor in allVisite:
            if coor[0] == x and coor[1] == y:
                return True
        return False
    
    def gererListe(self,allVisite,liste):
        listeGerer = []
        for coor in liste:
            if not self.dejaVisite(allVisite,coor[0],coor[1]):
                listeGerer.append(coor)
        return listeGerer
        
    def isVictory(self,x,y,name,allVisite,condition):
        if name == 1:
            if y == 0:
                condition[0] = True
            if y == 10:
                condition[1] = True
        elif name == 2:
            if x == 0:
                condition[0] = True
            if x == 10:
                condition[1] = True

        allVisite.append((x,y))
        liste = self.isTouching(x,y,name)
        liste = self.gererListe(allVisite,liste)

        for coor in liste:
            self.isVictory(coor[0],coor[1],name,allVisite,condition)

        if condition == [True,True]:#Il y a une victoire
            return True
        return False