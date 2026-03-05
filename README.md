# gha-test

A minimal Flask application used as a learning tool for GitHub Actions.

## Application

`app.py` exposes a single endpoint:

```
GET /hello?name=<name>
```

Returns `{"message": "Hello, <name>!"}` on success, or a `400` JSON error if the
name is missing, blank, or not a string.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Running Tests

```bash
pytest
```
