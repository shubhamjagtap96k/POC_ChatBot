from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid

from backend.dialog_manager import DialogManager

app = FastAPI(title="POC Chatbot")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (Not persistent across restarts)
sessions = {}
dialog_manager = DialogManager()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/ask", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Get or create session
    session_id = request.session_id
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"state": "GREETING", "data": {}}
        # If new session, we might want to return the greeting immediately? 
        # But the loop expects a user message to trigger a response.
        # Let's say if session is new, we ignore user input (or treat it as "hello")
        # and invoke handle_turn to get the greeting.
    
    session = sessions[session_id]
    
    # Process turn
    response_text, next_state = dialog_manager.handle_turn(session, request.message)
    
    # Check if we need to auto-advance (e.g., initial greeting)
    # The DialogManager logic I wrote:
    # GREETING -> Returns Greeting -> Next STATE_MENU
    # So if we are in GREETING, we get "Hello...", next is MENU.
    # The User sees "Hello...", then user types something.
    # That user input goes to MENU state logic.
    # It works.
    
    # Logic fix: If session was just created, we might want to auto-trigger the greeting without user input
    # But usually frontend sends "" or "start".
    
    return {
        "response": response_text,
        "session_id": session_id
    }

@app.get("/")
def read_root():
    return {"status": "POC Chatbot is running"}
