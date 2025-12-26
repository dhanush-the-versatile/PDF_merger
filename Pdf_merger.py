import os
from tkinter import *
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def add_filename(pdf, output, position):
    reader = PdfReader(pdf)
    writer = PdfWriter()
    filename = os.path.basename(pdf)

    for page in reader.pages:
        temp = "temp.pdf"
        c = canvas.Canvas(temp, pagesize=A4)

        if position == "Top":
            x, y = 50, 800
        elif position == "Bottom":
            x, y = 50, 30
        else:
            x, y = 50, 400

        c.setFont("Helvetica", 10)
        c.drawString(x, y, filename)
        c.save()

        overlay = PdfReader(temp)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    with open(output, "wb") as f:
        writer.write(f)

    os.remove(temp)

def process():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if not files:
        return

    pos = position.get()
    new_files = []

    for f in files:
        out = f.replace(".pdf", "_edited.pdf")
        add_filename(f, out, pos)
        new_files.append(out)

    save = filedialog.asksaveasfilename(defaultextension=".pdf")
    if save:
        writer = PdfWriter()
        for f in new_files:
            reader = PdfReader(f)
            for p in reader.pages:
                writer.add_page(p)
        with open(save, "wb") as file:
            writer.write(file)

        messagebox.showinfo("Success", "PDFs merged successfully!")

root = Tk()
root.title("PDF Filename Inserter & Merger")
root.geometry("400x250")

Label(root, text="Select Filename Position").pack(pady=10)

position = StringVar(value="Top")
OptionMenu(root, position, "Top", "Center", "Bottom").pack()

Button(root, text="Upload PDFs & Merge", command=process,
       bg="blue", fg="white", padx=20, pady=10).pack(pady=30)

root.mainloop()
