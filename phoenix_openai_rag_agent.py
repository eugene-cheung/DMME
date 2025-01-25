# phoenix_openai_rag_agent.py

# ! pip install --upgrade --quiet pymilvus langchain langchain-community langchainhub langchain-openai faiss-cpu unstructured
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents import Tool
from langchain.llms import OpenAI
from langchain.agents import initialize_agent

import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Set it as an environment variable or in a .env file.")

# Launch Phoenix session for observability
session = px.launch_app()
LangChainInstrumentor().instrument()

# Load and split pgn games for analysis
pgn_folder_path = "./Annotated Games"
loader = DirectoryLoader(pgn_folder_path, glob="*.pgn")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
split_docs = text_splitter.split_documents(docs)
print(f"Loaded and split {len(split_docs)} documents.")

# Embeds split documents into FAISS for retrieval
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(split_docs, embeddings)
retriever = db.as_retriever()
print("Vector store created and retriever initialized.")

# Given chess analysis in chess.py, integrate with LangChain to form agent.
llm = OpenAI(temperature=0, verbose=True)
chess_tool = Tool(
    name="Chess Analysis Tool",
    func=lambda query: ChessEngineTool(engine_path="path/to/stockfish").analyze_position(query), # replace w/ api call
    description="Analyzes a chess position given its FEN."
)

agent = initialize_agent(
    tools=[chess_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# example query
query = "Analyze the position after the 5th move in this game: 1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6"
result = agent.run(query)