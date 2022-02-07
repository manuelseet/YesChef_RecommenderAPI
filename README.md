# YesChef_RecommenderAPI

## Components
- Flask API (Python) exposing endpoints in `api_server.py`
- Tester Spring Boot App to consume ML outputs

## Dependencies
The API has the following dependencies:
```
Flask
atexit
pandas
spacy
pattern
APScheduler
requests
json
```

Named Entity Recognition (Part of Speech Tagging) is done for feature vectorization:
To support this, download `en_core_web_sm` as follows:
```python -m spacy download en_core_web_sm```

## Launching the Flask API
1. Navigate to the working directory containing the flask API, via `cd` in command prompt
2. Launch the API via `python api_server.py`
3. Confirm that the API is active, with the following message: `* Running on http://127.0.0.1:5000/`
