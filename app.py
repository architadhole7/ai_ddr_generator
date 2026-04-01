from flask import Flask, render_template, request, send_file
import os
from dotenv import load_dotenv
import pdfkit
from flask import send_from_directory


# Load environment variables
load_dotenv()

# Import modules
from modules.extractor import extract_data
from modules.image_cleaner import clean_images
from modules.ai_structuring import extract_observations
from modules.merger import merge_observations
from modules.reasoning import enrich_observations
from modules.image_matcher import match_images
from modules.ddr_generator import generate_ddr

app = Flask(__name__)

# Folder paths
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
IMAGE_FOLDER = "extracted_images"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

FINAL_REPORT_PATH = os.path.join(OUTPUT_FOLDER, "report.html")


# 🔍 Classify file type
def classify_file(text):
    text = text.lower()
    if any(word in text for word in ["temperature", "thermal", "°c", "heat"]):
        return "thermal"
    return "inspection"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            print("\n--- REQUEST RECEIVED ---")

            files = request.files.getlist("files")

            if not files or files[0].filename == "":
                return render_template("index.html", error="Please upload at least one file.")

            all_text_data = []
            all_images = []

            # 📥 Process files
            for file in files:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

                print(f"Processing: {file.filename}")

                data = extract_data(file_path, IMAGE_FOLDER)

                if not data:
                    continue

                all_text_data.append({
                    "text": data.get("text", ""),
                    "type": classify_file(data.get("text", ""))
                })

                all_images.extend(data.get("images", []))

            print("TEXT FILES:", len(all_text_data))
            print("TOTAL IMAGES:", len(all_images))

            # 🧹 Clean images
            cleaned_images = clean_images(all_images)

            # 🤖 Extract observations
            inspection_obs = []
            thermal_obs = []

            for item in all_text_data:
                obs = extract_observations(item["text"], item["type"]) or []

                if item["type"] == "thermal":
                    thermal_obs.extend(obs)
                else:
                    inspection_obs.extend(obs)

            print("INSPECTION OBS:", len(inspection_obs))
            print("THERMAL OBS:", len(thermal_obs))

            # 🧠 Merge
            merged_obs = merge_observations(inspection_obs, thermal_obs) or []

            # 🔎 Reasoning
            enriched_obs = enrich_observations(merged_obs) or []

            # 🖼️ Match images
            final_obs = match_images(enriched_obs, cleaned_images) or []

            print("FINAL OBS:", len(final_obs))

            # 📄 Generate DDR
            report = generate_ddr(final_obs)

            if not report:
                return render_template("index.html", error="Failed to generate report.")

            # ✅ Render HTML
            rendered_html = render_template("report_template.html", report=report)

            # 💾 Save file
            with open(FINAL_REPORT_PATH, "w", encoding="utf-8") as f:
                f.write(rendered_html)

            # 🔥 IMPORTANT CHANGE → show report page directly
            return rendered_html

        except Exception as e:
            print("ERROR:", str(e))
            return render_template("index.html", error=str(e))

    return render_template("index.html")


# 🖼️ Serve images
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)


# 📥 Download report
@app.route("/download")
def download():
    if not os.path.exists(FINAL_REPORT_PATH):
        return "No report available"

    pdf_path = FINAL_REPORT_PATH.replace(".html", ".pdf")

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    pdfkit.from_file(
        FINAL_REPORT_PATH,
        pdf_path,
        configuration=config,
        options={"enable-local-file-access": ""}
    )

    return send_file(pdf_path, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)