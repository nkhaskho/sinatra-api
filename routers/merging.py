import pandas as pd
from fastapi import APIRouter, UploadFile, HTTPException
from .models.dataset import Dataset

router = APIRouter(prefix="/merging", tags=["merging"])


@router.put("/local") # response_model=Dataset, 
def merge_from_local(dataset1: UploadFile, dataset2: UploadFile, separator: str, subject_col: str):
    """
    TODO: Adding API endpoint documentation
    TODO: Refactor endpoint to merge from remote
    """
    df1 = pd.read_csv(dataset1.file, sep=separator)
    df2 = pd.read_csv(dataset2.file, sep=separator)
    if subject_col=='' or subject_col==None:
        subject_col = df1.columns[0]
    if subject_col not in df1.columns or subject_col not in df2.columns:
        raise HTTPException(status_code=404, detail="Subject column missing") 
    df_result = pd.merge(df1, df2, how="outer", on=subject_col)
    df_result.fillna("", inplace=True)
    # TODO: Replace fillna by sparql fill
    ds_result = df_result.to_dict('index')
    return list(ds_result.values())