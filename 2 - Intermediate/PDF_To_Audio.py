import pyttsx3
import PyPDF2

def pdf_to_audio(pdf_path, start_page=1, end_page=None):
    try:
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        end_page = end_page if end_page else num_pages

        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)

        for page_num in range(start_page - 1, end_page):
            page = pdf_reader.getPage(page_num)
            text = page.extractText()
            engine.say(text)
            engine.runAndWait()

        pdf_file.close()
    except Exception as e:
        print(f'Error: {e}')

# Example usage
# pdf_to_audio('sample.pdf', 1, 3)
