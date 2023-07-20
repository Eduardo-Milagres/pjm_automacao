from modulos.fileManager import fileManager
import customtkinter, tkinter.messagebox

class Copy_gui:
    def gui(self, root):
        entry_path = customtkinter.CTkEntry(master=root, placeholder_text="Digite o caminho dos arquivos", width=400)
        entry_path.pack(padx=20, pady=10)

        button = customtkinter.CTkButton(master=root, text="Copiar", command=lambda: self.caller(entry_path.get()))
        button.pack(padx=20, pady=5)

        tb_not_found = customtkinter.CTkTextbox(master=root, width=400)
        tb_not_found.pack(padx=10)

    def caller(self, path):
        Manager = fileManager()
        not_found = Manager.copy(path, 'dft')
        self.not_found(not_found)
        tkinter.messagebox.showinfo("Concluído", "Arquivos copiados")

    def not_found(self, not_founds):
        print("not found")
        print(not_founds)
        for not_found in not_founds: print(not_found); self.gui.tb_not_found.insert(0, not_found)

if __name__ == "__main__":
    Copy_gui()