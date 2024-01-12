import PySimpleGUI as ig #Interface Graphique utilisé
import os
def recherche(values, interface):
    global results
    global nboc
    global nbfiles
    global nbfj
    global nbocf
    global a
    global dictionnaire
    results.clear()
    interface['ResultatDR'].update(values=results)
    for root, dirs ,files in os.walk(values['SelecterPath']):
        for file in files:
            nbfiles+=1 
            if values['Termine'] and file.lower().endswith(values['mot'].lower()):
                nbfj+=1
                #Methode si on a selectionné "Termine Avec"
                results.append(f'{root}\\{file}'.replace('\\', '/'))# Replace Pour arranger le nom de la directoire du File
                interface['ResultatDR'].update(results)
            if values['Commence'] and file.lower().startswith(values['mot'].lower()):#Methode si on a selecté "Commence Avec"
                results.append(f'{root}\\{file}'.replace('\\', '/'))#Replace Pour arranger le nom de la directoire du File
                nbfj+=1
                interface['ResultatDR'].update(results)
            if values['Contient'] and values['nom'].lower() in file.lower():
                os.chdir(f'{root}')
                with open(f'{file}','r') as f:
                    dicv=0
                    l=f.readlines()
                    for i in range(len(l)):
                        if len(l[i].split())==1:
                             if len(l)==1:
                                 if values['mot'].lower()== str(l[i]):
                                     nboc+=1
                                     if  dicv==0:
                                         results.append(f'{root}\\{file}'.replace('\\', '/'))
                                     dicv+=1        
                             elif i==0:
                                 if values['mot'].lower()+'\n'== str(l[i]):
                                    nboc+=1
                                    if  dicv==0:
                                         results.append(f'{root}\\{file}'.replace('\\', '/'))
                                    dicv+=1
                             elif i==len(l)-1:
                                 if values['mot'].lower()== str(l[i]):
                                     
                                     nboc+=1
                                     if  dicv==0:
                                         results.append(f'{root}\\{file}'.replace('\\', '/'))
                                     dicv+=1
                             else:
                                if values['mot'].lower()+'\n'== str(l[i]) :
                                    nboc+=1
                                    if  dicv==0:
                                         results.append(f'{root}\\{file}'.replace('\\', '/'))
                                    dicv+=1
                        else:
                            for k in range( len(l[i].split())):
                                a=l[i].split()
                                if a[k]==values['mot'].lower() or a[k]==values['mot'].lower()+str('\n')  or a[k]==values['mot']+',' or a[k]==values['mot']+',':
                                    nboc+=1
                                    if  dicv==0:
                                         results.append(f'{root}\\{file}'.replace('\\', '/'))
                                    dicv+=1                
                    if dicv != 0:
                              dictionnaire[str(file)]=str(dicv)+" fois"
                interface['ResultatDR'].update(results)
    interface['ao'].update('Recherche terminée , Consultez Les fichiers ci dessous pour votre demande')
    if values['Contient']:
     interface['dic'].update(dictionnaire)
     interface['no'].update("Nombre d'occurences du mot "+"" ":" +str(nboc)+" " +"fois" +"  "+ "dans"+" " +str(nbfiles)+" " " fichiers recherchés")
    else:
        interface['dic'].update("")
        interface['no'].update("Nombre de fichiers requis "+"" ":" +str(nbfj)+" " "dans"+" " +str(nbfiles)+" " " fichiers recherchés")
    if nboc==0 and values['Contient']:
        interface['ao'].update('Pas De Resultats Dans Ce Path.Reesayer dans un autre')
        interface['no'].update("N/A")
        interface['dic'].update("")
        LF=['File Not Found']
        interface['ResultatDR'].update(LF)
        ig.PopupOK("Mot N'existe Pas dans aucun fichier")
    if nboc != 0 or values['Commence'] or values['Termine']:
      ig.PopupOK('Recherche terminée, Voir Les Resultats Ci Dessous')     
nboc=0
a=None
nbfj=0
nbfiles=0
dictionnaire={}
dicv=None
results = []
layout = [
    [ig.Text('Type de fichier désiré*', size=(16, 1)),
     ig.Input('.txt', size=(40, 2), key='nom',disabled='True'),
     [ig.Text('*Seulement Pour CONTIENT')],
    [ig.Text('Mot Désiré', size=(16, 1)),
     ig.Input('', size=(40,1), key='mot' )],
     ig.Radio('Contient', group_id='searchtype', size=(10, 1), default=True, key='Contient'),
     ig.Radio('Nom du fichier', group_id='searchtype', size=(15, 1), key='Commence'),
     ig.Radio('Extension', group_id='searchtype', size=(20, 1), key='Termine')],
    [ig.Text('Path: ', size=(15, 1)), 
    ig.Text('/..', size=(50, 1), key='PATH'),
     ig.FolderBrowse('Selectionner le Path',size=(15, 1), key='SelecterPath'), #Choisir ou on veut effectuer la recherche
     ig.Button('Recherche', size=(15, 1), key='Chercher')],
    [ig.Text(size=(80,1),key='no')],#Dans l'output le Nombre d'oc +Nombre de fichiers cherches
    [ig.Text("Tip : Saisir le mot, puis l'option desirée ,puis `Recherche` Après avoir sélectionner le path", key='ao')],
    [ig.Text('',key='dic',size=(100,1))],
    [ig.Listbox(values=results, size=(200, 30), enable_events=True, key='ResultatDR')]]
interface = ig.Window('Mini Search Engine Informatique 3', layout=layout,size=(850,500), grab_anywhere=True)
while True:
    event, values = interface.read()
    if event is None:
        break
    if event == 'Chercher':
        recherche(values, interface)
        nboc=0
        nbfiles=0
        nbfj=0
        dictionnaire={}
        
