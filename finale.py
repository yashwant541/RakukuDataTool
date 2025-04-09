import tkinter as tk
from tkinter import font, filedialog, messagebox
from PIL import Image, ImageTk
import os
from DummyDataGenerator import main

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def generate_dummy():
    folder_path = folder_entry.get()
    num_rows = int(rows_entry.get())
    options = ""

    for i in range(4):
        if checkboxes[i].get():
            options += str(i + 1)

    try:
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Invalid folder path.")
            return

        main(folder_path, options=options, num_rows=num_rows)

        messagebox.showinfo("Success", "Dummy data generated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Rakuku Dummy Data Generator")

# Load the background image using Pillow
image_path = r"C:\Users\yavnv\OneDrive\Desktop\Packages\gui_test\racoon logo_product.jpg"
image = Image.open(image_path)
background_image = ImageTk.PhotoImage(image)

# Set the window size based on the image size
window_width, window_height = image.size
root.geometry(f"{window_width}x{window_height}")

# Set custom icon
icon_path = r"C:\Users\yavnv\OneDrive\Desktop\Packages\gui_test\racoon_logo_d7K_icon.ico"
root.iconbitmap(icon_path)

# Load Roboto font from the folder
try:
    roboto_font = font.Font(family="Roboto", size=10, name="Roboto", root=root)
except tk.TclError:
    roboto_font = font.nametofont("TkDefaultFont")

# Create a Canvas to place the background image
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

# Set background image
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Create a label with Roboto font
label = tk.Label(root, text="Rakuku Dummy Data Generator", font=(roboto_font, 15), bg="#008000", fg="white")
label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

# Create entry for folder path
folder_label = tk.Label(root, text="Folder Path:", font=(roboto_font, 12), bg="#008000", fg="white")
folder_label.place(relx=0.3, rely=0.35, anchor=tk.E)

folder_entry = tk.Entry(root, width=60, font=roboto_font)
folder_entry.place(relx=0.9, rely=0.35, anchor=tk.E)

browse_button = tk.Button(root, text="Browse", command=browse_folder, bg="#008000", fg="white", font=roboto_font)
browse_button.place(relx=0.8, rely=0.40, anchor=tk.E)

# Create entry for number of rows
rows_label = tk.Label(root, text="Number of Rows:", font=(roboto_font, 12), bg="#008000", fg="white")
rows_label.place(relx=0.3, rely=0.45, anchor=tk.E)

rows_entry = tk.Entry(root, width=15, font=roboto_font)
rows_entry.place(relx=0.5, rely=0.45, anchor=tk.E)

# Create checkboxes for options
checkbox_labels = ["Duplicates", "Errors", "Dupl&Err", "Blank"]
checkboxes = [tk.IntVar() for _ in range(4)]

for i, label_text in enumerate(checkbox_labels):
    checkbox = tk.Checkbutton(root, text=label_text, variable=checkboxes[i], font=roboto_font, bg="#008000", fg="white")
    checkbox.place(relx=0.4, rely=0.55 + i * 0.04, anchor=tk.W)

# Create a button to generate dummy data
generate_button = tk.Button(root, text="Generate Dummy Data", command=generate_dummy, bg="#008000", fg="white", font=roboto_font)
generate_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Start the main loop
root.mainloop()
