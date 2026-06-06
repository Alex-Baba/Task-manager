import { api } from '../lib/api'
import type { AdminUser, Category, CategoryName } from '../types/api'

export async function getAdminUsers() {
  const response = await api.get<AdminUser[]>('/admin/users')
  return response.data
}

export async function grantAdmin(userId: string) {
  await api.post(`/admin/users/${userId}/admin`)
}

export async function revokeAdmin(userId: string) {
  await api.delete(`/admin/users/${userId}/admin`)
}

export async function deleteUser(userId: string) {
  await api.delete(`/admin/users/${userId}`)
}

export async function createCategory(name: CategoryName) {
  const response = await api.post<Category>('/admin/categories', { name })
  return response.data
}
