import pandas as pd
from fastapi import APIRouter, UploadFile, Body
from .models.dataset import *


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/remote", response_model=DatasetAnalytics)
async def get_analytics_from_remote(url: str):
    df = pd.read_csv(url, sep=";")
    nalist = list(df.isna().sum())
    analytics = DatasetAnalytics(
        columns = df.shape[1], rows = df.shape[0],
        nacount = sum(nalist), headers = list(df.columns),
        duplicates = list(df.duplicated()).count(True),
    )
    return analytics


@router.post("/local", response_model=DatasetAnalytics)
async def get_analytics_from_upload(file: UploadFile = Body()):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=";")
    nalist = list(df.isna().sum())
    analytics = DatasetAnalytics(
        columns = df.shape[1], rows = df.shape[0],
        nacount = sum(nalist), headers = list(df.columns),
        duplicates = list(df.duplicated()).count(True),
    )
    return analytics

