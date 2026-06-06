import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Navigate } from 'react-router-dom'

import { useAuth } from '../auth/auth-context'
import { AdminCategoryForm } from '../components/admin/AdminCategoryForm'
import { AdminUsersTable } from '../components/admin/AdminUsersTable'
import { ConfirmDialog } from '../components/common/ConfirmDialog'
import {
  createCategory,
  deleteUser,
  getAdminUsers,
  grantAdmin,
  revokeAdmin,
} from '../services/admin-api'
import { getCategories } from '../services/categories-api'
import type { AdminUser } from '../types/api'

export function AdminPage() {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [userPendingDelete, setUserPendingDelete] = useState<AdminUser | null>(null)

  const usersQuery = useQuery({
    queryKey: ['admin-users'],
    queryFn: getAdminUsers,
    enabled: Boolean(user?.is_admin),
  })
  const categoriesQuery = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  })

  const grantAdminMutation = useMutation({
    mutationFn: grantAdmin,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['admin-users'] })
    },
  })

  const revokeAdminMutation = useMutation({
    mutationFn: revokeAdmin,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['admin-users'] })
      void queryClient.invalidateQueries({ queryKey: ['current-user'] })
    },
  })

  const deleteUserMutation = useMutation({
    mutationFn: deleteUser,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['admin-users'] })
    },
  })

  const createCategoryMutation = useMutation({
    mutationFn: createCategory,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['categories'] })
    },
  })

  if (!user?.is_admin) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <h1>Admin</h1>
          <p>Manage users, admin access, and reference categories.</p>
        </div>
      </header>

      <section className="admin-grid">
        <section className="panel">
          <h2>Users</h2>
          <p className="panel-subtitle">
            Grant admin access, revoke it, or remove users.
          </p>

          <AdminUsersTable
            currentUserId={user.id}
            isDeletePending={deleteUserMutation.isPending}
            isGrantPending={grantAdminMutation.isPending}
            isRevokePending={revokeAdminMutation.isPending}
            users={usersQuery.data ?? []}
            onDelete={setUserPendingDelete}
            onGrantAdmin={(userId) => grantAdminMutation.mutate(userId)}
            onRevokeAdmin={(userId) => revokeAdminMutation.mutate(userId)}
          />

          {usersQuery.isLoading ? <p className="status-line">Loading users...</p> : null}
          {usersQuery.isError ? (
            <p className="error-text">Could not load admin users.</p>
          ) : null}
        </section>

        <aside className="panel">
          <h2>Categories</h2>
          <p className="panel-subtitle">
            Create missing reference categories if the seed script was not run.
          </p>

          <AdminCategoryForm
            categories={categoriesQuery.data ?? []}
            isError={createCategoryMutation.isError}
            isPending={createCategoryMutation.isPending}
            onCreateCategory={(name) => createCategoryMutation.mutate(name)}
          />
        </aside>
      </section>

      {userPendingDelete ? (
        <ConfirmDialog
          confirmLabel="Delete user"
          description={
            <>
              This will permanently remove <strong>{userPendingDelete.username}</strong>{' '}
              and all related tasks, tags, and predictions.
            </>
          }
          isPending={deleteUserMutation.isPending}
          title="Delete user?"
          onCancel={() => setUserPendingDelete(null)}
          onConfirm={() => deleteUserMutation.mutate(userPendingDelete.id)}
        />
      ) : null}
    </main>
  )
}
