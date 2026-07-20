from pprint import pprint

from app.ai.vectorstore.vector_service import VectorService

service = VectorService()

pprint(service.peek())