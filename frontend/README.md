# Frontend

React + TypeScript + Vite frontend for TaskFlow, a task management application
with authentication, user-owned tasks and tags, category filters, dashboard
insights, and ML-assisted task predictions.

## Tech Stack

- React
- TypeScript
- Vite
- React Router
- TanStack Query
- React Hook Form
- Zod
- Axios
- Lucide React icons

## Main Features

- Register and login flow with JWT-backed API access
- Protected dashboard route
- Task creation, editing, completion, cancellation, and deletion
- Category, status, priority, due date, and tag filters
- Clickable dashboard overview cards
- Tag management with search, create, edit, delete, and attach-to-task flows
- ML prediction flow with generate, review, apply, and dismiss actions
- Admin navigation when the authenticated user has admin access
- Docker-based development service with Vite hot reload

## Local Development

Install dependencies:

```powershell
npm install
```

Start the Vite development server:

```powershell
npm run dev
```

The app expects the backend URL in:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Default local URL:

```text
http://localhost:5173
```

## Docker

The root `docker-compose.yml` includes the frontend service. From the repository
root:

```powershell
docker compose up --build
```

Frontend URL:

```text
http://localhost:5173
```

The container runs Vite in development mode. File watching uses polling through
`CHOKIDAR_USEPOLLING=true`, which makes hot reload work reliably with Docker
bind mounts on Windows.

## Project Structure

```text
src/
  auth/          authentication context and route protection
  components/    shared UI, task forms/cards, tag management
  layout/        authenticated app shell and navigation
  lib/           configured API client
  pages/         login, register, dashboard, admin, not found
  services/      API request modules
  types/         shared frontend API types
```

## API Integration

The Axios client reads `VITE_API_BASE_URL` and attaches the stored JWT token to
authenticated requests.

Important API areas used by the frontend:

```text
/auth
/users
/admin
/categories
/tags
/tasks
/tasks/{task_id}/predictions
```

## Checks

```powershell
npm run lint
npm run build
```

Run these before committing frontend changes.
