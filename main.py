from tkinter import*
import tkinter
from tkinter import messagebox
import webbrowser
import time

from random import choice, randint
from board import*
from pion import*
from joueur import*

class Plateau(Tk):

    def __init__(self):
        #couleurs
        self.bgColor = "#F5F5F5"
        self.dicolor = {"Rouge":"#FF0005","Orange":"#F28705","Jaune":"#FFE129","Bleu":"#003F63","Rose":"#F2A0B6","Violet":"#A066F2",
                        "Noir" : "#000000","#8191DD":"#8191DD","Invisible":self.bgColor,"Chocolat": "#d2691e","Kakhi Foncé":"#bdb76b",
                        "Multicolor":"#000001"}

        self.unlockableColor = ["Noir","Invisible","#8191DD","Chocolat","Kakhi Foncé","Multicolor"]

        #initialisation
        super().__init__()
        self.geometry('900x400')
        self.configure(bg=self.bgColor)
        self.title("HEX ÆCO")
        self.iconbitmap("logo3.ico")
        self.resizable(False, False)

        #variables
        self.fauxPion = Pion(self.bgColor,17,0)
        self.fauxPion.marque = None
        self.game = False
        self.whoPlay = 12

        #Frame
        self.frame = Frame(self,bg = self.bgColor)
        self.frame.pack()

        #Canvas
        self.canvas = Canvas(self.frame,width = 550, height = 350, bg = self.bgColor)
        self.canvas.grid(column = 0, row = 0,columnspan = 3,rowspan = 6,padx=5,pady=5)

        #bouton des règles
        #self.regle = Button(self.frame,text="Les règles",command = lambda: self.boutonReprendre())
        self.regle = Button(self.frame,text="Les règles",command = lambda: webbrowser.open_new("www.hexwiki.net/index.php/Rules"))
        self.regle.grid(column =4, row =6)

        #Bouton quitter
        self.quitter = Button(self.frame,text = "Quitter",command = quit)
        self.quitter.grid(column = 5, row = 6)

        #Bouton sauvegarder/Reprendre
        self.save = Button(self.frame,text="Reprendre",state = ACTIVE,command = lambda:self.boutonReprendre())
        self.save.grid(column = 0, row = 6)

        #Bouton Jouer
        self.play = Button(self.frame,text="Jouer",padx = 10,command=lambda:self.boutonPlay())
        self.play.grid(column=1,row = 6)

        #Bouton Recommencer
        self.reco = Button(self.frame,text="Recommencer",state = DISABLED,command = lambda:self.boutonReco())
        self.reco.grid(column=2,row=6)

        #Zone pour déterminer qui commence
        self.varStart = IntVar()
        self.zoneOption = LabelFrame(self.frame,text="Option :",bg = self.bgColor)
        self.zoneOption.grid(column = 3, row = 2,columnspan = 3)
        Label(self.zoneOption,text="Qui commence ? : ",bg=self.bgColor).grid(column=0,row=0,padx=5)
        Radiobutton(self.zoneOption, text='Joueur 1', variable=self.varStart, value=0,bg=self.bgColor).grid(row=0, column=1)
        Radiobutton(self.zoneOption, text="Joueur 2", variable=self.varStart, value=1,bg=self.bgColor).grid(row=0, column=2)
        Radiobutton(self.zoneOption, text="Aléa", variable=self.varStart, value=2,bg=self.bgColor).grid(row=0, column = 3)
        self.varStart.set(2)

        #Zone pour savoir si on introduit le 'swap'
        self.isSwap = IntVar()
        Label(self.zoneOption, text="Option de jeu : ",bg = self.bgColor).grid(column = 0,row =1)
        checkSwap = Checkbutton(self.zoneOption,text = "Swap",variable = self.isSwap,onvalue=1, offvalue=0,bg= self.bgColor)
        checkSwap.grid(column = 1,row=1)
        Label(self.zoneOption,text="Temps : ",bg = self.bgColor).grid(row=1,column=2)
        self.varTemps = IntVar()
        self.varTemps.set(300)
        self.spinTime = Spinbox(self.zoneOption,from_=60,to_=900,width = 5, increment=60, textvariable=self.varTemps)
        self.spinTime.grid(row = 1, column = 3)

        #Joueur 1 (name, couleur, chrono)
        self.zoneJ1 = LabelFrame(self.frame,text="joueur 1",bg= self.bgColor)
        self.zoneJ1.grid(column = 3,columnspan = 3,row = 0)
        Label(self.zoneJ1,text="Pseudo 1 : ").grid(row = 0,column=0,padx=5)
        self.pseudo1 = Entry(self.zoneJ1,width = 15)
        self.pseudo1.insert(0,"Mattchau")
        self.pseudo1.grid(column=1,row=0)
        self.chrono1 = Label(self.zoneJ1,text = "temps : 000",bg = "white",fg="black",relief="solid",bd=1,width=10)
        self.chrono1.grid(column = 2 ,row = 0)

        self.choice1 = ["Rouge","Orange","Jaune"]
        self.variable1 = StringVar(self.zoneJ1)
        self.variable1.set("Rouge")
        self.colorChoice1 = OptionMenu(self.zoneJ1,self.variable1,*self.choice1,command = lambda event: self.updatePreview(1))
        Label(self.zoneJ1, text = "Couleur :").grid(row = 1,column = 0)
        self.colorChoice1.grid(row = 1, column=1)
        self.preview1 = Canvas(self.zoneJ1, width = 40, height = 40, bg = self.dicolor[self.variable1.get()])
        self.preview1.grid(column = 2, row = 1, padx = 50, pady = 20)

        #Joueur 2 (name, couleur)
        self.zoneJ2 = LabelFrame(self.frame,text = "joueur 2",bg = self.bgColor)
        self.zoneJ2.grid(column = 3, columnspan=3,row = 4)
        Label(self.zoneJ2,text="Pseudo 2 : ").grid(row = 0,column=0,padx = 5)
        self.pseudo2 = Entry(self.zoneJ2,width = 15)
        self.pseudo2.insert(0,"Nicoloc")
        self.pseudo2.grid(column=1,row=0)
        self.chrono2 = Label(self.zoneJ2,text = "temps : 000",bg = "white",fg="black",relief="solid",bd=1,width=10)
        self.chrono2.grid(column = 2 ,row = 0)


        self.choice2 = ["Bleu","Rose","Violet"]
        self.variable2 = StringVar(self.zoneJ2)
        self.variable2.set("Bleu")
        self.colorChoice2 = OptionMenu(self.zoneJ2,self.variable2,*self.choice2,command = lambda event: self.updatePreview(2))
        Label(self.zoneJ2, text = "Couleur :").grid(row = 1,column = 0)
        self.colorChoice2.grid(row = 1, column=1)
        self.preview2 = Canvas(self.zoneJ2, width = 40, height = 40, bg = self.dicolor[self.variable2.get()])
        self.preview2.grid(column = 2, row = 1, padx = 50, pady = 20)

        self.canvas.bind("<Motion>",self.survol)
        self.canvas.bind("<Button-1>",self.souris)
        self.bind("<Button-3>",self.clicDroit)
    
    def actuMultiColor(self):
        for j in self.joueurs:
            if j.color == "#000001":
                self.newColor = choice(list(self.dicolor.items()))
                if self.joueurs.index(j)==1:
                    self.preview2["bg"] = self.newColor[1]
                else:
                    self.preview1["bg"] = self.newColor[1]
                
                for marque in self.grille.bordMulticolor:
                    self.canvas.itemconfig(marque, fill=self.newColor[1])
                for p in self.allPions:
                    if p.color == "#000001": #le pion est multicolor
                        p.afficherPion(self.canvas,self.newColor[1])
    
    def actuChrono(self):
        if self.defaite():
            return self.victoire()
        if self.game:
            self.actuMultiColor()
            self.joueurs[self.whoPlay].time -= 1
            if self.whoPlay == 0:
                self.chrono1['text'] = f"temps : {self.joueurs[self.whoPlay].time}"
            elif self.whoPlay == 1:
                self.chrono2['text'] = f"temps : {self.joueurs[self.whoPlay].time}"
            self.after(1000, self.actuChrono)
    
    def clicDroit(self,event):
        self.victoire()
    
    def survol(self,event):
        if self.game:
            #La fonction survol créer en permanance un nouveau pion s'il peut être posé et est supprimé ensuite
            actualJ = self.joueurs[self.whoPlay]
            if actualJ.color == "#000001":
                color = self.newColor[1]
            else:
                color = actualJ.color

            testPion = Pion(color,17,actualJ.id)
            testPion.findCoor(event.x,event.y,self.grille.allCoor)

            self.canvas.delete(self.fauxPion.marque)
            placer = testPion.isPossible(self.allPions,False,None)
            if placer == "True":
                self.fauxPion = Pion(color,17,actualJ.id)
                self.fauxPion.findCoor(event.x,event.y,self.grille.allCoor)
                self.fauxPion.previewPion(self.canvas,testPion.color,self.bgColor)
            else:
                self.fauxPion = Pion(self.bgColor,17,0)
                self.fauxPion.marque = None


    def souris(self,event):
        if self.game:
            actualJ = self.joueurs[self.whoPlay]
            color = actualJ.color

            p = Pion(color,17,actualJ.id)
            p.findCoor(event.x,event.y,self.grille.allCoor)
            
            placer = p.isPossible(self.allPions,self.swap,self.grille.allCoor)
            if placer == "swap":
                """
                Le deuxième joueur à cliquer sur le seul pion --> swap
                L'ancien Pion est :
                    - supprimé de la liste de pion
                    - supprimé du tableau de la grille
                    - sa marque sur le pavage est supprimé
                On ajoute le nouveau pion de manière classique
                """
                self.swap = False
                ancienPion = self.allPions[0]
                self.canvas.delete(ancienPion.marque)
                self.grille.board[ancienPion.tabY][ancienPion.tabX] = 0
                self.allPions = [p]
                self.grille.fillTab(p.tabX,p.tabY,p.name)
                p.afficherPion(self.canvas,p.secondColor)
                self.whoPlay = abs(self.whoPlay-1)
                self.ligne1["text"] = f"C'est à {self.joueurs[self.whoPlay].name}"

            elif placer == "True":
                #Le dernier pion est modifié (s'il existe) et qu'il n'est pas multicolor
                if len(self.allPions)>0:
                    dernierPion = self.allPions[-1]
                    if dernierPion.color != "#000001":
                        dernierPion.afficherPion(self.canvas,dernierPion.color)
                if p.color != "#000001":
                    p.afficherPion(self.canvas,p.secondColor)
                else:
                    p.afficherPion(self.canvas,self.newColor[1])
                if self.grille.isVictory(p.tabX,p.tabY,p.name,[],[False,False]):
                    self.victoire()
                else:
                    self.grille.fillTab(p.tabX,p.tabY,p.name)
                    #self.grille.printBoard()
                    self.allPions.append(p)
                    self.whoPlay = abs(self.whoPlay-1)
                    self.ligne1["text"] = f"C'est à {self.joueurs[self.whoPlay].name}"

    #Toutes les Fonction pour les boutons
    def updatePreview(self,nb):
        if nb == 1:
            self.preview1["bg"] = self.dicolor[self.variable1.get()]
        else:
            self.preview2["bg"] = self.dicolor[self.variable2.get()]
    
    def boutonSave(self):
        with open('SavedGame','w') as file:
            #On écrit les joueurs
            for j in self.joueurs:
                s = j.__str__()
                file.write(s+";")
            file.write(str(self.whoPlay))
            
            #On écrit les pions
            for p in self.allPions:
                txt = f"\n{p.x};{p.y};{p.color};{p.tabX};{p.tabY};{p.name}"
                file.write(txt)
    
    def boutonReprendre(self):
        #reprise des informations du documents texte
        liste = []
        with open('SavedGame', 'r') as doss:
            lmots=doss.readlines()
        for mot in lmots:
            mo = mot[0:-1].split(";")
            liste.append(mo)   

        #recéreation des joueurs
        j1 = Player(liste[0][0],liste[0][1],int(liste[0][2]),0,0)
        j2 = Player(liste[0][3],liste[0][4],int(liste[0][5]),0,0)
        self.joueurs = [j1,j2]

        self.whoPlay = int(liste[0][6])
        
        #recréations de la grille
        self.allPions = []
        self.grille = Grille(j1.color,j2.color,self.bgColor,combine_hex_values([j1.color,j2.color]),0,5,17)
        self.grille.afficherGrille(game.canvas)
        self.grille.afficherCoor(game.canvas)

        #recréation des pions
        for info in liste[1:-1]:
            p = Pion(info[2],17,int(info[5]))
            p.x,p.y = float(info[0]),float(info[1])
            p.tabX,p.tabY = int(info[3]),int(info[4])

            self.grille.fillTab(p.tabX,p.tabY,p.name)
            p.afficherPion(self.canvas,p.color)
            self.allPions.append(p)

        #Reprise d'une parti normal avec les attibuts
        self.game = True
        self.play['state'] = DISABLED
        self.reco['state'] = ACTIVE
        self.save['text'] = "Sauvegarder"
        self.save["command"] = lambda: self.boutonSave()
        self.zoneOption.destroy()

        self.pseudo1.destroy()
        self.labelName1 = Label(self.zoneJ1,text=j1.name,bg=self.bgColor)
        self.labelName1.grid(column=1,row=0)
        self.pseudo2.destroy()
        self.labelName2 = Label(self.zoneJ2,text=j2.name,bg=self.bgColor,justify=LEFT)
        self.labelName2.grid(column=1,columnspan=2,row=0)

        #message à afficher
        self.ligne1 = Label(self.frame,text=f"C'est à {self.joueurs[self.whoPlay].name}",bg=self.bgColor)
        self.ligne1.grid(column=3,row = 2,columnspan=4)
        self.ligne2 = Label(self.frame,text="de jouer",bg=self.bgColor)
        self.ligne2.grid(column =3, row = 3,columnspan=4)

        self.colorChoice1.configure(state="disabled")
        self.colorChoice2.configure(state="disabled")
        self.preview1["bg"] = j1.color
        self.preview2["bg"] = j2.color
        
    def boutonPlay(self):
        self.game = True

        self.totalTime = self.varTemps.get()
        self.timeStart = time.time()
        self.after(1000, self.actuChrono)

        self.play['state'] = DISABLED
        self.reco['state'] = ACTIVE
        self.save['text'] = "Sauvegarder"
        self.save["command"] = lambda: self.boutonSave()
        self.swap = self.isSwap.get() 
        self.whoPlay = self.varStart.get()
        if self.whoPlay == 2:
            self.whoPlay = randint(0,1)
        self.zoneOption.grid_remove()

        j1 = Player(self.pseudo1.get(),self.dicolor[self.variable1.get()],1,self.totalTime)
        j2 = Player(self.pseudo2.get(),self.dicolor[self.variable2.get()],2,self.totalTime)
        self.joueurs = [j1,j2]

        #On afficher correctement les prénom
        self.pseudo1.destroy()
        self.labelName1 = Label(self.zoneJ1,text=j1.name,bg=self.bgColor)
        self.labelName1.grid(column=1,row=0)
        self.pseudo2.destroy()
        self.labelName2 = Label(self.zoneJ2,text=j2.name,bg=self.bgColor,justify=LEFT)
        self.labelName2.grid(column=1,row=0)
        self.chrono1['text'] = f"temps : {str(j1.time)}"
        self.chrono2['text'] = f"temps : {str(j2.time)}"

        #message à afficher
        self.ligne1 = Label(self.frame,text=f"C'est à {self.joueurs[self.whoPlay].name}",bg=self.bgColor)
        self.ligne1.grid(column=3,row = 2,columnspan=4)
        self.ligne2 = Label(self.frame,text="de jouer",bg=self.bgColor)
        self.ligne2.grid(column =3, row = 3,columnspan=4)

        self.colorChoice1.configure(state="disabled")
        self.colorChoice2.configure(state="disabled")

        self.allPions = []
        self.grille = Grille(j1.color,j2.color,self.bgColor,combine_hex_values([j1.color,j2.color]),0,5,17)
        self.grille.afficherGrille(game.canvas)
        self.grille.afficherCoor(game.canvas)
    
    def defaite(self):
        if self.joueurs[self.whoPlay].time <=0:
            self.whoPlay = abs(self.whoPlay -1)
            return True
        return False
    
    def victoire(self):
        self.game = False
        gagnant = self.joueurs[self.whoPlay]
        unlockColor = choice(self.unlockableColor)
        self.unlockableColor.remove(unlockColor)
        self.ligne1['text'] = f"Félicitation {gagnant.name} a gagné la partie."
        self.ligne2['text'] = f"{gagnant.name} débloque la couleur {unlockColor}"

        if self.whoPlay == 0:
            self.colorChoice1['menu'].add_command(label=unlockColor, command=tkinter._setit(self.variable1,unlockColor, lambda cv=self.variable1, con=unlockColor: self.updatePreview(1)))
        else:
            self.colorChoice2['menu'].add_command(label=unlockColor, command=tkinter._setit(self.variable2, unlockColor, lambda cv=self.variable2, con=unlockColor: self.updatePreview(2)))

    def boutonReco(self):
        self.game = False
        self.play['state'] = ACTIVE
        self.reco['state'] = DISABLED
        self.save['text'] = "Reprendre"
        self.save['command'] = lambda : self.boutonReprendre()

        self.ligne1.destroy()
        self.ligne2.destroy()
        self.labelName1.destroy()
        self.labelName2.destroy()
        self.zoneOption.grid()
        
        self.pseudo1 = Entry(self.zoneJ1,width = 15)
        self.pseudo1.insert(0,self.joueurs[0].name)
        self.pseudo1.grid(column=1,row=0)
        self.chrono1['text'] = "temps : 000"

        self.pseudo2 = Entry(self.zoneJ2,width = 15)
        self.pseudo2.insert(0,self.joueurs[1].name)
        self.pseudo2.grid(column=1,row=0)
        self.chrono2['text'] = "temps : 000"

        self.colorChoice1.configure(state="active")
        self.colorChoice2.configure(state="active")

        fg = Grille(self.bgColor,self.bgColor,self.bgColor,self.bgColor,0,5,17)
        fg.afficherGrille(self.canvas)
        fg.afficherCoor(self.canvas)

        self.fauxPion = Pion(self.bgColor,17,0)
        self.fauxPion.marque = None

def combine_hex_values(d):
    red = int(sum([int(k[1:3], 16) for k in d])/2)
    green = int(sum([int(k[3:5], 16) for k in d])/2)
    blue = int(sum([int(k[5:7], 16) for k  in d])/2)
    zpad = lambda x: x if len(x)==2 else '0' + x
    return "#" + zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])

def transparancyHexValue(color):
    return "#1C"+color[1:]

if __name__ =="__main__":
    regleWiki = "Les joueurs possèdent des pions à leur couleur qu'ils disposent tour à tour sur une case de leur choix et un par un. Le tablier se remplit ainsi progressivement. L'objectif d'un joueur, par exemple Bleu, est de relier les deux côtés opposés du losange symbolisés par la couleur bleue. Si la configuration des pions bleus permet la création d'une ligne continue (en blanc sur la figure) reliant un côté bleu à l'autre, Bleu a gagné et le jeu s'arrête. Plus d'info sur : https://fr.wikipedia.org/wiki/Hex"
    game = Plateau()
    fg = Grille(game.bgColor,game.bgColor,game.bgColor,game.bgColor,0,5,17)
    fg.afficherGrille(game.canvas)
    fg.afficherCoor(game.canvas)
    game.mainloop()