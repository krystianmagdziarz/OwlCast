# OwlCast

OwlCast is a high-performance, scalable, AI-supported web analytics service that collects and analyzes website statistics in real-time.

## Features

- Real-time statistics collection and analysis
- Horizontal scalability
- Privacy-focused design
- Support for cached and static pages
- REST API for data access
- Flexible dashboard integration capabilities

### Metrics Collected

- Page views and unique visitors
- Bounce rate
- Average time on page
- Scroll depth
- Device type (mobile/desktop)
- Referrer information
- User agent details
- Screen size
- Language preferences
- Geographical data (country, city)
- ISP information

## Tech Stack

- **Backend**: FastAPI
- **Databases**:
  - ClickHouse (statistics storage)
  - Redis (caching)
- **Task Queue**: Celery
- **Deployment**: Docker Compose
- **Web Server**: Nginx

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10 or higher
- Node.js 18 or higher (for client development)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/statcollector.git
cd statcollector
```

2. Create and configure environment variables:

```bash
cp .env.example .env
```

3. Start the development environment:

```bash
docker-compose -f local.yml up -d
```

## Client Integration

Add the following script to your website:

```html
<script src="https://cdn.statcollector.com/collector.js"></script>
<script>
	StatCollector.init("YOUR_API_KEY");
</script>
```

## Development

### Development Setup

1. Install development dependencies:

```bash
pip install -r requirements.txt
```

2. Install client dependencies:

```bash
cd client
npm install
```

### Code Quality

The project uses:

- Black for code formatting
- isort for import sorting
- flake8 for code linting
- mypy for type checking

### Running Tests

```bash
pytest
```

## API Documentation

API documentation is available at `/docs` when running the service locally.

### Key Endpoints

- `POST /api/v1/statistics` - Submit statistics
- `GET /api/v1/statistics/{domain}` - Get domain statistics
- `GET /api/v1/statistics/{domain}/{page}` - Get page statistics
- `GET /api/v1/statistics/chart` - Get chart data
