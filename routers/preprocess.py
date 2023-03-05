import pandas as pd
from fastapi import APIRouter
from .models.dataset import Dataset

router = APIRouter(prefix="/preprocess", tags=["preprocess"])


@router.get("/remote", response_model=Dataset) # tags=["preprocess"]
async def preprocess(url: str):
    records = []
    df = pd.read_csv(url, sep=";")
    df = df.dropna(0)
    rows = df.to_numpy()
    records.append(list(df.columns.values))
    for row in rows:
        records.append(list(row))
    dataset = Dataset(headers=records[0], records=records[1:])
    return dataset