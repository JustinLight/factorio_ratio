import pandas as pd
import xlrd
import numpy

request=input("What recipe do you want to search for? ")
recipes = pd.read_excel("Factorio Planning Calculator.xlsx",sheet_name=0)
recipes = recipes.set_index("Recipe")
z = list(recipes.loc[:,:])
l=recipes.loc[request, :]

recipe_dict = dict(zip(z,l))
fr_dict = {k:v for (k,v) in recipe_dict.items() if v>0}
cps=fr_dict.pop('Output')/fr_dict.pop('Time')
