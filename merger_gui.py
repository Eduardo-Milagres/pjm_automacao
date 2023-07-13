from modulos.docMerger import *
import customtkinter, tkinter.messagebox

class Merger_gui:
    def caller(self):
        merger = docManager()
        merger.merger(self.gui.entry_path.get())
        tkinter.messagebox.showinfo("Concluído", "Documento criado")

    def gui(self, root):
        entry_path = customtkinter.CTkEntry(master=root, placeholder_text="Digite o caminho dos arquivos")
        entry_path.pack(padx=20)

        button = customtkinter.CTkButton(master=root, text="Juntar", command=self.caller)
        button.pack(padx=20, pady=20)

if __name__ == "__main__":
    Merger_gui()