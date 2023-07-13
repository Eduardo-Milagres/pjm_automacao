from modulos.fileManager import fileManager
import customtkinter, tkinter.messagebox

class Copy_gui:
    def caller(self, path):
        Manager = fileManager()
        Manager.copy(path, 'dft')
        tkinter.messagebox.showinfo("Concluído", "Arquivos copiados")

    def gui(self, root):
        entry_path = customtkinter.CTkEntry(master=root, placeholder_text="Digite o caminho dos arquivos")
        entry_path.pack(padx=20)

        button = customtkinter.CTkButton(master=root, text="Copiar", command=lambda: self.caller(entry_path.get()))
        button.pack(padx=20, pady=20)

if __name__ == "__main__":
    Copy_gui()