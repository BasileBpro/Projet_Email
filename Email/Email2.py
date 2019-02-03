from tkinter import *
import requests
import os
from bs4 import BeautifulSoup
import csv
import smtplib
from email.mime.text import MIMEText as text
import email.utils
import threading

#Lecture fichier
global ValueCSVBis
global namefichier
global fichierDepart
ValueCSVBis = ""
global Ress
Ress = ""
def Read_File(namefile):
    global namefichier
    namefichier = namefile
    try:
        my_file = open(namefile, "r")
        infos = my_file.read()
        print("Le fichier a été ouvert")
        my_file.close()
    except:
        my_file = open(namefile, "w+")
        my_file.close()
        infos = ""
        print("Le fichier " + namefile + " a été créé")

    return infos

def Write_File(namefile, text):
    global namefichier
    namefichier = namefile
    my_file = open(namefile, "a")
    my_file.write(text)
    my_file.close()

def Write_File_Final(namefile, text):
    global namefichier
    namefichier = namefile
    my_file = open(namefile, "w")
    my_file.write(text)
    my_file.close()

def Verif_Mail(name_Mail):
    #VERIFICATION DU MAIL
    if( "@" in name_Mail and (name_Mail.endswith(".com") or name_Mail.endswith(".fr"))):
        return True
    else:
        return False

def Verif_URL(name_URL):
    #VERIFIE L URL ENTRE
   if("http://" in name_URL or "https://" in name_URL):
       hostname = "ping" + name_URL
       if(os.system(hostname) == 0):
           return True
       else:
           return False
   else:
       return False
def ping_URL(name_URL):
    #PING L URL
    domaine = Recup_Domaine(name_URL)
    domaine_finale = "ping " + domaine
    if (os.system(domaine_finale) == 0):
        return True
    else:
        return False

def Recup_Domaine(name_URL):
    infos = name_URL.split("@")
    return infos[1]

def Recup_List_Mail(File_Name):
    #RECUPERE LES MAILS D UN FICHIER
    global namefichier
    f = open(File_Name, "r")
    lignes = f.readlines()
    f.close()
    list_True = []
    for ligne in lignes:
        list_True.append(ligne)
        #Write_File(namefichier, ligne + "\n")
    return list_True

def Verif_List_Mail(liste1, liste):
    #VERIFIE LES MAILS DE LA LISTE
    global Ress
    listeTempo = []
    """f = open(File_Name, "r")
    lignes = f.readlines()
    f.close()
    list_True = []
    for ligne in lignes:
        if(Verif_Mail(ligne.rstrip())== True):
            list_True.append(ligne)
    return list_True"""
    liste.delete(0, END)
    for i in range(0, len(liste1)):
        if(Verif_Mail(liste1[i].rstrip())==True):
            listeTempo.append(liste1[i])
            liste.insert(i, liste1[i])
    Ress = listeTempo
    return None

def Suppr_Doublons(liste1, liste):
    #SUPPRIME LES DOUBLONS DE LA LISTE EN VIDANT LA LISTBOX ET EN REMETTANT LES VALEURS APRES LE TRI
    global Ress
    liste_sans = set(liste1)
    liste_sans = list(liste_sans)
    liste.delete(0, END)
    for i in range (0,len(liste_sans)):
        liste.insert(i, liste_sans[i])
    Ress = liste_sans
    return liste_sans

def Recup_ListBox(listeBoxAtm):
    #RECUPERATION DE LA LISTEBOX
    listActuelle = []
    for i in range(0,listeBoxAtm.size()):
        listActuelle.append(listeBoxAtm.get(i))
    return listActuelle

def ImportationCSV(NameCSVBis):
    #IMPORTATION D UN FICHIER CSV AVEC OUVERTURE DE LA FENETRE 2
    Fenetre2(NameCSVBis, False)

def ImportationURL(NameURLBis):
    #IMPORTATION DE MAIL A PARTIR D UN SITE WEB ET OUVERTURE DE LA FENETRE 2
    Url = Crawler(NameURLBis)
    Fenetre2(Url, False)

def Crawler(URL):
    #PERMET DE RECUPERER LES ADRESSES MAILS CONTENUS DANS LE HREF ET STOCK DANS UN FICHIER EPEHEMERE
    """requete = requests.get("http://univcergy.phpnet.org/python/mail.html")"""
    requete = requests.get(URL)
    page = requete.content
    soup = BeautifulSoup(page, features="html.parser")
    Write_File_Final("StockageMailUrl.txt", "")
    for link in soup.find_all('a', href=True):
        if("mailto" in link['href']):
            mail = str(link['href'])
            finalmail = mail.split(":")
            Write_File("StockageMailUrl.txt", finalmail[1] + "\n")
    finalmail = "StockageMailUrl.txt"
    return finalmail

