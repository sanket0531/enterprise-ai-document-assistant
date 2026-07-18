from app.ai.vectorstore.vector_service import VectorService

service = VectorService()

print("Total vectors:", service.get_collection_count())