from typing import Iterable

from chromadb import PersistentClient


class VectorDB:
    def __init__(self, path: str, collection_name: str = "tech_insights") -> None:
        self.client = PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_documents(self, ids: list[str], texts: list[str], metadatas: list[dict] | None = None) -> None:
        self.collection.add(ids=ids, documents=texts, metadatas=metadatas)

    def query(self, text: str, n_results: int = 3) -> dict:
        return self.collection.query(query_texts=[text], n_results=n_results)

    def count(self) -> int:
        return self.collection.count()
