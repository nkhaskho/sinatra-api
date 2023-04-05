from typing import List

from pydantic import BaseModel


class Dataset(BaseModel):
    headers: List[str] = []
    records: List[object] = []


class DatasetAnalytics(BaseModel):
    columns: int
    rows: int
    nacount: int
    duplicates: int
    spechars: int
    binaries: int
    headers: List[str] = []