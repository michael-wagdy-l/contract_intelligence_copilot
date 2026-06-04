from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import json
import re

class ContractState(TypedDict):
    contract_text: str
    extracted_clauses: dict
    rag_context: str
    compliance_findings: dict
    risk_score: int
    final_report: dict

def build_workflow(vectorstore, clause_extractor, compliance_checker):
    graph = StateGraph(ContractState)

    
    def extract_clauses(state):
        result = clause_extractor.invoke({"contract_text": state["contract_text"]})
        return {"extracted_clauses": result.content}

 
    def retrieve_policies(state):
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(state["contract_text"])
        context = "\n\n".join([d.page_content for d in docs])
        return {"rag_context": context}

   
    def check_compliance(state):
        result = compliance_checker.invoke({
            "extracted_clauses": state["extracted_clauses"],
            "rag_context": state["rag_context"]
        })
        return {"compliance_findings": result.content}

 
    def score_risk(state):
        findings = state["compliance_findings"]
    
        score = calculate_score(findings)
        report = build_report(state, score)
        return {"risk_score": score, "final_report": report}
    


    def extract_json_from_findings(findings_raw) -> dict:
        
        if isinstance(findings_raw, list):
            text = ""
            for block in findings_raw:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    break
        else:
            text = findings_raw

        
        clean = re.sub(r"```json|```", "", text).strip()

        return json.loads(clean)


    def calculate_score(findings_raw) -> int:
        try:
            findings = extract_json_from_findings(findings_raw)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print(f"[calculate_score] Parse failed: {e}")
            return 75

        weights = {"HIGH": 30, "MEDIUM": 15, "LOW": 5}
        score = 0

        for category in ["violations", "risks", "missing"]:
            for item in findings.get(category, []):
                severity = item.get("severity", "LOW").upper()
                score += weights.get(severity, 5)

        return min(score, 100)


    def build_report(state: dict, score: int) -> dict:
        """
        Assemble the final structured report from workflow state.
        """
        try:
            clean = re.sub(r"```json|```", "", state["compliance_findings"]).strip()
            findings = json.loads(clean)
        except (json.JSONDecodeError, TypeError):
            print (state["compliance_findings"])
            findings = {}

        
        if score >= 70:
            recommendation = "REJECT — critical violations require legal review before signing."
        elif score >= 40:
            recommendation = "REVIEW — moderate risks identified; negotiate flagged clauses."
        else:
            recommendation = "APPROVE — low risk, contract aligns with internal policies."
        print(findings)
        return {
            "risk_score":       score,
            "recommendation":   recommendation,
            "violations":       findings.get("violations", []),
            "risks":            findings.get("risks", []),
            "missing_clauses":  findings.get("missing", []),
            "safe_clauses":     findings.get("safe", []),
            "extracted_clauses": state.get("extracted_clauses", "text"),
            "rag_context_used":  state.get("rag_context", ""),
        }
        

   
    graph.add_node("extract", extract_clauses)
    graph.add_node("retrieve", retrieve_policies)
    graph.add_node("check", check_compliance)
    graph.add_node("score", score_risk)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "retrieve")
    graph.add_edge("retrieve", "check")
    graph.add_edge("check", "score")
    graph.add_edge("score", END)

    return graph.compile()
