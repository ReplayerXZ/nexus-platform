# Nexus Platform

A production-ready microservices platform built with Docker,
featuring automated CI/CD, centralized monitoring, and logging.

## Architecture

- **Auth Service** — Node.js · JWT authentication
- **User Service** — Go · User management REST API
- **Notification Service** — Python · Event-driven notifications
- **Worker Service** — Python · Background job processing

## Infrastructure

| Component | Purpose |
|---|---|
| Nginx | API Gateway & reverse proxy |
| PostgreSQL | Primary database |
| Redis | Cache & session store |
| RabbitMQ | Message queue |
| MongoDB | Notification history |
| Prometheus | Metrics collection |
| Grafana | Monitoring dashboard & logging |
| Loki | Log aggregation |

## Quick Start

\`\`\`bash
# Clone repository
git clone https://github.com/USERNAME/nexus-platform.git
cd nexus-platform

# Setup environment
cp .env.example .env

# Jalankan semua service
make up-build

# Lihat status
make ps

# Lihat logs
make logs
\`\`\`

## DevOps Highlights

- Multi-stage Docker builds untuk image yang ringan
- Automated CI/CD dengan GitHub Actions
- Centralized monitoring dengan Prometheus & Grafana
- Centralized logging dengan Loki
- Health checks & auto-restart pada semua service
- Secrets management dengan Docker secrets
\`\`\`