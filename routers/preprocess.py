import pandas as pd
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from settings import ABBREVS, SPEC_CHARS_DICT


router = APIRouter(prefix="/preprocess", tags=["preprocess"])


def lowercase_dataframe(df: pd.DataFrame):
    cols = []
    for index, col in enumerate(df.columns):
        cols.append(col.lower())
    df.columns = cols
    for col in df.columns:
        try:
            df[col] = df[col].str.lower()
        except Exception as e:
            pass
    return df

@router.get("/remote")
async def preprocess_from_remote(url: str, separator: str, fileres: bool=True):
    df = pd.read_csv(url, sep=separator)
    # Abbreviations replace (in-place)
    df = lowercase_dataframe(df)
    df.replace(ABBREVS.keys(), ABBREVS.values(), inplace=True)
    if fileres == True:
        df.to_csv('./datasets/dataset.csv')
        return FileResponse('./datasets/dataset.csv')
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset


@router.post("/local")
def preprocess_from_upload(file: UploadFile, separator: str, fileres:bool=True):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=separator)
    df = lowercase_dataframe(df)
    # Pre-process auto-replace (see settings)
    df.replace(ABBREVS.keys(), ABBREVS.values(), inplace=True)
    # add SPEC_CHARS_DICT & fix regex check
    df.replace({r'.*\?.*': ''}, regex=True, inplace=True)
    if fileres == True:
        df.to_csv('./datasets/dataset.csv')
        return FileResponse('./datasets/dataset.csv')
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset

@router.post("/json")
def preprocess_from_json(data: list[list], separator: str, fileres:bool=True):
    print(data)
    df = pd.DataFrame(data[1:], columns=data[0])
    #df = lowercase_dataframe(df)
    # Pre-process auto-replace (see settings)
    df.replace(ABBREVS.keys(), ABBREVS.values(), inplace=True)
    # add SPEC_CHARS_DICT & fix regex check
    df.replace({r'.*\?.*': ''}, regex=True, inplace=True)
    if fileres == True:
        df.to_csv('./datasets/dataset.csv')
        return FileResponse('./datasets/dataset.csv')
    rows = df.to_numpy(na_value='')
    dataset = [list(df.columns.values)]
    dataset.extend([list(row) for row in rows])
    return dataset