from fastapi import FastAPI, UploadFile, HTTPException
from app import analyze_contract
from fileReader import read_file_as_text

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile):

   
    allowed = (".pdf", ".txt")
    if not file.filename.endswith(allowed):
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Upload a PDF, DOCX, or TXT.")

    file_bytes = await file.read()

    # Convert to plain text
    try:
        contract_text = read_file_as_text(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not read file: {str(e)}")

    
    if not contract_text.strip():
        raise HTTPException(status_code=422, detail="File appears empty or text could not be extracted.")


    report = analyze_contract(contract_text, False)
    print(report)

    return {
        "risk_score":      report["risk_score"],
        "violations":      report["violations"],
        "risks":           report["risks"],
        "missing_clauses": report["missing_clauses"],
        "recommendation":  report["recommendation"]
    }
