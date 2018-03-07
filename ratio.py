import pandas as pd
import xlrd
import numpy


recipes = pd.read_excel("Factorio Planning Calculator.xlsx",sheet_name=0)#pull data from excel sheet
recipes = recipes.set_index("Recipe")#set index
z = list(recipes.loc[:,:])#create list from header names
f = {'stone': 1, 'steel': 2, 'electric': 2}#furnace speed
fpower = {'stone': ['coal', 0.0225], 'steel': ['coal', 0.0225], 'electric': ['electricity', 180]}#furnace power needs

#fuctions to call with user request for recipe
def recipe_find(request):
    l=recipes.loc[request, :] #pull row with restested recipe
    recipe_dict = dict(zip(z,l)) #create dict with header for key and recipe line as values
    fr_dict = {k:v for (k,v) in recipe_dict.items() if v>0} #remove keys if value is 0, not used in recipe
    cps=fr_dict.pop('Output')/fr_dict.pop('Time') #calculate how maybe of request can be made per second and remove from dict
    item_list = 'You can craft ' +str(cps)+' '+request+' per second.\nEvery second you will need:\n' #create variable with start of string for output
    for k,v in fr_dict.items(): #calculate items created per assembling machine (currently only 1 per second with no speed changes)
        item_list+=str(v*cps)+' '+str(k)+'\n'

    fr_dict = {k:v for (k,v) in fr_dict.items() if k!='Stone'} #remove base materials from dict
    if 'Steel plate' in fr_dict: #calculate steel plate production
        item_list+='To craft '+str(fr_dict['Steel plate']*cps)+' steel plates per second, you will need:\n'+str(fr_dict['Steel plate']*cps*5)+' iron plates per second smelted in ' + str(fr_dict['Steel plate']*cps/(1/17.5)*f[furnace])+ ' '+furnace+ ' furnace\n'
        del fr_dict['Steel plate']
    if "Iron plate" in fr_dict: #calculate iron plate production
        item_list+='To craft '+str(fr_dict['Iron plate']*cps)+' iron plates per second, you will need:\n'+str(fr_dict['Iron plate']*cps)+' iron ore per second smelted in ' + str(fr_dict['Iron plate']*cps/(1/3.5)*f[furnace])+ ' '+furnace+ ' furnace\n'
        del fr_dict['Iron plate']
    if "Copper plate" in fr_dict: #calculate copper plate production
        item_list+='To craft '+str(fr_dict['Copper plate']*cps)+' copper plates per second, you will need:\n'+str(fr_dict['Copper plate']*cps)+' copper ore per second smelted in ' + str(fr_dict['Copper plate']*cps/(1/3.5)*f[furnace])+ ' '+furnace+ ' furnace\n'
        del fr_dict['Copper plate']
    if "Stone brick" in fr_dict: #calculate stone brick production
        item_list+='To craft '+str(fr_dict['Stone brick']*cps)+' stone brick per second, you will need:\n'+str(fr_dict['Stone brick']*cps*2)+' stone per second smelted in ' + str(fr_dict['Stone brick']*cps/(1/3.5)*f[furnace])+ ' '+furnace+ ' furnace\n'
        del fr_dict['Stone brick']

    return(item_list)



request=input("What recipe do you want to search for? ")
furnace=input("What furnace are you using? (stone, steel, or electric)")
print(recipe_find(request))
