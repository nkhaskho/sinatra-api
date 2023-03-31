import pandas as pd
from fastapi import APIRouter, UploadFile
from .mtab import *
from .models.dataset import *


router = APIRouter(prefix="/annotations", tags=["annotations"])

mtab_client = MtabClient()


@router.get("/remote")
async def annotate_from_url(url: str):
    ann_request = AnnotationRequest("From-URL")
    """
    for line in urllib.request.urlopen(url): # .read(10); read only 20 000 chars
        table.append(line.decode('utf-8')[:-1].split(","))
    """
    df = pd.read_csv(url, sep=";")
    rows = df.to_numpy(na_value='')
    table = [list(row) for row in rows]
    ann_request.set_table(table)
    ann = mtab_client.annotate(ann_request.to_dict())
    if "semantic" in ann.keys(): # {"table": table}
        return {"res": ann["semantic"]} 
    return ann


@router.post("/local")
def annotate_from_upload(file: UploadFile):
    ann_request = AnnotationRequest("table 2")
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    df = pd.read_csv(file.file, sep=";")
    rows = df.to_numpy(na_value='')
    table = [list(row) for row in rows]
    ann_request.set_table(table)
    ann = mtab_client.annotate(ann_request.to_dict())
    #print(ann_request.to_dict())
    #semantic = annotation["semantic"]
    if "semantic" in ann.keys():
        return {"res": ann["semantic"]}
    return ann

