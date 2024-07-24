from encode_message import encodeLsbWithSecretkey,decodeLsbWithSecretkey
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter.filedialog import asksaveasfile

class HideMessagePage(tk.Frame):
    def __init__(self, parent, entry_width):
        super().__init__(parent)

        self.image_path_label = tk.Label(self,text='Image not selected')
        self.image_path_label.pack()

        self.select_button = ttk.Button(self, text="Select image", width=entry_width, command=self.select_file)
        self.select_button.pack(anchor='w', pady=(0, 20),padx=10)

        self.key_label = tk.Label(self, text='Secret key')
        self.key_label.pack()

        self.key_entry = tk.Entry(self, width=entry_width)  # Multiline text input field
        self.key_entry.pack( anchor='w', pady=(0, 20),padx=10)

        self.message_label = tk.Label(self, text='Secret message')
        self.message_label.pack()
        self.message_entry = scrolledtext.ScrolledText(self, height=5, width=entry_width)  # Multiline text input field
        self.message_entry.pack( anchor='w', pady=(0, 20),padx=10)

        self.print_button = ttk.Button(self, text="Encode", width=entry_width, command=self.encode)
        self.print_button.pack(anchor='w', padx=10)

        self.info_label = tk.Label(self, text='')
        self.info_label.pack()

    # Funkcj do wybierania ścieżki obrazu
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path == "" or file_path == 'Image not selected':
            self.info_label.configure(text="Please select image!")
            return


        print("Selected file:", file_path)
        # Update the label with the new image
        self.image_path_label.configure(text=file_path)

    # Funcja walidująca dane i wywołująca fukcję kodującą
    def encode(self):





        image = self.image_path_label.cget("text")

        if image == "" or image == 'Image not selected':
            self.info_label.configure(text="Please select image!")
            return
        key = self.key_entry.get()
        if (key == ""):
            self.info_label.configure(text="Please enter key!")
            return

        message = self.message_entry.get("1.0", tk.END)
        message += '\x00'
        if(message == "\x00" or message is None):
            self.info_label.configure(text="Please enter message!")
            return



        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path == "":
            self.info_label.configure(text="Please select path to save file!")
            return

        self.info_label.configure(text="Processing")
        status = encodeLsbWithSecretkey(message=message, secretKey=key, path=image,path_to_save=file_path)
        if(status == True):
            self.info_label.configure(text="Encoded image saved at: " + file_path)
        else:
            self.info_label.configure(text="Secret message is too long")

    def print_message(self):
        message = self.message_entry.get("1.0", tk.END)
        print(message)





class DecodeMessagePage(tk.Frame):

    def __init__(self, parent, entry_width):
        super().__init__(parent)

        self.image_path_label = tk.Label(self, text='Image not selected')
        self.image_path_label.pack()

        self.select_button = ttk.Button(self, text="Select image", width=entry_width, command=self.select_file)
        self.select_button.pack(anchor='w', padx=10,pady=(0,20))

        self.key_label = tk.Label(self, text='Secret key')
        self.key_label.pack()

        self.key_entry = tk.Entry(self, width=entry_width)  # Multiline text input field
        self.key_entry.pack(anchor='w', padx=10,pady=(0,20))



        self.print_button = ttk.Button(self, text="Decode", width=entry_width, command=self.decode)
        self.print_button.pack(anchor='w', padx=10)

        self.info_label = tk.Label(self, text='')
        self.info_label.pack()

        self.message_label = tk.Label(self, text='Encoded Secret message')
        self.message_label.pack()
        self.message_entry = scrolledtext.ScrolledText(self, height=5, width=entry_width)  # Multiline text input field
        self.message_entry.pack(anchor='w', padx=10)

    # Funkcj do wybierania ścieżki obrazu
    def select_file(self):
        file_path = filedialog.askopenfilename()


        print("Selected file:", file_path)

        # Load the image using PIL
        image = Image.open(file_path)

        # Create a Tkinter-compatible photo image
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        self.image_path_label.configure(text=file_path)

    # Funcja walidująca dane i wywołująca fukcję dekodującą
    def decode(self):

        key = self.key_entry.get()
        image = self.image_path_label.cget("text")

        if image == "" or image == 'Image not selected':
            self.info_label.configure(text="Please select image!")
            return

        if (key == ""):
            self.info_label.configure(text="Please enter key!")
            return

        msg = decodeLsbWithSecretkey(path=image,secretKey=key)


        self.message_entry.delete("1.0", tk.END)  # Clear existing text
        self.message_entry.insert(tk.END, msg)

    def print_message(self):
        message = self.message_entry.get("1.0", tk.END)
        print(message)

