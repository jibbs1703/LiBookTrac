# Libooktrac Backend Roadmap

This file is intended to track my progress in adding features to this backend project.
Think of this as a way to keep my self honest while _slowly_ building out this backend
to sharpen my FastAPI skills. 


## TODO List

- use isbn check to input book details (external API exists)


# Libooktrac Bakend Command Snippet

- **Run Library Management Application Locally:**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8008
```

- **Run Library Management Application in Container:**
```bash
docker build -f backend.Dockerfile -t libooktrac:latest .
docker rm -f libooktrac-env || true # Remove existing container if it exists
docker run -it --name libooktrac-env -v .:/workspace -p 8000:8000 libooktrac:latest
docker exec -it libooktrac-env sh
```