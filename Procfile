web: gunicorn --workers 3 --bind 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker --log-level debug app.main:app
