import chromadb
from chromadb.utils import embedding_functions
 
# ChromaDB stores vectors locally in a folder called "chroma_data"
# Like a local H2 database — no external server needed
client = chromadb.PersistentClient(path="./chroma_data")
 
# Use a local embedding model — converts text to numbers
# This is what makes semantic search possible
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # Small, fast, free model
)
 
class RAGStore:
    def __init__(self):
        # Get or create a "collection" — like a database table
        self.collection = client.get_or_create_collection(
            name="ccm_cases",
            embedding_function=embedding_fn
        )
 
    def add_case(self, case_id: str, text: str, metadata: dict = {}):
        """Add a past case to the vector store — like a save() in JPA"""
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[case_id]
        )
 
    def search_similar(self, query: str, n_results: int = 3) -> list[str]:
        """Find similar past cases — like a JPQL similarity query"""
        count = self.collection.count()
        if count == 0:
            return []
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, count)
        )
        return results["documents"][0] if results["documents"] else []
