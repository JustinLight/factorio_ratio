import pandas as pd
import xlrd
import numpy
import re


recipes = pd.read_excel("Factorio Planning Calculator.xlsx",sheet_name=0)#pull data from excel sheet
recipes = recipes.set_index("Recipe")#set index
cps=''
z = list(recipes.loc[:,:])#create list from header names
f = {'stone': 1, 'steel': 2, 'electric': 2}#furnace speed
fpower = {'stone': ['coal', 0.0225], 'steel': ['coal', 0.0225], 'electric': ['electricity', 180]}#furnace power needs
base_mat = ['Stone', 'Iron ore', 'Copper ore', 'Coal']
furnace_mat = ['Iron plate', 'Copper plate', 'Stone brick', 'Steel plate']
rt=''
ro=''
furnace_output='\n---Furnace Production---\n'
item_list=''


def d_zip(d):
    global cps, z, f, fpower, base_mat, furnace_mat, rt, ro, furnace_output, item_list
    l=recipes.loc[d, :] #pull row with restested item
    recipe_dict = dict(zip(z,l)) #create dict with header for key and recipe line as values
    rd = {k:v for (k,v) in recipe_dict.items() if v>0} #remove keys if value is 0, not used in recipe
    return(rd)

def time(t,o): #set time, output, and per second
    global cps, z, f, fpower, base_mat, furnace_mat, rt, ro, furnace_output, item_list
    rt=t
    ro=o
    return(o/t)

def furn(kf,vf): #fuction to calculate furnace production
    global cps, z, f, fpower, base_mat, furnace_mat, rt, ro, furnace_output, item_list
    furnace_dict=d_zip(kf)
    ftime=furnace_dict['Time']
    fout=furnace_dict['Output']
    fps=furnace_dict.pop('Output')/furnace_dict.pop('Time')
    ore=list(furnace_dict.keys())
    ore=ore[0]

    furnace_output+='To craft '+str(vf*cps/ro)+' '+kf +' per second, you will need:\n' + str(furnace_dict[ore]*cps/ro)+' '+ ore+' per second, and ' + str((vf*cps/ro)*ftime/f[furnace])+' furnaces.\n\n'
    if kf=='Steel plate':
        furnace_output+='To craft '+str(furnace_dict[ore]*cps/ro)+' '+ ore+' per second, you will need ' + str(furnace_dict[ore]*cps/ro)+ ' iron ore per second and '+ str(3.5*furnace_dict[ore]*cps/ro/f[furnace])+' furnaces.\n\n'

def recipe_find(request):
    global cps, z, f, fpower, base_mat, furnace_mat, rt, ro, furnace_output, item_list
    fr_dict=d_zip(request)
    cps=time(fr_dict.pop('Time'),fr_dict.pop('Output'))
    item_list += 'You can craft ' +str(cps)+' '+request+' per second.\nEvery second you will need:\n' #create variable with start of string for output
    for k,v in fr_dict.items(): #calculate items created per assembling machine (currently only 1 per second with no speed changes)
        item_list+=str((v*cps)/ro)+' '+str(k)+'\n'
    item_list+='\n\n'
    fr_dict = {k:v for (k,v) in fr_dict.items() if base_mat.count(k)==0} #remove base materials from dict
    for (k,v) in fr_dict.items():
        if k in furnace_mat: #calculate furnace production
            furn(k,v)
    fr_dict = {k:v for (k,v) in fr_dict.items() if furnace_mat.count(k)==0}
    for (k,v) in fr_dict.items(): #intermediate crafting
        ir=recipes.loc[k, :]
        i_recipe_dict = dict(zip(z,ir))
        i_recipe_dict={k:v for (k,v) in i_recipe_dict.items() if v>0}
    item_list+=furnace_output
    return(item_list)

def tirm(t_dict):
    t_dict = {k:v for (k,v) in t_dict.items() if base_mat.count(k)==0}
    t_dict = {k:v for (k,v) in t_dict.items() if furnace_mat.count(k)==0}
    del t_dict['Time']
    del t_dict['Output']
    return(t_dict)

def sub_list(a):#generate crafting list
    global rlist, working_list, z, temp_list
    fl_dict=d_zip(a)
    fl_dict=tirm(fl_dict)
    p=list(fl_dict.keys())
    if len(p)>0:
        rlist=rlist+p
        for i in p:
            if i in z:
                working_list.append(i)

request=input("What recipe do you want to search for? ")
furnace=input("What furnace are you using? (stone, steel, or electric)")
rlist=rlist.append(request)
working_list=[]
sub_list(request)

print (working_list)
