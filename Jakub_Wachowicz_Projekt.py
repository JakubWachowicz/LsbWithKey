import tkinter as tk
from tkinter import ttk
from encode_image_page import HideImagePage, DecodeImagePage
from encode_message_page import HideMessagePage, DecodeMessagePage



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Ustawienie rozmiaru aplikacji
        self.geometry("300x400")

        #utworzenie comboboxa zawierającym funkcje stegonograficzne programu
        self.combo = ttk.Combobox(self, state='readonly')
        self.combo.pack(fill=tk.X, padx=10, pady=10)  # fill=tk.X expands the Combobox to the full width
        self.combo['values'] = ('Hide message', 'Decode message','Hide image','Decode image')
        self.combo.current(0)

        #Inicjalizacjja stron stron które wyświetlane są po wybraniu opdowiedniej pozycji z comboboxa
        self.hide_message_frame = HideMessagePage(self, self.winfo_screenwidth())
        self.hide_image_frame = HideImagePage(self,self.winfo_screenwidth())
        self.decode_message_frame = DecodeMessagePage(self,self.winfo_screenwidth())
        self.decode_image_frame = DecodeImagePage(self,self.winfo_screenwidth())

        #Wyświetlenie strony domyślnej
        self.hide_message_frame.pack(fill=tk.BOTH, expand=True)


        #Powiązanie comboboxa z funckją odpowiedzialną za zmianę strony
        self.combo.bind('<<ComboboxSelected>>', self.on_combo_selected)

    #Funkcja usuwająca wyświetlane strony
    def clear_widgets(self):
        self.hide_image_frame.pack_forget()
        self.hide_message_frame.pack_forget()
        self.decode_message_frame.pack_forget()
        self.decode_image_frame.pack_forget()


    #Funkcja obsługująca zmianę wartości comboboxa
    def on_combo_selected(self, event):

        #W zależności od wybranej pozycji wyświetlamy odpowiednią stronę
        selected_option = self.combo.get()
        if selected_option == 'Hide message':
            self.clear_widgets()
            self.hide_message_frame.pack(fill=tk.BOTH, expand=True)

        elif selected_option == 'Decode message':
            self.clear_widgets()
            self.decode_message_frame.pack(fill=tk.BOTH, expand=True)


        elif selected_option == 'Hide image':
            self.clear_widgets()
            self.hide_image_frame.pack(fill=tk.BOTH, expand=True)
        elif selected_option == "Decode image":
            self.clear_widgets()
            self.decode_image_frame.pack(fill=tk.BOTH, expand=True)

app = App()
app.mainloop()