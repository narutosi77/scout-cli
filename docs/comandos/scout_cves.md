# `scout cves`

El comando `scout cves` escanea una imagen Docker en busca de vulnerabilidades conocidas (CVEs).

## Uso Básico

```bash
scout cves [IMAGEN]
scout cves nginx:latest --severity CRITICAL,HIGH
scout cves myapp:latest --format sarif > cves-report.sarif
