import pandas as pd
from string import punctuation
from fastapi import APIRouter, UploadFile, Body
from .models.dataset import *

# define all your specials chars
SPECIAL_CHARS = ['@', '(', ')', '!']
BIN_CHARS = ['y', 'n', 't', 'f', 'y', 'y.', 'n.', 't.', 'f.']

spechars = "|".join(SPECIAL_CHARS)


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/remote", response_model=DatasetAnalytics)
async def get_analytics_from_remote(url: str, sep=";"):
    df = pd.read_csv(url, sep=sep)
    nalist = list(df.isna().sum())
    spechars_counts, bins = 0, 0
    bins = df.isin(BIN_CHARS).sum(axis=1).count()
    for col in df.columns:
        try:
            spechars_counts += len(df[df[col].str.contains(spechars)])
        except:
            pass
    analytics = DatasetAnalytics(
        columns = df.shape[1], 
        rows = df.shape[0],
        nacount = sum(nalist), # na_counts 
        headers = list(df.columns),
        duplicates = list(df.duplicated()).count(True),
        spechars = spechars_counts,
        binaries = bins
    )
    return analytics



@router.post("/local")
async def get_analytics_from_upload(file: UploadFile, sep=","):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=sep)
    nalist = list(df.isna().sum())
    spechars_counts, bins = 0, 0
    bins = df.isin(BIN_CHARS).sum(axis=1).count()
    for col in df.columns:
        try:
            spechars_counts += len(df[df[col].str.contains(spechars)])
        except:
            print('Exception')
    analytics = DatasetAnalytics(
        columns = df.shape[1], 
        rows = df.shape[0],
        nacount = sum(nalist),
        duplicates = list(df.duplicated()).count(True),
        spechars = spechars_counts,
        binaries = bins,
        headers = list(df.columns),
    )
    return analytics