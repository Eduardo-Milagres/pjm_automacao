from modules.fileManager import fileManager
import copy_gui
import customtkinter


class main:
    def __init__(self):
        config = fileManager().readJson("config/GUI.json")
        self.main_GUI(config)

    def main_GUI(self, config):
        WINDOW_WIDTH = config['WINDOW_WIDTH']
        WINDOW_HEIGHT = config['WINDOW_HEIGHT']
        RESIZE = config['resizible'] #Boolean

        ASIDE_PADDING = 5
        ASIDE_WIDTH = 100

        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('green')

        root = customtkinter.CTk()
        root.title("Copy DFTs")
        root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        root.resizable(RESIZE, RESIZE)

        aside_frame = customtkinter.CTkFrame(master=root, width=ASIDE_WIDTH, height=WINDOW_HEIGHT-(ASIDE_PADDING*2))
        aside_frame.grid(row=0, column=0, padx=ASIDE_PADDING, pady=ASIDE_PADDING)
        aside_frame.pack_propagate(False) #Keep aside_frame defined size - True resize based on content

        main_frame = customtkinter.CTkFrame(master=root, width=WINDOW_WIDTH-ASIDE_WIDTH-ASIDE_PADDING*3, height=WINDOW_HEIGHT-(ASIDE_PADDING*2))
        main_frame.grid(row=0, column=1)
        main_frame.pack_propagate(False) #Keep main_frame defined size - True resize based on content

        copy_gui.Copy_gui().gui(main_frame)

        root.mainloop()

if __name__ == "__main__":
    main()

