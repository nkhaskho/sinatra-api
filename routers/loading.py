import pandas as pd
from fastapi import APIRouter, UploadFile

ABBREVIATIONS = {
    "y": 'yes',
    "n": 'no',
    "m": 'male',
    "f": 'femal',
    "nn": 'naninne',
    "ch": 'champion',
}


router = APIRouter(prefix="/loading", tags=["loading"])


@router.get("/remote") 
async def preprocess(url: str, separator: str):
    df = pd.read_csv(url, sep=separator)
    # Abbreviations replace (in-place)
    df.replace(ABBREVIATIONS.keys(), ABBREVIATIONS.values(), inplace=True)
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset


@router.post("/local")
def load_from_upload(file: UploadFile, separator: str):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=separator)
    # Abbreviations replace (in-place)
    df.replace(ABBREVIATIONS.keys(), ABBREVIATIONS.values(), inplace=True)
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset


