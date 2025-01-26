from os import environ
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(
)

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user", "content": "Analyze the position after the 5th move in this game: 1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6"}
#   ]
# )
#
# print(completion.choices[0].message)


def analyze_game(pgn, index):
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
      {"role": "user",
       "content": f"Analyze the position after the {index+1}th move in this game: {pgn}."}
    ]
  )
  return completion.choices[0].message

# load_dotenv()
#
#
# from llama_index.core import (
#     SimpleDirectoryReader,
#     VectorStoreIndex,
#     StorageContext,
#     load_index_from_storage,
# )
# from llama_index.core.tools import QueryEngineTool, ToolMetadata
# from llama_index.core.agent import ReActAgent
# from llama_index.llms.openai import OpenAI
#
#
# # Create an llm object to use for the QueryEngine and the ReActAgent
# llm = OpenAI(model="gpt-4")
#
# import phoenix as px
# session = px.launch_app()
#
# from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
# from phoenix.otel import register
#
# tracer_provider = register()
# LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
#
# try:
#     storage_context = StorageContext.from_defaults(
#         persist_dir="./storage/chess"
#     )
#     chess_index = load_index_from_storage(storage_context)
#
#     index_loaded = True
# except:
#     index_loaded = False
#
# if not index_loaded:
#     # Load chess game data (assuming `.pgn` files)
#     chess_docs = SimpleDirectoryReader(
#         input_files=["./Annotated Games/*.pgn"]
#     ).load_data()
#
#     # Build the index
#     chess_index = VectorStoreIndex.from_documents(chess_docs, show_progress=True)
#
#     # Persist index
#     chess_index.storage_context.persist(persist_dir="./storage/chess")
#
# # Create a query engine for chess game data
# chess_engine = chess_index.as_query_engine(similarity_top_k=3, llm=llm)
#
# query_engine_tools = [
#     QueryEngineTool(
#         query_engine=chess_engine,
#         metadata=ToolMetadata(
#             name="chess_game_analysis",
#             description=(
#                 "Provides analysis on chess positions. Input a chess move sequence or FEN string."
#             ),
#         ),
#     ),
# ]
#
# agent = ReActAgent.from_tools(
#     query_engine_tools,
#     llm=llm,
#     verbose=True,
#     max_turns=10,
# )
#
# # Example query to analyze a chess position
# response = agent.chat("Analyze the position after the 5th move in this game: 1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6")
# print(str(response))