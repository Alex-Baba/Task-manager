import { CheckSquare, LogOut } from 'lucide-react'
import { Link, Outlet } from 'react-router-dom'

import { useAuth } from '../auth/auth-context'

export function AppShell() {
  const { logout, user } = useAuth()

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">
            <CheckSquare size={19} />
          </span>
          TaskFlow
        </div>
        <div className="topbar-actions">
          <Link className="button button-ghost" to="/dashboard">
            Dashboard
          </Link>
          {user?.is_admin ? (
            <Link className="button button-ghost" to="/admin">
              Admin
            </Link>
          ) : null}
          {user ? (
            <span className="user-chip">
              {user.username}
              {user.is_admin ? ' · admin' : ''}
            </span>
          ) : null}
          <button className="button button-ghost" type="button" onClick={logout}>
            <LogOut size={17} />
            Logout
          </button>
        </div>
      </header>
      <Outlet />
    </div>
  )
}
