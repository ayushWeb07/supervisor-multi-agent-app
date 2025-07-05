# IMPORT PACKAGES
from fastapi import FastAPI, Query
from ai_agent import graph_builder
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from utils import AgentState
from langchain_core.messages import HumanMessage
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Optional
import uuid
from langchain_core.messages import AIMessageChunk
import json

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

agent_app= graph_builder()


# Add CORS middleware with settings that match frontend requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
    expose_headers=["Content-Type"], 
)


# HOME ROUTE
@app.get("/")
async def home():
    return JSONResponse(
        content={
            "message": "Welcome to the AI Agent API",
            "documentation": "Visit /docs for API documentation"
        },
        
        status_code=200
    )


# HEALTH CHECK ROUTE
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "message": "AI Agent API is running smoothly"
        },
        status_code=200
    )
    
    
# FUNCTION FOR GENERATING THE AGENT RESPONSE
async def generate_agent_response(message: str, thread_id: str):
    
    
    # memory configuration
    memory_config= {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    # Get saved memory
    snapshot = agent_app.get_state(config= memory_config)
    
    if snapshot and "messages" in snapshot.values:
        old_msgs = snapshot.values["messages"]
        
    else:
        old_msgs = []           
        
    # invoke the agent
    events = agent_app.astream_events(input=AgentState(messages= old_msgs + [HumanMessage(content= message)]), version="v2", config= memory_config)
        

    # SEND THE EVENTS BACK TO THE USER
    async for event in events: 
                                
        if event["event"] == "on_chat_model_stream":
            
            if isinstance(event["data"]["chunk"], AIMessageChunk):
                event_content= event["data"]["chunk"].content
                
                safe_content = event_content.replace("'", "\\'").replace("\n", "\\n")
                
                safe_content_json= {
                    "type": "content",
                    "content": safe_content
                }
                
                yield f"data: {json.dumps(safe_content_json)}\n\n"
            
            
    # SEND THE END OF STREAM SIGNAL
    yield "data: {\"type\": \"end\"}\n\n"



# CHAT STREAM ROUTE
@app.get("/chat_stream/{message}")
def chat_stream(message: str, thread_id: Optional[str] = Query(default= None, description="Optional thread ID for existing conversations")):
    
    return StreamingResponse(
        generate_agent_response(message, thread_id),
        media_type="text/event-stream"
    )