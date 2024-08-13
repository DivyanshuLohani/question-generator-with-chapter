from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pdfkit
import os, time

from learncbse import gen_html_header, replace_text_with_headers, BeautifulSoup, get_content as gC


def get_content():
    url = input("URL: ")
    final_content = gen_html_header()
    content = gC(url)

    soup = BeautifulSoup(content, "html.parser")
    main = soup.find("div", class_="entry-content")
    for i in main.find_all("p"):
        html = str(i)
        final_content += replace_text_with_headers(html)

    final_content += '</body>\n</html>'

    return final_content


def html_to_pdf_with_math(html_content, output_file):
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Configure Chrome options for headless mode
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # Optional: might be needed for some environments
    options.add_argument('--no-sandbox')

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    path = os.path.abspath("test.html")
    # Load the HTML content
    driver.get("file://" + path)
    print(path)
    # Wait for MathJax to render the content
    time.sleep(30)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    config = pdfkit.configuration(
        wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # Save the rendered HTML to a PDF
    pdfkit.from_string(driver.page_source, output_file, configuration=config)

    # Clean up
    driver.quit()


# # Example HTML with MathJax
# with open("1.html") as f:
#     html_content = f.read()

# Convert to PDF
html_to_pdf_with_math(get_content(), 'output.pdf')
