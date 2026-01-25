import os, sys
from ansi_actions.style import style


def main():
    print(style("hello world", "underline", "yellow"))

if __name__ == "__main__":
    main()
