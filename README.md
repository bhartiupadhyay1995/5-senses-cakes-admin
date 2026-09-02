# 5 Senses Cakes — Business Management Application

A personalized web application for managing a small made-to-order cake business, including inventory, recipes, orders, and profitability analysis.

## Quick Start

### Prerequisites

- Git
- Docker Desktop

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd 5-senses-cakes
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Start the application:
   ```bash
   docker compose up
   ```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Project Structure

```
5-senses-cakes/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── database.py     # Database connection
│   │   └── main.py         # FastAPI app initialization
│   ├── alembic/            # Database migrations
│   ├── tests/              # Pytest tests
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile
│   └── README.md
│
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   ├── hooks/          # Custom hooks
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/             # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   ├── tailwind.config.js
│   └── README.md
│
├── docs/                   # Documentation
│   ├── PHASE_1_REQUIREMENTS_AND_ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   ├── API_SPECIFICATION.md (coming)
│   └── FRONTEND_WIREFRAMES.md (coming)
│
├── docker-compose.yml      # Container orchestration
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
npm run build
```

## Database

The application uses PostgreSQL. When running with `docker compose up`, a PostgreSQL container is automatically created and initialized.

To manually apply migrations:
```bash
cd backend
alembic upgrade head
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### End-to-End Tests

```bash
cd frontend
npm run test:e2e
```

## Documentation

- [Phase 1: Requirements and Architecture](docs/PHASE_1_REQUIREMENTS_AND_ARCHITECTURE.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)

## Development Phases

- **Phase 1**: Requirements and architecture ✓
- **Phase 2**: Database design and implementation
- **Phase 3**: Backend API development
- **Phase 4**: Frontend UI development
- **Phase 5**: Testing and refinement
- **Phase 6**: Local deployment with Docker

## Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL 14+
- **Testing**: Pytest, Playwright
- **Deployment**: Docker Compose

## License

MIT

