import streamlit as st
import requests
import json
import re

from supabase_db import insert_chat, get_chat_history, get_session_summaries, sign_up_authentication, sign_in_authentication

import uuid


# UTILITIES

# List of route tags to clean
route_tags = [json.dumps({"route": "greeting"}), 
              
              json.dumps({"route": "enhancer"}),
              
              json.dumps({"route": "coder"}),
              
              json.dumps({"route": "maths_reasoner"}),
              
              json.dumps({"route": "researcher"})            
]

# remove all the route tags from the ai response
def clean_text(text):
    for tag in route_tags:
        text = text.replace(tag, "")
        
    return text 

# format the text for LaTeX rendering in markdown
def format_latex_markdown(text: str) -> str:
    # Replace [some latex] → $some latex$
    text = re.sub(r'\(([^)]*?\\frac[^)]*?)\)', r'$\1$', text)
    return text.replace("\\n", "\n")


# INITIALISE THE ST SESSIONS
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
    
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    
if "all_session_summaries" not in st.session_state:
    st.session_state["all_session_summaries"]= []
    
if "user_id" not in st.session_state:
    st.session_state["user_id"]= None
    
if "is_signing_in" not in st.session_state:
    
    st.session_state["is_signing_in"]= True
    
# ATUHENTICATION FUNCTIONS
def change_auth_mode():
    st.session_state["is_signing_in"]= not st.session_state["is_signing_in"] 
    
def show_auth_ui():
    st.title("Sign In" if st.session_state["is_signing_in"] else "Sign Up")
        
    email= st.text_input("Enter your email")
    password= st.text_input("Enter your password", type= "password")

    sign_btn= st.button("Sign In" if st.session_state["is_signing_in"] else "Sign Up")
    
    st.toggle(label= "Already have an account?", value= True, on_change= change_auth_mode, key= "auth_toggle")

    st.html("<br >")
        
    if sign_btn:
        
        if email and password:
            try:
                
                if st.session_state["is_signing_in"]:
                    response= sign_in_authentication(email= email, password= password)
                
                else:
                    response= sign_up_authentication(email= email, password= password)
                    
                
                user_id= response.user.id
                
                st.session_state["user_id"]= user_id
                
                st.rerun()  # 🔁 Force UI to refresh and hide auth UI
            
            except Exception as e:
                st.error(f"Sign in failed\n\nError: {str(e)}" if st.session_state["is_signing_in"] else f"Sign up failed\n\nError: {str(e)}")
                
        else:
            st.error("Both email and password should be filled")
    
    
# SHOW AUTH UI
if not st.session_state["user_id"]:    
    
    show_auth_ui()
    
    
# SELECT PRE EXISTING SESSION
def select_pre_existing_session(session_id):
    
    st.session_state["session_id"]= session_id
    
    st.session_state["chat_history"]= get_chat_history(user_id= st.session_state["user_id"], session_id= session_id)
    # st.session_state["is_new_session"]= False
    
    
# CREATE NEW SESSION
def create_new_chat():
    st.session_state["chat_history"]= []
    st.session_state["session_id"]= str(uuid.uuid4())
    st.session_state["all_session_summaries"]= get_session_summaries(user_id= st.session_state["user_id"])
    
    
# LOGOUT USER
def logout_user():
    st.session_state["user_id"]= None


# CREATE THE BASIC UI
if st.session_state["user_id"]:
    st.title("Chat with the Multi-Agent AI")

    st.write("Type your message below and press Enter to chat with the AI agent.")

    st.html("<br >")

    st.html("<br >")

# FUNCTION TO STREAM CHAT RESPONSE 
def stream_chat_response(message):
    url = f"http://127.0.0.1:8000/chat_stream/{message}"
    
    thread_id= st.session_state["session_id"]
    
    params = {}
    if thread_id:
        params["thread_id"] = thread_id

    with requests.get(url, params=params, stream=True) as response:
        
        if response.status_code != 200:
            yield f"Error: {response.status_code}"
            return
        
        for line in response.iter_lines(decode_unicode=True):
            
            if line:
                # If it's SSE format like "data: hello"
                if line.startswith("data:"):
                    json_str= line[5:].strip()
                    
                    try:
                        data = json.loads(json_str)
                        
                        if thread_id and data.get("type") == "content":
                            yield data.get("content", "")
                            
                    except json.JSONDecodeError:
                        raise Exception(f"Invalid JSON format: {json_str}")
                
                else:
                    yield line
    
    
# SHOW ALL SESSIONS IN THE SIDEBAR
if st.session_state["user_id"]:
    with st.sidebar:


        col_1, col_2= st.columns(2)
        
        # create new chat
        
        col_1.button(label= "New Chat", key= str(uuid.uuid4()), on_click= create_new_chat)
        
        # logout
        col_2.button(label= "Logout", key= str(uuid.uuid4()), on_click= logout_user)
            
        # show all chats
        st.html("<h3>All chats</h3>")
        
        st.session_state["all_session_summaries"]= get_session_summaries(user_id= st.session_state["user_id"])
        
        
        if len(st.session_state["all_session_summaries"]) == 0:
            st.write("No sessions found")
            
        else:
            
            for session in st.session_state["all_session_summaries"]:
                st.button(label= session["first_query"][:20], key= session["id"], on_click= select_pre_existing_session, args= [session["session_id"]])
                
                
    
# SHOW THE CHAT HISTORY
if st.session_state["user_id"]:
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            if msg["role"] == "ai":
                st.markdown(msg["content"], unsafe_allow_html=False)
                
            else:
                st.write(msg["content"])


    
# USER IS SIGNED IN AND HAS A SESSION

if st.session_state["user_id"]:

    # show the user input
    prompt= st.chat_input("Talk to the AI agent here...")

    if prompt:
        
        # display prompt and update session state -> user prompt
        st.chat_message("human").write(prompt)
        
        st.session_state["chat_history"].append({"role": "human", "content": prompt})
        
         # append to the supabse db
        insert_chat(
            session_id= st.session_state["session_id"],
            user_id= st.session_state["user_id"],
            role= "human",
            content= prompt
        )
        
        # displayprompt and update session state -> AI response
        with st.spinner("Thinking..."):
        
            # update the ui
            ai_msg_ui= st.chat_message("ai")
            
            # Placeholder to allow dynamic updates
            msg_placeholder = ai_msg_ui.empty()
        
            full_response = ""
            
            thread_id= st.session_state["session_id"]
            
            for chunk in stream_chat_response(prompt):
                print(chunk)
                full_response += chunk
                clean_response = clean_text(full_response)

                # Properly render markdown (headings, bullets, code, LaTeX math)
                msg_placeholder.markdown(format_latex_markdown(clean_response), unsafe_allow_html=False)
            
            # update the session state with the AI response
            st.session_state["chat_history"].append({"role": "ai", "content": format_latex_markdown(clean_text(full_response))})
            
            # append to the supabse db
            insert_chat(
                session_id= st.session_state["session_id"],
                user_id= st.session_state["user_id"],
                role= "ai",
                content= format_latex_markdown(clean_text(full_response))
            )
            
            # rerun -> update the sidebar
            st.session_state["all_session_summaries"]= get_session_summaries(user_id= st.session_state["user_id"])
            
            st.rerun()
            
