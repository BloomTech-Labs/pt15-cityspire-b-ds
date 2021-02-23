"""Machine learning functions"""
import os
import requests
import sqlalchemy
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import APIRouter
from .fetch_data import fetch_data

router = APIRouter()


@router.post('/output')
async def output(city, state, ZIPcode, latitude, longitude):
    """Real data"""
    return fetch_data(city, state, ZIPcode, latitude, longitude)
