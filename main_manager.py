from modules.fileManager import fileManager

class Main:
    def __init__(self):
        from_path = input('Caminho do arquivo: ')
        Manager = fileManager()
        Manager.copy(from_path, 'dft')


if __name__ == "__main__":
    Main()