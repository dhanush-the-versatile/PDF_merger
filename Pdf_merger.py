import os
from tkinter import *
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def add_filename(pdf, output, position):
    reader = PdfReader(pdf)
    writer = PdfWriter()

    # Get filename WITHOUT extension
    filename = os.path.splitext(os.path.basename(pdf))[0]

    for page in reader.pages:
        temp = "temp_overlay.pdf"
        c = canvas.Canvas(temp, pagesize=A4)

        # Position selection
        if position == "Top":
            x, y = 50, 800
        elif position == "Bottom":
            x, y = 50, 30
        else:  # Center
            x, y = 50, 400

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, filename)
        c.save()

        overlay = PdfReader(temp)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    with open(output, "wb") as f:
        writer.write(f)

    os.remove(temp)

def process_pdfs():
    files = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not files:
        return

    pos = position_var.get()
    edited_files = []

    for pdf in files:
        output_pdf = pdf.replace(".pdf", "_edited.pdf")
        add_filename(pdf, output_pdf, pos)
        edited_files.append(output_pdf)

    save_path = filedialog.asksaveasfilename(
        title="Save Merged PDF",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if save_path:
        writer = PdfWriter()
        for pdf in edited_files:
            reader = PdfReader(pdf)
            for page in reader.pages:
                writer.add_page(page)

        with open(save_path, "wb") as f:
            writer.write(f)

        messagebox.showinfo("Success", "PDFs merged successfully!")

# ---------------- GUI ---------------- #

root = Tk()
root.title("PDF Filename Inserter & Merger")
root.geometry("400x280")
root.resizable(False, False)

Label(root, text="Select Filename Position", font=("Arial", 12)).pack(pady=10)

position_var = StringVar(value="Top")
OptionMenu(root, position_var, "Top", "Center", "Bottom").pack()

Button(
    root,
    text="Upload PDFs & Merge",
    command=process_pdfs,
    bg="blue",
    fg="white",
    padx=20,
    pady=10
).pack(pady=25)

# Developer Credit Text
Label(
    root,
    text="This was Developed by Dhanush",
    font=("Arial", 9, "italic"),
    fg="gray"
).pack(side="bottom", pady=10)

root.mainloop()
