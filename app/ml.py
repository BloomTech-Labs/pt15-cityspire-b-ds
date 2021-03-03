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
    #an effective post route that outputs projected data. Requires 5 arguments
    #listed below
async def output(city, state, ZIPcode, latitude, longitude):
    #Real data#
    return fetch_data(city, state, ZIPcode, latitude, longitude)