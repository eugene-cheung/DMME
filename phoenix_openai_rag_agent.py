# ! pip install --upgrade --quiet pymilvus langchain langchain-community langchainhub langchain-openai faiss-cpu unstructured
# ! docker-compose up -d

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.callbacks import StdOutCallbackHandler
from langchain.callbacks.arize_callback import ArizeCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


session = px.launch_app()


LangChainInstrumentor().instrument()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
loader = DirectoryLoader("../city_data")
docs = loader.load_and_split(text_splitter=text_splitter)



embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(
    docs, 
    embeddings)

retriever = db.as_retriever()





tool = create_retriever_tool(
    retriever,
    "search_cities",
    "Searches and returns excerpts from Wikipedia entries of many cities.",
)
tools = [tool]



prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.messages



llm = ChatOpenAI(temperature=0, verbose=True)



agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke(
    {
        "input": "How big is Boston?"
    }
)

result["output"]