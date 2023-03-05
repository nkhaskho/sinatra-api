import pandas as pd
from fastapi import APIRouter, UploadFile, Body
from .models.dataset import Dataset

router = APIRouter(prefix="/merging", tags=["merging"])


@router.put("/local") # response_model=Dataset, 
def merge_from_local(dataset1: UploadFile, dataset2: UploadFile):
    """
    TODO: Impl
    """
    df1 = pd.read_csv(dataset1.file, sep=";")
    df2 = pd.read_csv(dataset2.file, sep=";")
    ds_result = Dataset(headers=[], records=[])
    return ds_result