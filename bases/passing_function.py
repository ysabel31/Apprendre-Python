def methodception(another):
    return another()

def add_two_numbers():
    return 35+77

def not_thirteen(x):
    return x!=13

# print(methodception(add_two_numbers))

# lambda sur 1 ligne fonction anonyme
# print(methodception(lambda:35+77))

my_list = [13,56,77,484]

# my_list.remove(56) 

# utilisation fonction annyme , fonction, liste comprehension => equivalent
print(list(filter(lambda x: x != 13, my_list)))
"""
    (lambda x:x*3) (5) utilisé essentiellement dans les filtres 
        =
    def f(x):
        return x*3
    f(5)
"""
# Concept existe dans bcp de langage de prog
print(list(filter(not_thirteen, my_list)))

# List comprehension est propre à python
print([x for x in my_list if x != 13])