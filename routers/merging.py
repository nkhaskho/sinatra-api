import pandas as pd
from fastapi import APIRouter, UploadFile, HTTPException
from models.dataset import Dataset

router = APIRouter(prefix="/merging", tags=["merging"])


@router.put("/local") # response_model=Dataset, 
def merge_from_local(dataset1: UploadFile, dataset2: UploadFile, separator: str, subject_col: str=""):
    """
    TODO: Adding API endpoint documentation
    TODO: Refactor endpoint to merge from remote
    """
    df1 = pd.read_csv(dataset1.file, sep=separator)
    df2 = pd.read_csv(dataset2.file, sep=separator)
    if subject_col=='' or subject_col==None:
        subject_col = df1.columns[0]
    if subject_col in df2.columns and subject_col in df2.columns:
        df_result = pd.merge(df1, df2, how="outer", on=subject_col)
    else:
        # Check case 2 before
        s1 = set(df1[df1.columns[0]])
        s2 = set(df2[df2.columns[0]])
        if len(s1.intersection(s2))==0 and len(s2.intersection(s1))==0:
            raise HTTPException(status_code=404, detail="Subject column missmatch")
        else:
            df_result = pd.merge(df1, df2, "outer", left_on=df1.columns[0], right_on=df2.columns[0])
    df_result.fillna("", inplace=True)
    # TODO: Replace fillna by sparql fill
    ds_result = df_result.to_dict('index')
    return list(ds_result.values())