from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from rag_store import RAGStore
import json

# Initialize LLM — connects to your local Ollama instance
llm = OllamaLLM(model="llama3.2", temperature=0.1)

# Initialize RAG (past case search)
rag = RAGStore()

# Prompt template — instructions you give the AI
ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["communication", "similar_cases"],
    template="""
You are an expert AI assistant for a Customer Communication Management (CCM)
platform used by banks and insurance companies in India.

Analyze the following customer communication and return ONLY valid JSON.

CUSTOMER COMMUNICATION:
{communication}

SIMILAR PAST CASES FOR REFERENCE:
{similar_cases}

Return ONLY this JSON structure with no extra text:
{{
  "classification": "one of: complaint, query, feedback, escalation, fraud_alert, service_request",
  "urgency": "one of: critical, high, medium, low",
  "sentiment": "one of: very_negative, negative, neutral, positive",
  "compliance_risk": "one of: high, medium, low, none",
  "risk_reason": "brief reason if compliance risk exists, else empty string",
  "channel_recommendation": "one of: whatsapp, email, sms, phone_call",
  "channel_reason": "one line explaining why this channel",
  "draft_response": "a professional 2-3 sentence response to send to the customer",
  "confidence_score": a number between 0.0 and 1.0
}}
"""
)

# LangChain 0.3 uses pipe syntax instead of LLMChain
# Old: chain = LLMChain(llm=llm, prompt=ANALYSIS_PROMPT)
# New: chain = ANALYSIS_PROMPT | llm
chain = ANALYSIS_PROMPT | llm

def analyze_communication(text: str) -> dict:
    """
    Main analysis method.
    Takes a customer communication string, returns analysis dict.
    """
    # Step 1: Search similar past cases from FAISS (RAG)
    similar = rag.search_similar(text, n_results=3)
    similar_text = "\n".join([f"- {c}" for c in similar]) if similar else "No similar cases found."

    # Step 2: Run the LLM analysis
    # LangChain 0.3 uses .invoke() instead of .run()
    raw_response = chain.invoke({
        "communication": text,
        "similar_cases": similar_text
    })

    # Step 3: Parse JSON response
    try:
        cleaned = raw_response.strip()
        # Remove markdown code fences if LLM adds them
        if "```" in cleaned:
            parts = cleaned.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    cleaned = part
                    break
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback if LLM returns unexpected format
        result = {
            "classification": "query",
            "urgency": "medium",
            "sentiment": "neutral",
            "compliance_risk": "low",
            "risk_reason": "",
            "channel_recommendation": "email",
            "channel_reason": "Default fallback",
            "draft_response": raw_response[:300],
            "confidence_score": 0.5
        }

    return result