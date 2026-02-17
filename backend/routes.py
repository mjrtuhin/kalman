from fastapi import APIRouter, HTTPException
from backend.models import PredictionRequest, PredictionResponse, ChatRequest, ChatResponse
from backend.prediction_service import prediction_service
from backend.chat_manager import chat_manager
from agents.nlp_agent import NLPAgent
import requests

router = APIRouter()
nlp_agent = NLPAgent()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if not request.conversation_id:
            conv_id = chat_manager.create_conversation()
        else:
            conv_id = request.conversation_id
        
        chat_manager.add_message(conv_id, "user", request.message)
        context = chat_manager.get_context(conv_id)
        parsed = nlp_agent.parse_query(request.message)
        intent = nlp_agent.extract_intent(request.message)
        
        query_lower = request.message.lower()
        
        if "anywhere" in query_lower or ("london" in query_lower and "postcode" not in parsed["input_data"]):
            response = """I can give you a general idea! London property prices vary a lot by area:

📍 **Central London (SW1, W1):** £800K - £2M+ for a typical house
📍 **Inner London (E1, N1):** £500K - £900K
📍 **Outer London (BR1, RM1):** £300K - £600K

For a specific prediction, please provide:
- A postcode (e.g., SW1A 1AA)
- Property type (detached, semi, terraced, flat)

Example: "How much is a 3 bed semi in SW1A 1AA?"
"""
            chat_manager.add_message(conv_id, "assistant", response)
            return ChatResponse(
                message=response,
                conversation_id=conv_id,
                metadata={"intent": "general_guidance"}
            )
        
        if parsed.get("missing_fields") and intent == "predict_price":
            missing_prompt = nlp_agent.get_missing_fields_prompt(parsed["missing_fields"])
            chat_manager.add_message(conv_id, "assistant", missing_prompt)
            
            return ChatResponse(
                message=missing_prompt,
                conversation_id=conv_id,
                metadata={"intent": "request_info", "missing": parsed["missing_fields"]}
            )
        
        if intent == "predict_price":
            result = prediction_service.predict_house_price(parsed["input_data"])
            response_message = f"💰 {result['explanation']}"
            
            chat_manager.add_message(conv_id, "assistant", response_message)
            
            return ChatResponse(
                message=response_message,
                prediction=result["prediction"],
                confidence_low=result["confidence_low"],
                confidence_high=result["confidence_high"],
                conversation_id=conv_id,
                metadata={"intent": intent, "extracted": parsed["input_data"]}
            )
        
        elif intent == "scenario":
            prompt = f"Previous: {context}\n\nUser asks: {request.message}\n\nRespond about property value changes."
            
            llm_response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
                timeout=30
            )
            
            response_text = llm_response.json()["response"].strip()
            chat_manager.add_message(conv_id, "assistant", response_text)
            
            return ChatResponse(
                message=response_text,
                conversation_id=conv_id,
                metadata={"intent": intent}
            )
        
        else:
            response_text = "💡 Try asking: 'How much is a 3 bed semi in SW1 worth?' or 'What's the price of a flat in Manchester M1?'"
            chat_manager.add_message(conv_id, "assistant", response_text)
            return ChatResponse(
                message=response_text,
                conversation_id=conv_id,
                metadata={"intent": intent}
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict")
async def predict(request: PredictionRequest):
    try:
        result = prediction_service.predict_house_price(request.input_data)
        return PredictionResponse(
            category=request.category,
            prediction=result["prediction"],
            confidence_low=result["confidence_low"],
            confidence_high=result["confidence_high"],
            explanation=result["explanation"],
            metadata={"model_version": result["model_version"]}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models():
    return {"models": [{"id": "house_price", "status": "active"}]}
