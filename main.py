from fastapi import FastAPI, UploadFile
import pandas as pd
from mtab import *
from utils import sparql_query
import urllib.request
from fastapi.openapi.utils import get_openapi


app = FastAPI(title="Sinatra API")

mtab_client = MtabClient()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sinatra API",
        version="1.0",
        description="Sinatra API docs and schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/api/annotations/remote", tags=["annotations"])
async def annotate_from_url(url: str):
    if app.openapi_schema:
       return app.openapi_schema
    table = []
    ann_request = AnnotationRequest("table 1")
    for line in urllib.request.urlopen(url): # .read(10); read only 20 000 chars
        table.append(line.decode('utf-8')[:-1].split(","))
    annotation = mtab_client.annotate(ann_request)
    return annotation


@app.post("/api/annotations/local", tags=["annotations"])
def annotate_from_upload(file: UploadFile):
    if app.openapi_schema:
       return app.openapi_schema
    table = []
    ann_request = AnnotationRequest("table 2")
    if not file.filename.endswith('.csv'):
        return {"error": "invalid file extension"}
    # todo: load file with pandas
    df = pd.read_csv(file.file)
    # dealing with missing data -> drop row
    print(df)
    df = df.dropna(0)
    print(df)
    rows = df.to_numpy()
    table.append(list(df.columns.values))
    for row in rows:
        table.append(list(row))
    print(table)
    ann_request.set_table(table)
    ann = mtab_client.annotate(ann_request.to_dict())
    #print(ann_request.to_dict())
    #semantic = annotation["semantic"]
    if "semantic" in ann.keys():
        return {"res": ann["semantic"]} #{"table": table}
    return ann


@app.put("/api/augmentations", tags=["augmentations"])
def augmentate_from_upload(column: str):
    """
    TODO: add dataset as input?
    Could be saved in browser's cache
    """
    return sparql_query(column)


def get_uri(name: str):
    resource_url = "http://dbpedia.org/resource/"
    ontology_url = "http://dbpedia.org/ontology/"
    return resource_url + name.replace(" ", "_")


