import fitz  # PyMuPDF
import os

def extract_data(pdf_path, image_folder="extracted_images"):
    doc = fitz.open(pdf_path)

    text = ""
    images = []

    os.makedirs(image_folder, exist_ok=True)

    for page_num, page in enumerate(doc):
        text += page.get_text()

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            img_name = f"{image_folder}/img_{page_num}_{img_index}.png"

            with open(img_name, "wb") as f:
                f.write(image_bytes)

            images.append(img_name)

    return {"text": text, "images": images}