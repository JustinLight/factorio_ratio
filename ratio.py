import pandas as pd
import xlrd
import numpy


recipes = pd.read_excel("Factorio Planning Calculator.xlsx",sheet_name=0)#pull data from excel sheet
recipes = recipes.set_index("Recipe")#set index
csp=''
z = list(recipes.loc[:,:])#create list from header names
f = {'stone': 1, 'steel': 2, 'electric': 2}#furnace speed
fpower = {'stone': ['coal', 0.0225], 'steel': ['coal', 0.0225], 'electric': ['electricity', 180]}#furnace power needs
base_mat = ['Stone', 'Iron ore', 'Copper ore', 'Coal']
furnace_mat = ['Iron plate', 'Copper plate', 'Stone brick', 'Steel plate']




#fuctions to call with user request for recipe
def recipe_find(request):
    l=recipes.loc[request, :] #pull row with restested recipe
    recipe_dict = dict(zip(z,l)) #create dict with header for key and recipe line as values
    fr_dict = {k:v for (k,v) in recipe_dict.items() if v>0} #remove keys if value is 0, not used in recipe
    rtime=fr_dict['Time']
    rout=fr_dict['Output']
    cps=fr_dict.pop('Output')/fr_dict.pop('Time') #calculate how maybe of request can be made per second and remove from dict
    item_list = 'You can craft ' +str(cps)+' '+request+' per second.\nEvery second you will need:\n' #create variable with start of string for output
    for k,v in fr_dict.items(): #calculate items created per assembling machine (currently only 1 per second with no speed changes)
        item_list+=str((v*cps)/rout)+' '+str(k)+'\n'

    fr_dict = {k:v for (k,v) in fr_dict.items() if base_mat.count(k)==0} #remove base materials from dict
    furnace_output='\n---Furnace Production---\n'
    def furnace(kf,vf): #fuction to calculate furnace production
        fo=recipes.loc[kf,:]
        furnace_dict=dict(zip(z,fo))
        furnace_dict={k:v for (k,v) in furnace_dict.items() if v>0}
        ftime=furnace_dict['Time']
        fout=furnace_dict['Output']
        fps=furnace_dict.pop('Output')/furnace_dict.pop('Time')
        ore=str(list(furnace_dict.keys()))
        ore=ore[2:]
        ore=ore[:-2]
        nonlocal furnace_output
        global furnace
        furnace_output+='To craft '+str(vf*cps/rout)+' '+kf +' per second, you will need:\n' + str(furnace_dict[ore]*cps/rout)+' '+ ore+' per second, and ' + str((vf*cps/rout)*ftime/f[furnace])+' furnaces'
        if kf=='Steel plate':
            furnace_output+='\n To craft '+str(furnace_dict[ore]*cps/rout)+' '+ ore+' per second, you will need ' + str(furnace_dict[ore]*cps/rout)+ ' iron ore per second and '+ str(3.5*furnace_dict[ore]*cps/rout/f[furnace])+' furnaces.'
    for (k,v) in fr_dict.items():
        if k in furnace_mat: #calculate steel plate production
            furnace(k,v)

    item_list+=furnace_output
    return(item_list)



request=input("What recipe do you want to search for? ")
furnace=input("What furnace are you using? (stone, steel, or electric)")
print(recipe_find(request))
