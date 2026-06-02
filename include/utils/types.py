

"""
Metaclass for singleton creation.

:return Any:
    The singleton instance of the class
"""
from abc import ABCMeta


class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


"""
Metaclass for abstract base classes that will be singletons.

:return Any:
    The singleton instance of the class if properly defined
"""
class ABCSingleton(ABCMeta, Singleton):
    ...

