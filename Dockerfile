FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY conocimiento ./conocimiento
RUN pip install --no-cache-dir ".[web,claude]" \
    && useradd --create-home pymentor && mkdir -p /app/.cache && chown pymentor /app/.cache

ENV PAITHON_CONOCIMIENTO=/app/conocimiento \
    PAITHON_CACHE=/app/.cache/embeddings.sqlite
USER pymentor
EXPOSE 8000
CMD ["paithon", "web", "--host", "0.0.0.0", "--puerto", "8000"]
