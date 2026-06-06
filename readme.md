# TaskFlow

Full-stack task management application with a FastAPI backend, PostgreSQL database,
React frontend, user authentication, tags, categories, and ML-assisted task
predictions.

## Run With Docker Compose

From the repository root:

```powershell
docker compose up --build
```

If your Docker installation uses the legacy Compose binary:

```powershell
docker-compose up --build
```

Services:

```text
Frontend: http://localhost:5173
Backend:  http://localhost:8000
API docs: http://localhost:8000/docs
ReDoc:    http://localhost:8000/redoc
Postgres: localhost:5432
```

The frontend container runs Vite in development mode and calls the backend through
`http://localhost:8000`.

## ML Model

TaskFlow uses an ML-assisted prediction flow to suggest a task category and
priority. The category prediction model was trained in a Kaggle notebook:

```text
https://www.kaggle.com/code/alexandruionutbaba/task-category-classification
```

The model is a scikit-learn pipeline that combines word-level TF-IDF features
with character-level TF-IDF features, then classifies the task category with
balanced Logistic Regression. Word n-grams help detect phrases such as `pay rent`,
while character n-grams help with short text, partial words, slang, and small
misspellings.

The backend uses the model as a suggestion system. Users can generate a
prediction, review the suggested category and priority, then choose whether to
apply one or both suggestions.

## Useful Commands

Run backend tests:

```powershell
docker compose exec backend pytest
```

Run migrations manually:

```powershell
docker compose exec backend alembic upgrade head
```

Rebuild only the frontend:

```powershell
docker compose build frontend
```
