from fastapi import FastAPI, UploadFile
import pandas as pd
import numpy as np
from mtab import *
import urllib.request


app = FastAPI(
    title="Sinatra API",
    description="Mtab annotation from local or remote dataset",
    version="0.0.1"
)

mtab_client = MtabClient()


@app.get("/api/annotations/remote", tags=["annotations"])
async def annotate_from_url(url: str):
    table = []
    ann_request = AnnotationRequest("table 1")
    for line in urllib.request.urlopen(url): # .read(10); read only 20 000 chars
        table.append(line.decode('utf-8')[:-1].split(","))
    annotation = mtab_client.annotate(ann_request)
    return annotation


@app.post("/api/annotations/local", tags=["annotations"])
def annotate_from_upload(file: UploadFile):
    table = []
    ann_request = AnnotationRequest("table 2")
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    # todo: load file with pandas
    df = pd.read_csv(file.file)
    # dealing with missing data -> drop row
    df = df.dropna(0)
    rows = df.to_numpy()
    table.append(list(df.columns.values))
    for row in rows:
        table.append(list(row))
    print(table)
    ann_request.set_table(table)
    ann = mtab_client.annotate(ann_request.to_dict())
    #print(ann_request.to_dict())
    #semantic = annotation["semantic"]
    return {"res": ann} #{"table": table}