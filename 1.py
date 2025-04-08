import fitz  # PyMuPDF
import asyncio
from googletrans import Translator
import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to translate text asynchronously
async def translate_text_async(text, target_language):
    translator = Translator()
    # Await the translation, since the translate function is async
    translation = await translator.translate(text, dest=target_language)
    return translation.text

# Wrapper function to run async function in a synchronous environment
def translate_text(text, target_language):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(translate_text_async(text, target_language))

# Function to save translated text as a new PDF
def save_translation_as_pdf(translated_text, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 40)
    text_object.setFont("Helvetica", 10)
    text_object.setTextOrigin(40, height - 40)

    # Add translated text to the PDF
    for line in translated_text.splitlines():
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()

# Function to handle file selection and translation
def select_pdf():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        pdf_text = extract_text_from_pdf(filepath)
        translated_text = translate_text(pdf_text, selected_language.get())

        # Output translated text to the text box
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, translated_text)  # Display translated text

        # Store the translated text in a variable for later use
        global translated_text_global
        translated_text_global = translated_text

# Function to output the translated text to a PDF
def save_pdf():
    if translated_text_global:
        # Ask user for the output PDF filename and save the translated text as PDF
        save_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if save_filename:
            save_translation_as_pdf(translated_text_global, save_filename)
            print(f"PDF saved as: {save_filename}")
    else:
        print("No translated text available to save.")

# GUI Setup
root = tk.Tk()
root.title("PDF Translator")

# Language Selection Dropdown
selected_language = tk.StringVar(root)
languages = ['en', 'fr', 'de', 'es', 'it', 'ru', 'zh-cn', 'ja']  # Supported languages
selected_language.set('en')

language_dropdown = tk.OptionMenu(root, selected_language, *languages)
language_dropdown.pack(pady=10)

# Select PDF Button
select_button = tk.Button(root, text="Select PDF", command=select_pdf)
select_button.pack(pady=10)

# Save PDF Button
save_pdf_button = tk.Button(root, text="Save Translated PDF", command=save_pdf)
save_pdf_button.pack(pady=10)

# Output Text Area for Translated Text
output_text = tk.Text(root, wrap=tk.WORD, height=15, width=50)
output_text.pack(padx=10, pady=10)

# Initialize translated_text_global to store translated text
translated_text_global = ""

# Start the GUI main loop
root.mainloop()
