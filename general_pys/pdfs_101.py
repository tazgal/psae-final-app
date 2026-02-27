from PyPDF2 import PdfReader

'''

page = reader.pages # Πρώτη σελίδα
print(page.extract_text())  # Εξαγωγή κειμένου
'''
reader = PdfReader("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/CrisisDetectionNLP.pdf")
print(f"Αριθμός σελίδων: {len(reader.pages)}")

for page_num, page in enumerate(reader.pages):
    print(f"Σελίδα {page_num + 1}:")
    print(page.extract_text())
