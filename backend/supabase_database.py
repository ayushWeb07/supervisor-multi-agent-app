# IMPORT PACKAGES
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import EmailStr

# INSTANTIATE
load_dotenv()

url: str = os.getenv("SUPABASE_URL")

key: str = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)


# INSERT THE CHAT TO THE DB
def insert_chat(user_id: str, session_id: str, role: str, content: str):
    
    # insert to DB
    response = (
        sb.table("session")
        .insert({
            "session_id": session_id,
            "user_id": user_id,
            "role": role,
            "content": content
        })
        .execute()
    )
    
    return response
    
    

    
# fetch all sessions
def get_session_summaries(user_id: str):
    response = (
        sb.table("session")
        .select("id, session_id, role, content")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .execute()
    )

    if not response.data:
        return []

    # Dict to store first user_query per session
    first_queries = {}
    
    for row in response.data:
        
        sid = row["session_id"]
        
        if sid not in first_queries:
            first_queries[sid] = {
                "id": row["id"],
                "session_id": sid,
                "first_query": row["content"]
            }

    return list(first_queries.values())



# get application log -> from a session id
def get_chat_history(user_id, session_id):
    
    response = (
        sb.table("session")
        .select("role, content")
        .eq("user_id", user_id)
        .eq("session_id", session_id)
        .execute()
    )
    
    
    # get the messages
    if not response.data:
        return []
    
    else:
        return response.data
    
    
    
# sign up
def sign_up_authentication(email: EmailStr, password: str):

    response = sb.auth.sign_up({
        'email': email,
        'password': password,
        
        'options': {
            'email_redirect_to': 'https://supervisor-multi-agent-frontend.onrender.com/',
        },
    })
    
    
    return response

# sign in
def sign_in_authentication(email: EmailStr, password: str):

    response = sb.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )
    
    
    return response