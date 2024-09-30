from flask_restx import Api

from .auth import api as auth
from .ai import api as ai

api = Api(
    title='AI-Dashboard Backend',
    version='1.0.0',
    description='A RESTful API backend for the AI-Dashboard project.'
    # All API metadatas
)

api.add_namespace(auth)
api.add_namespace(ai)
