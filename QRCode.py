from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, askyesno
import qrcode
import re
from PIL import Image, ImageTk

def close_window():
    if askyesno(title='Close the Program?', message='Do you want to Exit?'):
        window.destroy()

def is_valid_filename(name):
    return bool(re.match(r'^[\w,\s-]+$', name))

def generate_qrcode():
    qrcode_data = data_entry.get()
    qrcode_name = filename_entry.get()
    if not qrcode_name or not is_valid_filename(qrcode_name):
        showerror(title='Error', message='Please provide a valid filename (letters, numbers, underscores, hyphens only).')
        return
    if askyesno(title='Confirmation', message='Create QRCode with provided information?'):
        try:
            qr = qrcode.QRCode(version=1, box_size=6, border=4)
            qr.add_data(qrcode_data)
            qr.make(fit=True)
            name = qrcode_name + '.png'
            img = qr.make_image(fill_color='black', back_color='white')
            img.save(name)
            pil_img = Image.open(name)
            tk_img = ImageTk.PhotoImage(pil_img)
            imagelabel.config(image=tk_img)
            imagelabel.image = tk_img
            reset_button.config(state=NORMAL, command=reset)
        except Exception as e:
            showerror(title='Error', message=f'Error saving QR code: {e}')

def reset():
    if askyesno(title='Reset', message='Reset Fields?'):
        imagelabel.config(image='')
        imagelabel.image = None
        reset_button.config(state=DISABLED)

window = Tk()
window.title('QR Code Generator')
window.geometry('500x480+440+180')
window.resizable(False, False)
window.protocol('WM_DELETE_WINDOW', close_window)

style = ttk.Style()
style.configure('TLabel', foreground='#000', font=('OCR A Extended', 11))
style.configure('TEntry', font=('Dotum', 15))
style.configure('TButton', foreground='#000', font=('DotumChe', 10))

canvas = Canvas(window, width=500, height=480)
canvas.pack()

imagelabel = Label(window)
canvas.create_window(250, 150, window=imagelabel)

qrdata_label = ttk.Label(window, text='QRcode Data', style='TLabel')
data_entry = ttk.Entry(window, width=55, style='TEntry')
canvas.create_window(70, 330, window=qrdata_label)
canvas.create_window(300, 330, window=data_entry)

filename_label = ttk.Label(window, text='Filename', style='TLabel')
filename_entry = ttk.Entry(window, width=55, style='TEntry')
canvas.create_window(84, 360, window=filename_label)
canvas.create_window(300, 360, window=filename_entry)

reset_button = ttk.Button(window, text='Reset', style='TButton', state=DISABLED)
generate_button = ttk.Button(window, text='Generate QRCode', style='TButton', command=generate_qrcode)
canvas.create_window(300, 390, window=reset_button)
canvas.create_window(410, 390, window=generate_button)

window.mainloop()