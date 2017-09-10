def my_method(arg1,arg2):
    return arg1+arg2

my_method(5,6)

def  addition_simplified(*args):
    return sum (args)

#addition_simplified(3,5,6,9,40,12)

"""
def what_are_kwargs(*args, **kwargs):
    print(args)
    print(kwargs)
"""

def what_are_kwargs(args1,name,location):
    print(name)
    print(location)

#what_are_kwargs(12, 34, 56, name="Jose",location="UK") 
#what_are_kwargs(name="Jose",location="UK")

# l'ordre des parametres n'a plus d'importance
# argument qui ont "nom" doivent etre a la fin 
what_are_kwargs(56,location="UK",name="Jose")