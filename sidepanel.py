import customtkinter as ctk
import settings
from PIL import Image


class SidePanel(ctk.CTkFrame):
    def __init__(self, master, set_style):
        super().__init__(master=master, fg_color=settings.SIDE_PANEL_BG)
        self.grid(row=0, column=0, sticky='nswe')

        ViewButtons(self, set_style)

        self.history_frame = HistoryFrame(self)


class ViewButtons(ctk.CTkFrame):
    def __init__(self, master, set_style):
        super().__init__(master=master, fg_color='transparent')
        self.pack(side='bottom', fill='both', padx='5', pady='5')

        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        map_image = ctk.CTkImage(dark_image=Image.open(settings.map_image_path), light_image=Image.open(settings.map_image_path))
        paint_image = ctk.CTkImage(dark_image=Image.open(settings.paint_image_path), light_image=Image.open(settings.paint_image_path))
        terrain_image = ctk.CTkImage(dark_image=Image.open(settings.terrain_image_path), light_image=Image.open(settings.terrain_image_path))

        ctk.CTkButton(self, text='', width=70, image=map_image, command=lambda: set_style(settings.MAIN_URL), fg_color=settings.BUTTON_COLOR, hover_color=settings.BUTTON_HOVER_COLOR).grid(row=0, column=0, sticky='w')
        ctk.CTkButton(self, text='', width=70, image=paint_image, command=lambda: set_style(settings.PAINT_URL), fg_color=settings.BUTTON_COLOR, hover_color=settings.BUTTON_HOVER_COLOR).grid(row=0, column=1)
        ctk.CTkButton(self, text='', width=70, image=terrain_image, command=lambda: set_style(settings.TERRAIN_URL), fg_color=settings.BUTTON_COLOR, hover_color=settings.BUTTON_HOVER_COLOR).grid(row=0, column=2, sticky='e')


class HistoryFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack(expand=True, fill='both', padx=5, pady=5)

        self.font = ctk.CTkFont(family=settings.TEXT_FONT, size=settings.TEXT_SIZE)

    def add_location(self, location, update_map):
        HistoryItem(self, location, self.font, update_map)


class HistoryItem(ctk.CTkFrame):
    def __init__(self, master, location, font, update_map):
        super().__init__(master=master)
        self.pack(fill='x')

        my_location = str(location).split(', ')
        town = my_location[0]
        country = my_location[-1]
        my_address = f'{country}, {town}' if town != country else country

        ctk.CTkButton(master=self, text=my_address, command=lambda: update_map(location.address), font=font, anchor='w', fg_color='transparent',
                      hover_color=settings.HISTORY_HOVER_COLOR, text_color=settings.TEXT_COLOR).pack(side='left')
        ctk.CTkButton(master=self, text='X', command=lambda: self.pack_forget(), width=15, font=font, anchor='e', fg_color='transparent',
                      hover_color=settings.HISTORY_HOVER_COLOR, text_color=settings.TEXT_COLOR).pack(side='right')
