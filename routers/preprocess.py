import pandas as pd
from fastapi import APIRouter, UploadFile
from .loading import ABBREVS

import sys
sys.path.append("..")


router = APIRouter(prefix="/preprocess", tags=["preprocess"])


@router.get("/remote")
async def preprocess_from_remote(url: str, separator: str):
    df = pd.read_csv(url, sep=separator)
    # Abbreviations replace (in-place)
    df.replace(ABBREVS.keys(), ABBREVS.values(), inplace=True)
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset


@router.post("/local")
def preprocess_from_upload(file: UploadFile, separator: str):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=separator)
    # Abbreviations replace (in-place)
    df.replace(ABBREV.keys(), ABBREV.values(), inplace=True)
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset