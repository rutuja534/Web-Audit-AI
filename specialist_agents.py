# specialist_agents.py

from langchain_groq import ChatGroq
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from agent_tools import web_search_tool

# --- Base LLM for all specialists ---
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

# --- The Analyst Tool (remains the same) ---
try:
    loader = TextLoader("knowledge/trackers.txt")
    docs = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50))
    retriever = FAISS.from_documents(docs, HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")).as_retriever()
    
    analyst_tool = create_retriever_tool(
        retriever,
        "knowledge_base_retriever",
        "Your primary source of information on known web trackers."
    )
except Exception as e:
    print(f"Error setting up Analyst's knowledge base tool: {e}")
    analyst_tool = None

# --- The OSINT Analyst (This is what we need to import) ---
osint_tools = [web_search_tool]
osint_prompt = hub.pull("hwchase17/react")
osint_agent_runnable = create_react_agent(llm, osint_tools, osint_prompt)
osint_analyst = AgentExecutor(agent=osint_agent_runnable, tools=osint_tools, verbose=True, handle_parsing_errors=True)