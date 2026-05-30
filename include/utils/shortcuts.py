from os import name as os_name


"""
Checks if the current system is a Posix system.
(likely nt, i.e. Windows otherwise)
"""
def is_posix() -> bool:
    return os_name == "posix"


"""
Checks if the current system is a Windows system.
(likely posix otherwise)
"""
def is_nt() -> bool:
    return os_name == "nt"
