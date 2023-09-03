import pandas as pd
from fastapi.responses import FileResponse
import io
from fastapi import APIRouter, HTTPException, UploadFile
from .mtab import *
from models.dataset import *
from settings import RESOURCE_URL, ONTOLOGY_URL


router = APIRouter(prefix="/annotations", tags=["annotations"])

mtab_client = MtabClient()


@router.get("/remote")
async def annotate_from_url(url: str, sep:str=","):
    ann_request = AnnotationRequest("From-URL")
    df = pd.read_csv(url, sep=sep)
    rows = df.to_numpy(na_value='')
    table = [list(row) for row in rows]
    ann_request.set_table(table)
    ann = mtab_client.annotate(ann_request.to_dict())
    if "semantic" not in ann.keys():
        raise HTTPException(status_code=400, detail="Dirty dataset")
    return ann["semantic"]


def annotate_dataframe(df: pd.DataFrame, ann:dict):
    cols = []
    ann_cols = ann["semantic"]['cpa']
    for index, col in enumerate(df.columns):
        try:
            cols.append(ONTOLOGY_URL + ann_cols[index][2])
        except Exception as e:
            cols.append('')
    df.columns = cols
    for col in df.columns:
        df[col] = RESOURCE_URL + df[col].replace(' ', '_', regex=True)
    return df


@router.post("/local")
def annotate_from_upload(file: UploadFile, fileres:bool, sep=","):
    ann_request = AnnotationRequest("table 2")
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=sep)
    rows = df.to_numpy(na_value='')
    table = [list(row) for row in rows]
    ann_request.set_table(table)
    ann = mtab_client.annotate(ann_request.to_dict())
    if "semantic" not in ann.keys():
        raise HTTPException(status_code=400, detail="Dirty dataset")
    df = annotate_dataframe(df, ann)
    if fileres == True:
        df.to_csv('datasets/dataset.csv')
        return FileResponse('datasets/dataset.csv')
    else:
        rows = df.to_numpy()
        table = [list(row) for row in rows]
        return table #ann["semantic"]