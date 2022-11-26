from fastapi import FastAPI, File, UploadFile
from mtab import *

app = FastAPI()


@app.get("/api/annotations/remote")
async def from_url(url: str):
    print(url)
    return {"file": url}


@app.post("/api/annotations/local")
async def from_upload(file: UploadFile):
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extention"}
    mtab_client = MtabClient()
    ann_request = AnnotationRequest()
    table = []
    for line in file.file.readlines():
        table.append((str(line))[:-1].split(","))
    ann_request.set_table(table)
    # print(ann_request.to_dict())
    ann = mtab_client.annotate(ann_request)
    return ann