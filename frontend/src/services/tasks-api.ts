import { api } from '../lib/api'
import type { Priority, Status, Task } from '../types/api'

export interface CreateTaskPayload {
  title: string
  description?: string
  category_id?: string
  due_date?: string
  manual_priority: Priority
  tag_ids: string[]
}

export interface UpdateTaskPayload {
  title: string
  description: string | null
  category_id: string | null
  due_date: string | null
  manual_priority: Priority
  status: Status
}

export async function getTasks() {
  const response = await api.get<Task[]>('/tasks')
  return response.data
}

export async function createTask(payload: CreateTaskPayload) {
  const response = await api.post<Task>('/tasks', payload)
  return response.data
}

export async function updateTask(taskId: string, payload: UpdateTaskPayload) {
  const response = await api.patch<Task>(`/tasks/${taskId}`, payload)
  return response.data
}

export async function updateTaskStatus(taskId: string, status: Status) {
  const response = await api.patch<Task>(`/tasks/${taskId}`, { status })
  return response.data
}

export async function completeTask(taskId: string) {
  const response = await api.patch<Task>(`/tasks/${taskId}`, {
    status: 'COMPLETED',
  })
  return response.data
}

export async function deleteTask(taskId: string) {
  await api.delete(`/tasks/${taskId}`)
}

export async function attachTagToTask(taskId: string, tagId: string) {
  const response = await api.post<Task>(`/tasks/${taskId}/tags/${tagId}`)
  return response.data
}

export async function removeTagFromTask(taskId: string, tagId: string) {
  const response = await api.delete<Task>(`/tasks/${taskId}/tags/${tagId}`)
  return response.data
}
