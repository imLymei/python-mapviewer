import customtkinter as ctk
import settings
import tkintermapview
from geopy.geocoders import Nominatim
import sidepanel


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('light')
        self.geometry('1200x800=100+50')
        self.minsize(800, 600)
        self.title('Mapview')
        self.iconbitmap('./src/map.ico')

        self.input_string = ctk.StringVar()

        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=8, uniform='a')

        self.map_widget = MapWidget(self, self.input_string, self.submit_location)

        self.side_panel = sidepanel.SidePanel(self, self.map_widget.set_style)

        self.mainloop()

    def submit_location(self, event):
        geo_locator = Nominatim(user_agent='my-user')
        location = geo_locator.geocode(self.input_string.get())

        if location:
            self.map_widget.set_address(location.address)
            self.side_panel.history_frame.add_location(location, self.map_widget.set_address)
            self.input_string.set('')
        else:
            self.map_widget.location_entry.error_animation()


class MapWidget(tkintermapview.TkinterMapView):
    def __init__(self, master, input_string, submit_location):
        super().__init__(master=master)
        self.grid(row=0, column=1, sticky='nswe')

        # self.set_tile_server(settings.TERRAIN_URL, max_zoom=22)

        self.location_entry = LocationEntry(self, input_string, submit_location)

    def set_style(self, view_style):
        self.set_tile_server(view_style)


class LocationEntry(ctk.CTkEntry):
    def __init__(self, master, input_string, submit_location):
        self.color_index = 15
        color = settings.COLOR_RANGE[self.color_index]

        input_string.trace('w', self.reset_animation)

        self.has_error = False

        super().__init__(master=master, textvariable=input_string, corner_radius=0, border_width=4,
                         fg_color=settings.ENTRY_BG, text_color=settings.TEXT_COLOR,
                         font=ctk.CTkFont(family=settings.TEXT_FONT, size=settings.TEXT_SIZE),
                         border_color=f'#F{color}{color}')

        self.place(relx=0.5, rely=0.95, anchor='center')

        self.bind('<Return>', submit_location)

    def error_animation(self):
        self.has_error = True

        if self.color_index > 0:
            self.color_index -= 1

            color = settings.COLOR_RANGE[self.color_index]
            border_color = f'#F{color}{color}'
            text_color = f'#{settings.COLOR_RANGE[15-self.color_index]}00'

            self.configure(border_color=border_color, text_color=text_color)

            self.after(10, self.error_animation)

    def reset_animation(self, *args):
        if self.has_error:
            self.configure(border_color=settings.ENTRY_BG, text_color=settings.TEXT_COLOR)
            self.color_index = 15
            self.has_error = False


if __name__ == '__main__':
    App()
