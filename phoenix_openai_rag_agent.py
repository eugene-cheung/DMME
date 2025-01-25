# phoenix_openai_rag_agent.py

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Launch Phoenix session
session = px.launch_app()
LangChainInstrumentor().instrument()

# Load and split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
loader = DirectoryLoader("../city_data")
docs = loader.load_and_split(text_splitter=text_splitter)

# Create FAISS vector store
db = FAISS.from_documents(docs, OpenAIEmbeddings())
retriever = db.as_retriever()

# Create retriever tool
tool = create_retriever_tool(
    retriever,
    "search_cities",
    "Searches and returns excerpts from Wikipedia entries of many cities."
)

# Set up LLM and agent
llm = ChatOpenAI(temperature=0, verbose=True)
prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_openai_tools_agent(llm, [tool], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[tool])

# Example query
result = agent_executor.invoke({"input": "How big is Boston?"})
print(result["output"])