FROM smrati/python-uv-slim-bookworm:3.13

EXPOSE 8000

# Create app directory
WORKDIR /app
COPY quick-data-mcp/pyproject.toml /app/
RUN uv sync
COPY quick-data-mcp/ /app

ENTRYPOINT ["uv", "run"]

CMD ["fastmcp", "run", "main.py", "--transport", "http"]

