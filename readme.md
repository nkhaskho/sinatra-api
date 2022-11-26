## Environment setup
Create a new virtual environment
``` shell
python -m venv env
```

Open the created virtual environment
``` shell
source env/bin/activate
```

Install FastApi with all it's dependencies (uvicorn,...)
``` shell
pip install "fastapi[all]"
```

Run the API in development mode
``` shell
uvicorn main:app --reload
```

## API documentation
API documentation will be available at http://127.0.0.1:8000/docs

