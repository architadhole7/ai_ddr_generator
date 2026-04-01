# AI DDR Generator

## Overview

This project is an AI-powered system that converts raw inspection reports and thermal reports into a structured **DDR (Detailed Diagnostic Report)**.

It focuses on transforming unstructured, imperfect data into a **clear, client-ready report** with logical reasoning, structured insights, and relevant visual support.

---

##  Key Features

*  Extracts **text and images** from inspection and thermal PDFs
*  Identifies **observations, issues, and thermal anomalies**
*  Merges multi-source data into a **single coherent report**
*  Handles:

  * Missing data → *"Not Available"*
  * Conflicting data → explicitly highlighted
*  Removes duplicate observations
*  Places **relevant images under corresponding sections**
*  Generates a structured **DDR output** in client-friendly language

---

##  AI Workflow

### 1. Input Processing

* Accepts multiple PDF documents:

  * Inspection Report
  * Thermal Report

### 2. Data Extraction

* Text extraction using PDF parsers
* Image extraction and storage

### 3. AI Structuring

* LLM processes extracted data to identify:

  * Observations
  * Affected areas
  * Thermal insights
  * Key issues

### 4. Data Merging (Core Logic)

* Combines inspection + thermal findings
* Removes duplicate entries
* Aligns related observations
* Handles inconsistencies and missing information

### 5. Report Generation

Generates a structured DDR with:

* Property Issue Summary
* Area-wise Observations
* Probable Root Cause
* Severity Assessment (with reasoning)
* Recommended Actions
* Additional Notes
* Missing / Unclear Information

### 6. Output

* Clean, readable report format
* Option to download final report

---

## 🛠️ Tech Stack

* Python
* Flask
* Google Gemini API
* PDF Processing Libraries (PyPDF2 / pdfplumber / Pillow)

---

## 📂 Project Structure

```
ai_ddr_generator/
│── app.py
│── requirements.txt
│── modules/
│   ├── extractor.py
│   ├── image_matcher.py
│   ├── image_cleaner.py
│   ├── ai_structuring.py
│   ├── reasoning.py
│   ├── merger.py
│   ├── ddr_generator.py
```

---

## ⚠️ Limitations

* Performance depends on input document quality
* Image-to-observation mapping can be improved
* Some parts of the pipeline are partially rule-based
* Complex or highly inconsistent reports may affect accuracy

---

## Future Improvements

* Better semantic linking between images and observations
* Fully dynamic and generalized AI pipeline
* Improved conflict detection and reasoning
* Scalable deployment (API-based system)

---

##  Setup Instructions

```bash
pip install -r requirements.txt
python app.py
```

---

##  Demo Link

https://drive.google.com/drive/folders/1PtUr8HXUzBD_VmE-qzEaesb7rljvaZxe?usp=sharing

---

##  Submission

* GitHub Repository: github.com/architadhole7/ai_ddr_generator
* Demo Video: https://drive.google.com/drive/folders/1PtUr8HXUzBD_VmE-qzEaesb7rljvaZxe?usp=sharing

---


