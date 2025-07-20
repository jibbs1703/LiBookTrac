FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/jibbs1703/LiBookTrac"

WORKDIR /workspace

RUN useradd -ms /bin/bash jibbs-user

RUN chown -R jibbs-user:jibbs-user /workspace

USER jibbs-user

COPY . /workspace

ENV PATH="/home/jibbs-user/.local/bin:${PATH}"

RUN pip install --no-cache-dir -r /workspace/backend/requirements.txt

CMD ["uvicorn", "backend.v1.app.server.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]