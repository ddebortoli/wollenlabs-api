# URL Health Checker

A modern web application for checking the health and availability of multiple URLs in parallel. Built with Django, Celery, Redis, and React.

## Features

- ✨ Check multiple URLs simultaneously
- 🚀 Asynchronous processing with real-time progress
- 💾 Caching of successful results
- 🔄 Automatic retries with exponential backoff
- 📊 Detailed error categorization
- 📈 Real-time task monitoring with Flower
- 🎯 Process URLs in optimized chunks
- ⚡ Fast response times with Redis caching

## Tech Stack

### Backend
- Django + Django REST Framework
- Celery for async task processing
- Redis for caching and message broker
- SQLite for development database

### Frontend
- React with TypeScript
- Material-UI components
- Axios for HTTP requests

### DevOps
- Docker and Docker Compose
- Flower for Celery monitoring

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd url-health-checker
```

2. Start the services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Flower (Celery monitoring): http://localhost:5555

## API Endpoints

### Check URLs
```http
POST /api/url-checks/check_urls/
Content-Type: application/json

{
    "urls": [
        "https://example.com",
        "https://google.com"
    ]
}
```

### Get Batch Status
```http
GET /api/url-checks/batch_status/?batch_id=<batch_id>
```

### Get Batch Results
```http
GET /api/url-checks/batch_results/?batch_id=<batch_id>
```

## Architecture

The application follows a microservices architecture with the following components:

- **Frontend Service**: React SPA for user interaction
- **Backend Service**: Django/DRF API
- **Celery Workers**: Async task processing
- **Redis**: Message broker and cache
- **Flower**: Task monitoring

## Error Handling

The system handles various types of errors:
- DNS resolution failures
- SSL certificate errors
- Connection timeouts
- Too many redirects
- Server errors (4xx, 5xx)

## Development

### Project Structure
```
├── backend/
│   ├── api/
│   │   ├── models.py      # Data models
│   │   ├── serializers.py # API serializers
│   │   ├── tasks.py       # Celery tasks
│   │   └── views.py       # API endpoints
│   └── url_health_checker/
│       └── settings.py    # Django settings
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API clients
│   │   └── types/        # TypeScript types
└── docker-compose.yml     # Service orchestration
```

### Running Tests
```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests
docker-compose exec frontend npm test
```

## Performance Optimizations

- URLs are processed in chunks of 10
- Successful results are cached for 5 minutes
- Celery workers process tasks in parallel
- Frontend implements smart polling
- Redis caching reduces database load

## Monitoring

Access Flower dashboard at http://localhost:5555 to monitor:
- Active tasks
- Task history
- Worker status
- Queue metrics

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Celery](https://docs.celeryproject.org/)
- [React](https://reactjs.org/)
- [Material-UI](https://material-ui.com/)