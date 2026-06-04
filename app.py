from agents.clause_agent import build_clause_extractor
from agents.compliance_checker import build_compliance_checker
from graph import build_workflow
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_contract(contract: str, isPath: bool):
   
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    vectorstore = Chroma(
    collection_name="legal_kb",
    embedding_function=embeddings,
    persist_directory="./vector db",
    )
    
    # Build agents
    extractor = build_clause_extractor()
    checker = build_compliance_checker()

    # Build and run the workflow
    workflow = build_workflow(vectorstore, extractor, checker)

    if isPath:
        with open(contract, "r") as f:
            contract_text = f.read()

    else:
        contract_text = contract
    result = workflow.invoke({"contract_text": contract_text})
    return result["final_report"]
    #return result["compliance_findings"]

if __name__ == "__main__":
    report = analyze_contract('C:\\Users\\MichaelShenouda\\Desktop\\New folder\\Ai contract Intelligence copilot\\contracts\\RAG_Contract_03_Conflicting_Liability.pdf', True)
    print(report)