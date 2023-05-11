import pandas as pd
from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/loading", tags=["loading"])


@router.get("/remote") 
async def preprocess(url: str):
    df = pd.read_csv(url, sep=";")
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset


@router.post("/local")
def load_from_upload(file: UploadFile):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=";")
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset

