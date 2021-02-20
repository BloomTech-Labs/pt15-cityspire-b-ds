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
        return {'City': 'Houston',
            'CostOfLivingIndex': 95.8,
            'Density': 981.0,
            'Latitude': '29.5585',
            'Longitude': '-95.3215',
            'MonthlyRents': {'2020-01-01': '1503.0',
            '2020-02-01': '1505.0',
            '2020-03-01': '1505.0',
            '2020-04-01': '1502.0',
            '2020-05-01': '1501.0',
            '2020-06-01': '1500.0',
            '2020-07-01': '1499.0',
            '2020-08-01': '1498.0',
            '2020-09-01': '1499.0',
            '2020-10-01': '1499.0',
            '2020-11-01': '1500.0',
            '2020-12-01': '1500.0',
            '2021-01-01': '1504.0',
            '2021-02-01': '1504.0',
            '2021-03-01': '1503.0',
            '2021-04-01': '1501.0',
            '2021-05-01': '1500.0',
            '2021-06-01': '1498.0',
            '2021-07-01': '1497.0',
            '2021-08-01': '1497.0',
            '2021-09-01': '1497.0',
            '2021-10-01': '1498.0',
            '2021-11-01': '1499.0',
            '2021-12-01': '1499.0'},
            'Population': 122460,
            'PropertyCrimeRate': 101750.0,
            'State': 'TX',
            'ViolentCrimeRate': 25257.0,
            'WalkScore': 46,
            'WalkScoreDescription': 'Car-Dependent',
            'ZIPcode': '77584'}