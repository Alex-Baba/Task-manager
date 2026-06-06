import { Shield, ShieldOff, Trash2 } from 'lucide-react'

import type { AdminUser } from '../../types/api'

interface AdminUsersTableProps {
  currentUserId: string
  isDeletePending: boolean
  isGrantPending: boolean
  isRevokePending: boolean
  users: AdminUser[]
  onDelete: (user: AdminUser) => void
  onGrantAdmin: (userId: string) => void
  onRevokeAdmin: (userId: string) => void
}

export function AdminUsersTable({
  currentUserId,
  isDeletePending,
  isGrantPending,
  isRevokePending,
  onDelete,
  onGrantAdmin,
  onRevokeAdmin,
  users,
}: AdminUsersTableProps) {
  return (
    <div className="table-wrap">
      <table className="admin-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((adminUser) => {
            const isCurrentUser = adminUser.id === currentUserId

            return (
              <tr key={adminUser.id}>
                <td>{adminUser.username}</td>
                <td>{adminUser.email}</td>
                <td>
                  <span className="badge">
                    {adminUser.is_admin ? 'Admin' : 'User'}
                  </span>
                </td>
                <td>{formatOptionalDate(adminUser.created_at)}</td>
                <td>
                  <div className="row-actions">
                    {adminUser.is_admin ? (
                      <button
                        className="button button-secondary"
                        disabled={isCurrentUser || isRevokePending}
                        title={
                          isCurrentUser
                            ? 'You cannot revoke your own admin access'
                            : undefined
                        }
                        type="button"
                        onClick={() => onRevokeAdmin(adminUser.id)}
                      >
                        <ShieldOff size={16} />
                        Revoke
                      </button>
                    ) : (
                      <button
                        className="button button-secondary"
                        disabled={isGrantPending}
                        type="button"
                        onClick={() => onGrantAdmin(adminUser.id)}
                      >
                        <Shield size={16} />
                        Grant
                      </button>
                    )}
                    <button
                      className="button button-danger"
                      disabled={isCurrentUser || isDeletePending}
                      title={
                        isCurrentUser
                          ? 'You cannot delete your own account'
                          : undefined
                      }
                      type="button"
                      onClick={() => onDelete(adminUser)}
                    >
                      <Trash2 size={16} />
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function formatOptionalDate(value?: string) {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}
