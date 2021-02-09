"""Machine learning functions"""
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()


class Prediction(BaseModel):

    """this is an approximate class of what is going to
    be in return route. It may be a subject of change, but overall
    should not change much"""

    state: str
    zip: int
    fips: int
    violent_crime_rate: float
    property_crime_rate: float
    rental_rate: float
    housing_price: int
    walkability_score: float


@router.post('/output')
async def output():
        """For now, this endpoint is populated with fake data"""
        return {'state': 'NY', 'Zip': 10011, 'fips': 49017, 'violent crime rate': 0.4,
                'property crime rate': 1.34, 'rental rate': 1500.0, 'housing price': 700000,
                'walkability score': 138.4}