from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

from agent_tools import web_search_tool

# --- Base Agent Setup ---
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# --- The Knowledge Base Retriever ---
# We are creating the core retriever here and making it available for import.
# This is the object we will use directly in our orchestrator.
try:
    loader = TextLoader("knowledge/trackers.txt")
    docs = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50))
    knowledge_base_retriever = FAISS.from_documents(docs, embeddings).as_retriever()
except Exception as e:
    print(f"Error setting up knowledge base: {e}")
    knowledge_base_retriever = None

# --- The Cyber Intelligence Agent (remains the same) ---
cy_intel_tools = [web_search_tool]
cy_intel_prompt = hub.pull("hwchase17/react")
cy_intel_agent_runnable = create_react_agent(llm, cy_intel_tools, cy_intel_prompt)
cy_intel_agent = AgentExecutor(agent=cy_intel_agent_runnable, tools=cy_intel_tools, verbose=True)