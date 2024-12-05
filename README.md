# Backend Testing Framework

This repository contains an automated testing framework for any backend platform. 
It uses Python with pytest to perform API testing, including smoke tests and sanity checks.

## Project Structure

```
pytest-api/
├── api/
│   ├── __init__.py
│   └── endpoints.py
├── payload_data/
│   ├── __init__.py
│   └── payload_data.py
├── loadtests/
│   ├── __init__.py
│   └── locustfile.py
├── utils/
│   ├── __init__.py
│   ├── http_client.py
│   └── schema_validator.py
├── tests/
│   ├── __init__.py
│   └── test_sample.py
├── schemas/
│   ├── sample_schema.json
├── reports/
│   └── .gitkeep
├── config.py
├── conftest.py
├── pytest.ini
├── setup.py
├── requirements.txt
├── .env
└── README.md
```

## Setup

1. Clone the repository:

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install the project in editable mode:
   ```
   pip install -e .
   ```

5. Copy `.env.example` to `.env` and update the variables as needed:
   ```
   cp .env.example .env
   ```

## Running Tests

To run all tests:
```
pytest
```

To run smoke tests:
```
pytest -m smoke
```

To run sanity tests:
```
pytest -m sanity
```

To generate an HTML report:
```
pytest --html=reports/report.html
```

To Run in Parallel Mode and generate the HTML report:
```
pytest -m smoke --html=reports/report.html -n 6
```

``NOTE: We use pytest-rerunfailures & pytest-xdist plugins to Run in parallel mode and retry on failures``

To Run in Parallel Mode and generate the Allures report:
```
pytest -m sanity -n 6 --alluredir=allure-results OR pytest --alluredir=allure-results
allure serve allure-results
```
