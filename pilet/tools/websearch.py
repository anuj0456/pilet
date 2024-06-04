from llama_index.core.tools import FunctionTool
from typing import List, Optional
from llama_index.core import StorageContext
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

documents = SimpleDirectoryReader(input_files = [file_path]).load_data()
db = chromadb.PersistentClient(path="./chroma_db_mistral")
chroma_collection = db.get_or_create_collection("multidocument-agent")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
nodes = splitter.get_nodes_from_documents(documents)
print(f"Length of nodes : {len(nodes)}")

vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
vector_index.storage_context.vector_store.persist(persist_path="/content/chroma_db")


def vector_query(query: str, page_numbers: Optional[List[str]] = None) -> str:
    """
    perform vector search over index on
    query(str): query string needs to be embedded
    page_numbers(List[str]): list of page numbers to be retrieved,
                          leave blank if we want to perform a vector search over all pages
    """
    page_numbers = page_numbers or []
    metadata_dict = [{"key": 'page_label', "value": p} for p in page_numbers]
    #
    query_engine = vector_index.as_query_engine(similarity_top_k=2,
                                                filters=MetadataFilters.from_dicts(metadata_dict,
                                                                                   condition=FilterCondition.OR)
                                                )
    #
    response = query_engine.query(query)
    return response


vector_query_tool = FunctionTool.from_defaults(name=f"vector_tool_test", fn=vector_query)