def SupprMail():
    #SUPPRIME L ELEMENT SELECTIONNE
    global liste
    global Ress
    line = liste.curselection()[0]
    del Ress[line]
    liste.delete(line)

def ThreadMail(Expe, MyMail, Object, MyPass, MyMessage, HisMail):
    #CREATION D UN THREAD POUR L ENVOI DES MAILS
    threading.Thread(target=Envoi_Mail, args=(Expe, MyMail, Object, MyPass, MyMessage, HisMail)).start()


def Envoi_Mail(Expe, MyMail, Object, MyPass, MyMessage, HisMail):
    global Ress
    ResultatMail = ""
    global fichierDepart
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(MyMail, MyPass)
    msg = text(MyMessage)
    #CHANGEMENT DE L EXPEDITEUR
    msg['From'] = email.utils.formataddr((Expe,'test'))
    #CHANGEMENT DE L OBJET
    msg['Subject'] = Object
    for i in range(0, len(Ress)):
        ResultatMail = ResultatMail + Ress[i]
    #SAUVEGARDE DU FICHIER AVEC LES NOUVEAUX MAILS AJOUTES
    Write_File_Final(fichierDepart, ResultatMail)

    #ENVOI D UN MAIL TEST
    if HisMail != "":
        server.sendmail(MyMail, HisMail, msg.as_string())
    #ENVOI A UNE LISTE DE MAIL
    else:
        for i in range(0, len(Ress)):
            server.sendmail(MyMail, Ress[i], msg.as_string())
    server.quit()

def Fenetre2(NameCampagne, first):
    #CREATION DE LA FENETRE ET VERIFICATION DE SI L ON PROVIENT DE LA PAGE 1 OU NON
    global namecsv
    namecsv = NameCampagne
    global fichierDepart
    if(first==True):
        Write_File(NameCampagne, ValueCSVBis)
        fichierDepart = NameCampagne
    try:
        fenetre.destroy()
    except:
        print("Fenetre already down")
    try:
        fenetre4.destroy()
    except:
        print("Fenetre 4 already down")
    try:
        fenetre5.destroy()
    except:
        print("Fenetre 5 already down")
    # CREATION DE LA FENETRE TABLEAU
    global fenetre2
    global liste
    global Ress

    fenetre2 = Tk()
    fenetre2.title("Tableau")

    # PARAMETRE DE LA FENETRE2
    fenetre2.geometry("500x600")


    Ress = list(Ress) + Recup_List_Mail(NameCampagne)

    # BOUTONS
    Dedoublonner = Button(fenetre2, text="Dedoublonner", font="Arial 14", command=lambda: Suppr_Doublons(Recup_ListBox(liste), liste))
    Dedoublonner.place(relx=0.3, rely=0.2, anchor=CENTER, height=30, width=120)
    Verif = Button(fenetre2, text="Verification", font="Arial 14", command=lambda: Verif_List_Mail(Recup_ListBox(liste), liste))
    Verif.place(relx=0.7, rely=0.2, anchor=CENTER, height=30, width=120)
    ImportCSV = Button(fenetre2, text="Import CSV", font="Arial 14", command=Fenetre4)
    ImportCSV.place(relx=0.3, rely=0.4, anchor=CENTER, height=30, width=120)
    ImportURL = Button(fenetre2, text="Import URL", font="Arial 14", command=Fenetre5)
    ImportURL.place(relx=0.7, rely=0.4, anchor=CENTER, height=30, width=120)

    ButtonSuppr = Button(fenetre2, text="Supprimer Mail", font="Arial 14", command=SupprMail)
    ButtonSuppr.place(relx=0.82, rely=0.7, anchor=CENTER, height=30, width=150)

    value = "Valide"
    valuebis = "Non Valide"
    liste = Listbox(fenetre2)
    for start in range(0, len(Ress)):
        liste.insert(start, Ress[start])
    liste.place(relx=0.4, rely=0.6, anchor=CENTER, height=150, width=250)
    Ok0 = Button(fenetre2, text="Ok", font="Arial 14", command=Fenetre3)
    Ok0.place(relx=0.8, rely=0.9, anchor=CENTER, height=20, width=40)


