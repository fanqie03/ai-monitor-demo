# AGENTS.md - AI Monitor Demo Project

## Project Overview

This is a Prometheus + Grafana monitoring demo that simulates third-party API calls and exposes Prometheus metrics for monitoring.

## Tech Stack

- **Python 3.11**: Main application (`app.py`)
- **Prometheus v2.40.0**: Time-series metrics database
- **Grafana 7.5.17**: Visualization dashboard
- **Docker Compose**: Container orchestration

## Commands

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Python app
python app.py

# Verify metrics endpoint
curl http://localhost:8000/metrics
```

### Docker Commands

```bash
# Build and start all services
docker-compose up -d

# Rebuild app after code changes
docker-compose build --no-cache app && docker-compose up -d

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop and remove containers
docker-compose down -v
```

### Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| App (Metrics) | http://localhost:8000/metrics | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin |

## Code Style Guidelines

### Python (app.py)

- **Shebang**: `#!/usr/bin/env python3` at top of executable files
- **Docstrings**: Use triple-quoted strings for module and public function docs
- **Imports**: Standard library first, then third-party, each group separated by blank line
  ```python
  import time
  import random
  import threading
  from http.server import HTTPServer, BaseHTTPRequestHandler
  from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
  ```
- **Constants**: UPPER_SNAKE_CASE naming (e.g., `THIRD_PARTY_APIS`, `API_CALLS_total`)
- **Functions**: snake_case naming with type hints for parameters and return values
- **Comments**: Chinese comments for business logic, English for technical terms
- **Line length**: Max 120 characters

### Prometheus Metrics Naming

- Counter metrics: `_total` suffix (e.g., `invoke_im_total`, not `invoke_im`)
- Histogram buckets: Use standard latency buckets `(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)`
- Labels: Use snake_case for label names (e.g., `api_name`, not `apiName`)

### Grafana Dashboard (api-monitor.json)

- **Datasource**: Use string format `"datasource": "prometheus"` (not object format) for Grafana 7.x compatibility
- **Aggregation**: Use `sum without (instance)` for multi-Pod scenarios to aggregate metrics correctly
- **Panel IDs**: Must be unique integers
- **YAML configs**: Use proper YAML syntax, not JSON (e.g., `datasources.yml`)

### Docker/Compose

- Image tags should specify exact versions (e.g., `grafana/grafana:7.5.17`, not `grafana/grafana:latest`)
- Use `unless-stopped` for restart policy
- Use descriptive container names

## Git Conventions

- Commit message format: `<type>: <description>`
  - Types: `feat`, `fix`, `chore`, `docs`, `refactor`
- Example: `feat: add invokeHis histogram metric for service API monitoring`

## Adding New Metrics

1. Define metric in `app.py` using Counter or Histogram
2. Add simulation logic in `background_simulator()`
3. Add corresponding Grafana panel in `api-monitor.json`
4. Use `sum without (instance)` for aggregation queries

## File Structure

```
├── app.py                    # Python metrics exporter
├── Dockerfile.app            # App container definition
├── docker-compose.yml        # Service orchestration
├── prometheus.yml            # Prometheus scrape config
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
└── grafana/
    └── provisioning/
        ├── dashboards/
        │   └── dashboards/
        │       └── api-monitor.json  # Grafana dashboard
        └── datasources/
            └── datasources.yml      # Prometheus datasource
```
