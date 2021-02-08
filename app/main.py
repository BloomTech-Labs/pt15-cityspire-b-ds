from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app import db, ml, viz

description = """
This is a basic example of how the return route will look like. 
"""

app = FastAPI(
    title='DS API',
    description=description,
    docs_url='/',
)

app.include_router(db.router, tags=['Database'])
app.include_router(ml.router, tags=['Machine Learning'])
app.include_router(viz.router, tags=['Visualization'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
# For running it locally:
# uvicorn app.main:app --reload