def Fenetre3():
    fenetre2.destroy()
    #CREATION DE LA FENETRE MAIL
    global fenetre3
    fenetre3 = Tk()
    fenetre3.title("Mail")

    #PARAMETRE DE LA FENETRE3
    fenetre3.geometry("400x500")

    #LABELS
    Exp = Label(fenetre3, text="Exp", font="Arial 16")
    Exp.place(relx =0.2, rely = 0.2, anchor=CENTER)
    Obj = Label(fenetre3, text="Obj", font="Arial 16")
    Obj.place(relx =0.2, rely = 0.4, anchor=CENTER)
    Msg = Label(fenetre3, text="Msg", font="Arial 16")
    Msg.place(relx =0.2, rely = 0.6, anchor=CENTER)
    ExpText = Entry(fenetre3)
    ExpText.place(relx=0.5, rely=0.2, anchor=CENTER,height = 35, width=150)
    ObjText = Entry(fenetre3)
    ObjText.place(relx=0.5, rely=0.4, anchor=CENTER,height = 35, width=150)
    MsgText = Entry(fenetre3)
    MsgText.place(relx=0.5, rely=0.6, anchor=CENTER,height = 200, width=150)
    Ok1 = Button(fenetre3, text="Ok", font="Arial 16", command=lambda: Fenetre6(ExpText.get(), ObjText.get(), MsgText.get()))
    Ok1.place(relx=0.8, rely=0.9, anchor=CENTER, height = 20, width=40)

def Fenetre4():
    fenetre2.destroy()
    # CREATION DE LA FENETRE IMPORT CSV
    global fenetre4
    fenetre4 = Tk()
    fenetre4.title("Import CSV")

    # PARAMETRES DE LA FENETRE4
    fenetre4.geometry("400x400")

    # LABELS
    ImportCSVText = Label(fenetre4, text="Import csv", font="Arial 16")
    ImportCSVText.place(relx=0.5, rely=0.3, anchor=CENTER)
    ImportCSVButton = Entry(fenetre4)
    ImportCSVButton.place(relx=0.4, rely=0.6, anchor=CENTER)
    Ok2 = Button(fenetre4, text="Ok", font="Arial 16", command=lambda: ImportationCSV(ImportCSVButton.get()))
    Ok2.place(relx=0.7, rely=0.6, anchor=CENTER)

def Fenetre5():
    fenetre2.destroy()
    # CREATION DE LA FENETRE IMPORT URL
    global fenetre5
    fenetre5 = Tk()
    fenetre5.title("Import URL")

    # PARAMETRES DE LA FENETRE5
    fenetre5.geometry("400x400")

    # LABELS
    ImportURLText = Label(fenetre5, text="Import url", font="Arial 16")
    ImportURLText.place(relx=0.5, rely=0.3, anchor=CENTER)
    ImportURLButton = Entry(fenetre5)
    ImportURLButton.place(relx=0.4, rely=0.6, anchor=CENTER)
    Ok3 = Button(fenetre5, text="Ok", font="Arial 16", command=lambda: ImportationURL(ImportURLButton.get()))
    Ok3.place(relx=0.7, rely=0.6, anchor=CENTER)

def Fenetre6(Expe, Obj, Msg):
    fenetre3.destroy()
    # CREATION DE LA FENETRE TEST MAIL
    fenetre6 = Tk()
    fenetre6.title("Test Mail")

    # PARAMETRES DE LA FENETRE
    fenetre6.geometry("400x500")
    # LABELS
    Mail = Label(fenetre6, text="Mail", font="Arial 16")
    Mail.place(relx=0.2, rely=0.2, anchor=CENTER)
    MailText = Entry(fenetre6)
    MailText.place(relx=0.5, rely=0.2, anchor=CENTER, width=150, height=35)
    Test = Label(fenetre6, text="Test", font="Arial 16")
    Test.place(relx=0.2, rely=0.4, anchor=CENTER)
    TestButton = Button(fenetre6, text="Test Envoi", font="Arial 16", command=lambda: ThreadMail(Expe, "testpythonmailexo@gmail.com",Obj,"testpythonexo", Msg, MailText.get()))
    TestButton.place(relx=0.5, rely=0.4, anchor=CENTER)
    SendList = Button(fenetre6, text="Envoi à la liste", font="Arial 16", command=lambda: ThreadMail(Expe, "testpythonmailexo@gmail.com",Obj,"testpythonexo", Msg, MailText.get()))
    SendList.place(relx=0.5, rely=0.7, anchor=CENTER)

#IHM

#CREATION DE LA FENETRE NOM CAMPAGNE
global fenetre
global NomCampagne
fenetre = Tk()
fenetre.title("Nom Campagne")

#PARAMETRE DE LA FENETRE
fenetre.geometry("500x300")

#BOUTONS
choixFait = Label(fenetre, text="Nom Campagne", font="Arial 16", anchor="ne")
choixFait.place(relx =0.5, rely = 0.2, anchor=CENTER)
CSV = Entry(fenetre)
CSV.place(relx=0.5,rely=0.4, anchor=CENTER, height=30, width = 250)
ok = Button(fenetre, text="Ok", font="Arial 14", command=lambda: Fenetre2(CSV.get(), True))
ok.place(relx=0.8, rely=0.4, anchor=CENTER, height=30, width=50)

fenetre.mainloop()
