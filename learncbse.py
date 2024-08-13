import pdfkit
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import os
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from tkinter import filedialog
import threading
import htmldocx


def gen_html_header():

    html_content = '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    html_content += '<meta charset="UTF-8">\n<title>Generated Page</title>\n'
    html_content += '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
    html_content += '<style>\nbody { font-family: Arial, sans-serif; margin: 20px; }\n'
    html_content += 'h1 { color: #333; }\n'
    html_content += 'p { margin: 10px 0; }\n'
    html_content += 'img { max-width: 100%; height: auto; }\n</style>\n</head>\n<body>\n'

    return html_content


def convert_html_to_pdf(html_content, output_file):
    # Configuration (optional if wkhtmltopdf is in your PATH)
    config = pdfkit.configuration(
        wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # Convert HTML to PDF
    pdfkit.from_string(html_content, output_file, configuration=config)


def covert_html_to_docx(html_content, output_file):
    new_parser = htmldocx.HtmlToDocx()
    doc = new_parser.parse_html_string(html_content)
    doc.save(output_file)


def replace_text_with_headers(text):
    # Replace "Question xx." with "<h2>Question xx.</h2>"
    text = re.sub(r'(Question \d+\.)', r'<h2>\1</h2>', text)

    # Replace "Answer:" with "<h2>Answer</h2>"
    text = re.sub(r'Answer:', r'<h2>Answer</h2>', text)

    return text


def get_content(url):
    with requests.get(url) as r:
        return r.content


def generate_pdf():
    generate_button.configure(state="disabled")

    final_content = gen_html_header()
    name = entry_chapter_name.get()
    if not name:
        CTkMessagebox(title="Error", message="Enter valid name", icon="cancel")
        return
    format = format_var.get()
    if not format or not format in ('PDF',):
        CTkMessagebox(
            title="Error", message="Enter valid format", icon="cancel")
        return

    if format == "PDF":
        fileoptions = (("PDF Files", "*.pdf"),)
    else:
        fileoptions = (("Word File", "*.docx"),)

    filename = filedialog.asksaveasfilename(
        filetypes=fileoptions, initialfile=name)
    if not filename:
        CTkMessagebox(
            title="Error", message="Enter a valid filename", icon="cancel")
        return

    search_results = search(
        name + " Important questions learncbse", num_results=10)

    url = ""
    for i in search_results:
        if "learncbse.in" in i:
            url = i
            break
    if not url:
        CTkMessagebox(title="Error", message="No Chapter found", icon="cancel")
        # url = input("Enter url manually from learncbse.in: ")
        return
    else:
        print("Found page on learncbse extracting data.")

    content = get_content(url)

    soup = BeautifulSoup(content, "html.parser")
    main = soup.find("div", class_="entry-content")
    for i in main.find_all("p"):
        html = str(i)
        final_content += replace_text_with_headers(html)

    if format == "PDF":
        convert_html_to_pdf(
            final_content + '</body>\n</html>', filename + ".pdf")
        os.startfile(filename + ".pdf")
        generate_button.configure(state="normal")

    else:
        covert_html_to_docx(
            final_content + '</body>\n</html>', filename + ".docx")
        os.startfile(filename + ".docx")
        generate_button.configure(state="normal")


def on_generate_button_click():
    # Run the file generation in a separate thread
    threading.Thread(target=generate_pdf, daemon=True).start()


if __name__ == "__main__":
    # Set up the GUI
    root = ctk.CTk()
    root.title("Chapter Exporter")
    root.geometry("500x250")

    # Title
    title_label = ctk.CTkLabel(
        root, text="Chapter Exporter", font=("Arial", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Chapter Name Label and Entry
    ctk.CTkLabel(root, text="Chapter Name:", font=("Arial", 12)).grid(
        row=1, column=0, padx=10, pady=5, sticky="e")
    entry_chapter_name = ctk.CTkEntry(root, width=300, font=("Arial", 12))
    entry_chapter_name.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Format Label and Dropdown
    ctk.CTkLabel(root, text="Select Format:", font=("Arial", 12)).grid(
        row=3, column=0, padx=10, pady=5, sticky="e")
    format_var = ctk.StringVar(value="PDF")
    format_menu = ctk.CTkComboBox(root, variable=format_var, values=[
        "PDF"], font=("Arial", 12))
    format_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Generate Button
    generate_button = ctk.CTkButton(root, text="Generate File", font=(
        "Arial", 12, "bold"), fg_color="#4CAF50", hover_color="#45a049", command=on_generate_button_click)
    generate_button.grid(row=4, column=0, columnspan=2, pady=20)

    root.mainloop()
