from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app import db, ml, viz

description = """
This is a finalized version of DS API. 

GET route is used to ensure that AWS database has a proper connection
(does not affect the functionality)

POST route receives 5 arguments:
city, state, ZIPcode, latitude, longitude

and returns the following information:
ZIPcode, City, State, Latitude, Longitude,
Population, Density, WalkScore, WalkScoreDescription, 
ViolentCrimeRate, PropertyCrimeRate, 
MonthlyRents: Past 2 years,
CostOfLivingIndex
"""

app = FastAPI(
    title='DS API',
    description=description,
    docs_url='/',
)

# This portion connects routers from other files all together
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
