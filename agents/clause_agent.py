from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

def build_clause_extractor():
    model = ChatOllama(model= "gemma4:latest", temperature= 0)
    # model = ChatGoogleGenerativeAI(model= "gemini-2.0-flash", 
    #                                temperature = 0, 
    #                                model_kwargs={"response_mime_type": "application/json"})
    prompt = PromptTemplate.from_template("""
    You are a legal clause extraction specialist.
    Analyze this contract text and extract ALL clauses.
    For each clause, identify:
    - Clause type (NDA, IP, Liability, Payment, Termination, Governing Law, etc.)
    - Exact text
    - Parties involved
    - Key obligations

    CONTRACT TEXT:
    {contract_text}

    Return as structured JSON.
    """)
    return prompt | model