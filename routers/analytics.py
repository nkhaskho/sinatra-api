import pandas as pd
import numpy as np
from string import punctuation
from fastapi import APIRouter, UploadFile, Body
from .models.dataset import *

# define all your specials chars
SPECIAL_CHARS = ['@', '(', ')', '!']
BIN_CHARS = ['y', 'n', 't', 'f', 'y', 'y.', 'n.', 't.', 'f.']
# special null values
SPECIAL_NULLS = ['null', 'Nan', 'nan', 'nil', '?']

spechars = "|".join(SPECIAL_CHARS)
specialna = "|"

async def df_analytics(df: pd.DataFrame):
    analytics = DatasetAnalytics(
        columns = df.shape[1], 
        rows = df.shape[0],
        nacount = sum(list(df.isna().sum())),
        spechars = df[df.isin(SPECIAL_CHARS)].count(axis=0).sum(),
        specialnas = df[df.isin(SPECIAL_NULLS)].count(axis=0).sum(),
        binaries = df[df.isin(BIN_CHARS)].count(axis=0).sum(),
        numerics = df.select_dtypes(include=np.number).count().sum(),
        duplicates = list(df.duplicated()).count(True),
        headers = list(df.columns),
    )
    return analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/remote", response_model=DatasetAnalytics)
async def get_analytics_from_remote(url: str, sep=";"):
    df = pd.read_csv(url, sep=sep)
    analytics = await df_analytics(df)
    return analytics


@router.post("/local")
async def get_analytics_from_upload(file: UploadFile, sep=","):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=sep)
    analytics = await df_analytics(df)
    return analytics