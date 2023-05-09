import customtkinter as ctk
import settings


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode('light')
		self.geometry('1200x800=100+50')
		self.minsize(800, 600)
		self.title('Mapview')
		self.iconbitmap('./src/map.ico')

		self.mainloop()


if __name__ == '__main__':
	App()
