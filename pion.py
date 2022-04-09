from math import sqrt
from PIL import ImageColor, Image, ImageTk

class Pion:
    def __init__(self,color,coef,name):
        self.color = color
        self.secondColor = delayColor(color)
        self.coef = coef
        self.name = name
    
    def findCoor(self,reelX,reelY,allCoor):
        #Permet de corriger l'imperfection de notre clic
        #distance entre deux points : sqrt((x1-x2)**2+(y1-y2)**2)
        minDist = 50
        bestCoor = -50,-50,0,0
        for coor in allCoor:
            dist = calculDist(reelX,reelY,coor[0],coor[1])
            if minDist > dist:
                minDist = dist
                bestCoor = coor
        
        self.x,self.y = bestCoor[0]-2,bestCoor[1]
        self.tabX,self.tabY = bestCoor[2],bestCoor[3]
    
    def findWithTab(self,tabX,tabY,allCoor):
        #trouve les coordonnées x,y en fonction de sa place dans le tableau
        for coor in allCoor:
            if coor[2] == tabX and coor[3] == tabY:
                return coor[0],coor[1]
        return None,None
        
    def isPossible(self,allPions,swap,allCoor):
        #Verifie que le joueur ne clic pas en dehors du plateau
        if self.x < 0 and self.y <0:
            return "False"

        #vérifie qu'il ne clique pas sur un autre Pion déjà placer (sauf si swap)
        for p in allPions:
            if p.tabX == self.tabX and p.tabY == self.tabY:
                if swap == 1 and len(allPions) == 1:
                    self.tabX,self.tabY = 10-self.tabX, 10-self.tabY
                    self.x,self.y = self.findWithTab(self.tabX,self.tabY,allCoor)
                    self.x -= 2
                    return "swap"
                return "False"
        return "True"
    
    def afficherPion(self,surface,color):
        s = self.coef
        self.marque = surface.create_polygon(self.x-sqrt(3)/2*s,self.y-0.5*s,
                                self.x,self.y-s,
                                self.x+sqrt(3)/2*s,self.y-0.5*s,
                                self.x+sqrt(3)/2*s,self.y+0.5*s,
                                self.x,self.y+s,
                                self.x-sqrt(3)/2*s,self.y+0.5*s,
                                fill = color,outline = "black")
    
    def previewPion(self,surface,color,backColor):
        s = self.coef-3
        self.marque = surface.create_polygon(self.x-sqrt(3)/2*s,self.y-0.5*s,
                                self.x,self.y-s,
                                self.x+sqrt(3)/2*s,self.y-0.5*s,
                                self.x+sqrt(3)/2*s,self.y+0.5*s,
                                self.x,self.y+s,
                                self.x-sqrt(3)/2*s,self.y+0.5*s,
                                width=7,outline = color,fill=backColor)

def afficherImage(surface,x,y):
    img = ImageTk.PhotoImage(file='photo/starsH.png') #transparent image
    surface.create_image(x,y,image=img,anchor='ne') 
    print("je l'ai fait")
    
def calculDist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
    
def delayColor(color):
    rgb = ImageColor.getrgb(color)
    delayedColor = (int(rgb[0]*0.8),int(rgb[1]*0.8),int(rgb[2]*0.8))
    return "#"+rgb_to_hex(delayedColor)


    