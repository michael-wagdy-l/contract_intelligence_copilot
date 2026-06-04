from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

def build_compliance_checker():
    #model = ChatGoogleGenerativeAI(model= "gemini-2.0-flash", temperature = 0)
    model = ChatOllama(model= "gemma4:latest", temperature= 0)
    prompt = PromptTemplate.from_template("""
    You are a senior compliance analyst.
    Compare the extracted contract clauses against our internal policy knowledge base.

    EXTRACTED CLAUSES:
    {extracted_clauses}

    RELEVANT POLICY KNOWLEDGE (from RAG):
    {rag_context}

    Identify:
    1. VIOLATIONS — clauses that directly conflict with policy
    2. RISKS — clauses with potential danger
    3. MISSING — required clauses that are absent
    4. SAFE — clauses that comply fully

    You MUST respond with ONLY a valid JSON object in this exact structure, no markdown, no explanation:
    {{
      "violations": [{{"clause_type": "", "finding": "", "severity": "HIGH|MEDIUM|LOW", "explanation": "", "remediation": ""}}],
      "risks":      [{{"clause_type": "", "finding": "", "severity": "HIGH|MEDIUM|LOW", "explanation": "", "remediation": ""}}],
      "missing":    [{{"policy_requirement": "", "finding": "", "severity": "HIGH|MEDIUM|LOW", "explanation": "", "remediation": ""}}],
      "safe":       [{{"clause_type": "", "finding": "", "severity": "LOW", "explanation": ""}}]
    }}
    """)
    return prompt | model
