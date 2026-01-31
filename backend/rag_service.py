import os
import glob

# Try importing chromadb, handle failure gracefully for MVP
try:
    import chromadb
    from chromadb.utils import embedding_functions
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False
    print("Warning: chromadb not installed. RAG features will be disabled.")

DOCS_DIR = "data/docs"
CHROMA_PATH = "backend/chroma_db"

class RAGService:
    def __init__(self):
        self.collection = None
        if HAS_CHROMA:
            # Persistent Client
            self.client = chromadb.PersistentClient(path=CHROMA_PATH)
            
            # Use Default Embedding Function (all-MiniLM-L6-v2 via ONNX)
            # This downloads a small model automatically.
            self.ef = embedding_functions.DefaultEmbeddingFunction()
            
            self.collection = self.client.get_or_create_collection(
                name="knowledge_base",
                embedding_function=self.ef
            )
            
            # Check if empty, if so, ingest
            if self.collection.count() == 0:
                self.ingest_documents()

    def ingest_documents(self):
        print("Ingesting documents into Vector DB...")
        files = glob.glob(os.path.join(DOCS_DIR, "*.md"))
        
        ids = []
        documents = []
        metadatas = []
        
        for fpath in files:
            with open(fpath, "r") as f:
                content = f.read()
            
            fname = os.path.basename(fpath)
            ids.append(fname)
            documents.append(content)
            metadatas.append({"source": fname})
            
        if ids:
            # Batch add
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            print(f"Ingested {len(ids)} documents.")

    def search(self, query, n_results=1):
        if not self.collection:
            return "RAG Service Unavailable (ChromaDB not installed)."
            
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format result
        if results['documents'] and results['documents'][0]:
            top_doc = results['documents'][0][0]
            source = results['metadatas'][0][0]['source']
            return f"Found in **{source}**:\n\n{top_doc[:500]}..." # Truncate for display
        
        return "No relevant documents found."
