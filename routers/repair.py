from utils import sparql_query
from fastapi import APIRouter, UploadFile
from .mtab import AnnotationRequest

router = APIRouter(prefix="/repair", tags=["augmentations"])


@router.put("/local")
def repair_from_local(arg: str):
    """
    TODO: add dataset as input?
    Could be saved in browser's cache
    """
    
    sparqlres = sparql_query(arg)
    return [pred['predicate'] for pred in sparqlres]