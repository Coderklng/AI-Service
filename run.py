import pdfplumber 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings,ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun,tool
from typing import TypedDict,List,Annotated
from langgraph.graph import StateGraph,END,START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage,HumanMessage
import streamlit as st
import os  
import time


llm = ChatOllama(
    model="tinyllama"
)

embedding = HuggingFaceEmbeddings(
 model_name="sentence-transformers/all-MiniLM-L6-v2",
 model_kwargs={"device":"cpu"}
)


class State(TypedDict): 
    messages : Annotated[list,add_messages]
    results : str

    

dog = DuckDuckGoSearchRun()


def calculator(state:State):
    try:
       result = state["messages"][-1].content
       res = eval(result,{"__builtins__":{}},{})
       return {
           "messages":[AIMessage(content=str(res))],
           "results":str(res),
     
       }  
    except Exception as e:
       return {
           "messages":[AIMessage(content=str(e))],
           "results":""
       }
   
   
def web_search(state:State):
    query = state["messages"][-1].content
    res = dog.run(query)
    return {
        "messages":[AIMessage(content=str(res))],
        "results":str(res),

    }



def chatbot(state:State):
    response = llm.invoke(state["messages"])
    return {
        "messages":[AIMessage(content=str(response))],
        "results":response.content
    }     
    

def router(state:State):
    query = state["messages"][-1].content
    if any(op in query for op in ["+","-","/","*","%"]):
         return "calculator"
    elif query.startswith("search"):
         return "tool"  
    else:
         return "chatbot"
     


memory = MemorySaver()

graph = StateGraph(State)

graph.add_node("chatbot",chatbot)
graph.add_node("calculator",calculator)
graph.add_node("tool",web_search)       


graph.add_conditional_edges(
    START,
    router,
    {
        "calculator": "calculator",
        "tool": "tool",
        "chatbot": "chatbot"
    }
)

graph.add_edge("calculator", END)
graph.add_edge("tool", END)
graph.add_edge("chatbot", END)

app = graph.compile(checkpointer=memory)

config = {"configurable":{"thread_id":"user-25"}}

state = {
    "messages":[
        
    ]
}

state["messages"].append(
    HumanMessage(content="search AI latest news in 2026")
)

res = app.invoke(state,config=config)

print(res["messages"][-1].content)