**Verify Tool (Production-style)** สำหรับโปรเจกต์ *File Fingerprint 2 USB*
ออกแบบให้ **อ่าน Metadata → ดึง Fingerprint → เทียบกับ Server Log → แสดงผลชัดเจน**

---

# 🧠 Architecture ของ Verify Tool

```text
Input File
   ↓
Extract Metadata
   ↓
Parse Fingerprint (JSON)
   ↓
Search in Server (API)
   ↓
Show Result (Source Identification)
```

---

# 📦 โครงสร้างไฟล์

```text
verify_tool/
 ├── main.py
 ├── extractor.py
 ├── parser.py
 ├── api_client.py
 └── utils.py
```

---

# 1️⃣ extractor.py (อ่าน Metadata จากไฟล์)

รองรับหลายประเภท

```python
import json

def extract_from_txt(file_path):
    with open(file_path, "r", errors="ignore") as f:
        data = f.read()

    if "FP:" in data:
        raw = data.split("FP:")[-1]
        return raw.strip()

    return None


def extract_from_pdf(file_path):
    try:
        import fitz
        doc = fitz.open(file_path)
        meta = doc.metadata
        return meta.get("subject", None)
    except:
        return None


def extract_from_docx(file_path):
    try:
        from docx import Document
        doc = Document(file_path)
        return doc.core_properties.comments
    except:
        return None


def extract_fingerprint(file_path):

    ext = file_path.split(".")[-1].lower()

    if ext == "txt":
        return extract_from_txt(file_path)

    elif ext == "pdf":
        return extract_from_pdf(file_path)

    elif ext == "docx":
        return extract_from_docx(file_path)

    else:
        return None
```

---

# 2️⃣ parser.py (แปลง JSON)

```python
import json

def parse_fingerprint(raw):

    try:
        return json.loads(raw)
    except:
        return None
```

---

# 3️⃣ api_client.py (ค้นหาใน Server)

```python
import requests

SERVER_URL = "http://127.0.0.1:8000/search"

def search_by_hash(file_hash):

    try:
        r = requests.get(SERVER_URL, params={"hash": file_hash}, timeout=3)
        return r.json()
    except:
        return None
```

---

# 4️⃣ utils.py (แสดงผลสวยๆ)

```python
def print_result(fp, result):

    print("\n=== FILE FINGERPRINT ===")
    for k, v in fp.items():
        print(f"{k}: {v}")

    print("\n=== TRACE RESULT ===")

    if result and "status" not in result:
        print("✔ SOURCE FOUND")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("✖ NOT FOUND IN LOG")
```

---

# 5️⃣ main.py (ตัวหลัก)

```python
import sys

from extractor import extract_fingerprint
from parser import parse_fingerprint
from api_client import search_by_hash
from utils import print_result


def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <file>")
        return

    file_path = sys.argv[1]

    print("Analyzing file:", file_path)

    # 1. Extract
    raw = extract_fingerprint(file_path)

    if not raw:
        print("No fingerprint found")
        return

    # 2. Parse
    fp = parse_fingerprint(raw)

    if not fp:
        print("Invalid fingerprint format")
        return

    # 3. Search
    result = search_by_hash(fp["hash"])

    # 4. Show result
    print_result(fp, result)


if __name__ == "__main__":
    main()
```

---

# 🧪 วิธีใช้งาน

```bash
python main.py test.pdf
```

---

# ✅ Output ตัวอย่าง

```text
=== FILE FINGERPRINT ===
fpid: FGP-239182
host: FIN-PC01
user: somchai
timestamp: 2026-03-13T14:20
hash: fa8d23a9c...

=== TRACE RESULT ===
✔ SOURCE FOUND
host: FIN-PC01
user: somchai
file_name: budget.xlsx
risk_score: 85
```

---

# 🔥 Feature ที่ Tool นี้รองรับ

✅ อ่าน Metadata จากหลายไฟล์
✅ Parse JSON Fingerprint
✅ Query Server
✅ แสดงผลแบบ forensic

---

# 🚀 Upgrade เพิ่ม (ถ้าจะให้ดูระดับโปร)

## 1. Offline Mode (ไม่มี server ก็หาได้)

```python
search_local_logs(hash)
```

---

## 2. GUI (Tkinter / Web)

* Drag & Drop file
* แสดง result แบบ dashboard

---

## 3. Batch Scan

```bash
python main.py folder/
```

---

## 4. Integrity Check

```python
if current_hash != fp["hash"]:
    print("⚠ FILE MODIFIED")
```

---

# 🎯 สรุป

Verify Tool นี้คือ:

```text
Digital Forensics Tool สำหรับ Data Leak Investigation
```

