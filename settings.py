# Sinatra API version
API_VERSION = 1

# Mtab API URL
MTAB_API_URL = "http://mtab4d.kgraph.jp/api/v1/mtab"


RESOURCE_URL = "http://dbpedia.org/resource/" # column value
ONTOLOGY_URL = "http://dbpedia.org/ontology/" # column name

# Specials characters
SPECIAL_CHARS = ['@', '(', ')', '!']

# Spec chars encoding
SPEC_CHARS_DICT = {
    r'.*\?.*': '',
    r'.*\!.*': ''
}

# Binaries data
BIN_CHARS = ['y', 'n', 't', 'f', 'y', 'y.', 'n.', 't.', 'f.']

# special null values
SPECIAL_NULLS = ['null', 'Nan', 'nan', 'nil', '?']

# Abbreviations
ABBREVS = {
    "y": 'yes',
    "n": 'no',
    "m": 'male',
    "f": 'femal',
    "nn": 'naninne',
    "ch": 'champion',
}