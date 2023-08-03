from utils import *
from fastapi import APIRouter, UploadFile
from .mtab import AnnotationRequest

router = APIRouter(prefix="/repair", tags=["augmentations"])


@router.put("/predict")
def predict_from_local(arg: str):
    """
    TODO: add dataset as input?
    Could be saved in browser's cache
    """
    sparqlres = predict_query(arg)
    print(sparqlres)
    return [pred['predicate'] for pred in sparqlres]


@router.put("/fill")
def fill_from_local(subject: str, item: str):
    """
    TODO: add dataset as input?
    Could be saved in browser's cache
    """
    sparqlres = fill_query(subject, item)
    print(sparqlres)
    return "ok"