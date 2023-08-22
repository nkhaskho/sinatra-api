import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile
from .mtab import *
from models.dataset import *


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


@router.post("/local")
def annotate_from_upload(file: UploadFile, sep=","):
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
    return ann["semantic"]