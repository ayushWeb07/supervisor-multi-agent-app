# IMPORT PACKAGES



from langgraph.graph import StateGraph
from dotenv import load_dotenv

from utils import AgentState, SUPERVISOR, GREETING, ENHANCER, CODER, RESEARCHER, MATHS_REASONER, SHOULD_USE_TOOLS, TOOLS, supervisor_node, greeting_node, enhancer_node, should_use_tools_node, use_tools_node, coder_node, maths_reasoner_node, researcher_node

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

import asyncio

import logging

# Silence only the internal LangGraph noise
logging.getLogger("langgraph").setLevel(logging.ERROR)
logging.getLogger("langgraph.pregel").setLevel(logging.ERROR)



load_dotenv()



# GRAPH CONSTANTS 

graph= StateGraph(AgentState)

memory= MemorySaver()

LLM= "llm"
TOOLS= "tools"


# ADD NODES -> GRAPH
graph.add_node(ENHANCER, enhancer_node)
graph.add_node(GREETING, greeting_node)

graph.add_node(CODER, coder_node)
graph.add_node(MATHS_REASONER, maths_reasoner_node)
graph.add_node(RESEARCHER, researcher_node)

graph.add_node(SHOULD_USE_TOOLS, should_use_tools_node)
graph.add_node(TOOLS, use_tools_node)

graph.add_node(SUPERVISOR, supervisor_node)

graph.set_entry_point(SUPERVISOR)

# FUNCTION THAT COMPILES THE GRAPH AND RETURNS IT
def graph_builder():
    # COMPILE GRAPH
    app= graph.compile(checkpointer= memory)
    
    return app


if __name__ == "__main__":
    
    async def main():
        
        # memory configuration
        memory_config= {
            "configurable": {
                "thread_id": 1
            }
        }
        
        app= graph_builder()
        
        LEAF_NODES = {"greeting", "coder", "maths_reasoner", "enhancer", "researcher"}

        
            
        while True:
            
            # take user prompt
            user_prompt= input("\n\nUser: ")
            
            if user_prompt.lower() == "q":
                break
            
            
            # Get saved memory
            snapshot = app.get_state(config= memory_config)
            
            if snapshot and "messages" in snapshot.values:
                old_msgs = snapshot.values["messages"]
            else:
                old_msgs = []           
                
            # invoke the agent
            events = app.astream_events(input=AgentState(messages= old_msgs + [HumanMessage(content= user_prompt)]), version="v2", config= memory_config)
            
            # show the ai response
            print(f"\nAI: ", end= "", flush= True)
            

            async for event in events: 
                                                
                if event["event"] == "on_chat_model_stream":
                    print(event["data"]["chunk"].content, end="", flush=True)
                                 
            
            
    asyncio.run(main())