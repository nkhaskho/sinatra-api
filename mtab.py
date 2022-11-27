import requests

API_URL = "https://dbpedia.mtab.app/api/v1/mtab"

class AnnotationRequest:

    def __init__(self, table_name, search_limit=10, search_mode="b", round_id=2):
        self.table_name = table_name
        self.table = []
        self.tar_cea = None
        self.tar_cta = None
        self.tar_cpa = None
        self.search_limit = search_limit
        self.search_mode = search_mode
        self.round_id = round_id
        self.predict_target: True

    def set_table(self, data):
        self.table = data

    def from_csv(self, file):
        csv_file = open(file)
        for line in csv_file.readlines():
            self.table.append(line.split(','))

    def to_dict(self):
        return {
            "table_name": self.table_name,
            "table": self.table,
            "tar_cea": self.tar_cea,
            "tar_cta": self.tar_cta,
            "tar_cpa": self.tar_cpa,
            "search_limit": self.search_limit,
            "search_mode": self.search_mode,
            "round_id": self.round_id,
            "predict-target": "true"
        }
        

class MtabClient:

    def __init__(self):
        self.api_url = API_URL

    def annotate(self, request: AnnotationRequest):
        res = requests.post(self.api_url, json=request.to_dict())
        return res.json()