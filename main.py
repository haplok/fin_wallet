# Главный файл, точка входа в программу
from interface import *
from templates import *


if __name__ == "__main__":
    fw = Fin_wallet()
    print(logo)
    input(greet)
    fw.menu()