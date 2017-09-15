# fonctions appelé avant autre fonctions
# @classmethod, #static_method ....

import functools
# The functools module is for higher-order functions : 
# functions that act on or return other functions. 
# In general, any callable object can be treated as a function for 
# the purposes of this module.

def my_decorator(func):
    # This is a convenience function for 
    # invoking update_wrapper() as a function decorator 
    # when defining a wrapper function
    # functools.update_wrapper = Update a wrapper function to look like 
    # the wrapped function.

    @functools.wraps(func)
    def func_that_runs_func():
        print("In the decorator")
        func()
        print("After the decorator")
    return func_that_runs_func

@my_decorator
def my_function():
    print("I'm the function")

# my_function()
def decorator_with_arguments(number):
    def my_decorator_2(func):
        @functools.wraps(func)
        def func_that_runs_func_2(*args, **kwargs):
            print("In the decorator")
            if number == 56:
               print("Not running the function") 
            else:
                #run my_function_too
                func(*args, **kwargs) 
            print("After the decorator")
        return func_that_runs_func_2 
    return my_decorator_2


@decorator_with_arguments(57)
def my_function_too(x,y):
    print(x+y)

my_function_too(57, 67)