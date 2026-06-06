import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <main className="not-found">
      <div>
        <h1>Page not found</h1>
        <p className="status-line">The route you opened does not exist.</p>
        <p className="auth-switch">
          <Link to="/dashboard">Back to dashboard</Link>
        </p>
      </div>
    </main>
  )
}
