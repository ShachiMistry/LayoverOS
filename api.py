from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from agent_graph import app
import uvicorn
import os

# Initialize FastAPI
api = FastAPI(title="LayoverOS API", version="1.0")

# Allow Frontend to Talk to Backend (CORS)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for Hackathon (or specific ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_thread"
    user_location: str = "SFO"
    airport_code: str = "SFO"

class ChatResponse(BaseModel):
    response: str
    history: List[str]

@api.get("/")
def health_check():
    return {"status": "LayoverOS System Online"}

@api.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Main Chat Endpoint.
    Receives user message -> Runs LangGraph Agent -> Returns Response.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    
    # Initialize state with the user's location context
    initial_state = {
        "messages": [request.message],
        "user_location": request.user_location,
        # We will add airport_code to the state in agent_graph.py next
    }
    
    try:
        # Run the Agent
        output = app.invoke(initial_state, config=config)
        
        # Extract the last message from the agent
        agent_response = output['messages'][-1]
        
        # In LangGraph/LangChain, messages are often objects, we ensure string format
        if hasattr(agent_response, 'content'):
            response_text = agent_response.content
        else:
            response_text = str(agent_response)

        return ChatResponse(
            response=response_text,
            history=[str(m) for m in output['messages']]
        )
    
    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting LayoverOS API on port {port}...")
    uvicorn.run(api, host="0.0.0.0", port=port)
