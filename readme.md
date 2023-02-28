## Get source code
Clone the source code from remote github repository
``` shell
git clone https://github.com/nkhaskho/sinatra-api.git
```

## Environment setup
Create a new virtual environment
``` shell
python -m venv env
```

Open the created virtual environment
``` shell
source env/bin/activate
```

Install required modules
``` shell
pip install -r requirements.txt
```

## Run the Web API

Run the API in development mode
``` shell
uvicorn main:app --reload
```

## API documentation
API documentation will be available at: <br>
http://127.0.0.1:8000/docs

