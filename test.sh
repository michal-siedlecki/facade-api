#!/bin/bash
docker compose up -d &&
docker exec -it facade-public-1 /bin/bash -c "source venv/bin/activate && pytest -v" &&
docker compose down
