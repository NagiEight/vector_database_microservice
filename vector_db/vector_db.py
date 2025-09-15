import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class VectorDatabase:
    """
    A persistent vector database using FAISS for similarity search
    and pickle for metadata storage.
    """
    def __init__(self, dimension, model_name='all-MiniLM-L6-v2', db_path="data/vector_db.faiss", meta_path="data/metadata.pkl"):
        self.dimension = dimension
        self.db_path = db_path
        self.meta_path = meta_path
        self.model = SentenceTransformer(model_name)
        
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize internal state
        self.index = None
        self.metadata = {}
        self.id_counter = 0

        # Attempt to load the database from disk on initialization
        if self._load():
            print("Successfully loaded existing vector database.")
        else:
            self.index = faiss.IndexFlatL2(dimension)
            print("Initialized a new vector database.")

    def add(self, texts: list[str], metadata: list[dict]):
        """
        Adds new text embeddings and their metadata to the database.
        Returns a list of unique IDs assigned to the new entries.
        """
        if len(texts) != len(metadata):
            raise ValueError("Texts and metadata lists must be of the same length.")

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Generate new unique IDs for the entries
        new_ids = list(range(self.id_counter, self.id_counter + len(texts)))
        
        # Add the embeddings to the FAISS index
        self.index.add(np.array(embeddings, dtype='float32'))
        
        # Store metadata linked by the generated ID
        for i, text_id in enumerate(new_ids):
            self.metadata[text_id] = {'text': texts[i], **metadata[i]}
        
        self.id_counter += len(texts)

        # Persist the changes to disk
        self._save()
        return new_ids

    def search(self, query: str, k: int = 5):
        """
        Performs a similarity search for a given query string.
        Returns the top k most similar results with their original text and metadata.
        """
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        
        # Perform a similarity search using the FAISS index
        distances, indices = self.index.search(np.array(query_embedding, dtype='float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx in self.metadata:
                result = self.metadata[idx].copy()
                result['distance'] = float(distances[0][i])
                results.append(result)
        return results
    
    def _save(self):
        """
        Saves the FAISS index and metadata to separate files.
        """
        try:
            # Save the FAISS index
            faiss.write_index(self.index, self.db_path)
            
            # Save the metadata dictionary and ID counter using pickle
            with open(self.meta_path, 'wb') as f:
                pickle.dump({'metadata': self.metadata, 'id_counter': self.id_counter}, f)
        except Exception as e:
            print(f"Error saving database: {e}")

    def _load(self):
        """
        Loads the FAISS index and metadata from files.
        Returns True on success, False on failure.
        """
        # Check if both files exist before trying to load
        if not os.path.exists(self.db_path) or not os.path.exists(self.meta_path):
            print("Database files not found. A new database will be initialized on the first `add` operation.")
            return False

        try:
            # Load the FAISS index
            self.index = faiss.read_index(self.db_path)
            
            # Load the metadata
            with open(self.meta_path, 'rb') as f:
                data = pickle.load(f)
                self.metadata = data['metadata']
                self.id_counter = data['id_counter']
            return True
        except (IOError, EOFError, pickle.UnpicklingError) as e:
            print(f"Error loading database files: {e}. Starting with a new database.")
            # If files are corrupt, we should still start a new database
            return False