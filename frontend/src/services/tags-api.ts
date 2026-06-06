import { api } from '../lib/api'
import type { Tag } from '../types/api'

export async function getTags() {
  const response = await api.get<Tag[]>('/tags')
  return response.data
}

export async function createTag(name: string) {
  const response = await api.post<Tag>('/tags', { name })
  return response.data
}

export async function updateTag(tagId: string, name: string) {
  const response = await api.patch<Tag>(`/tags/${tagId}`, { name })
  return response.data
}

export async function deleteTag(tagId: string) {
  await api.delete(`/tags/${tagId}`)
}
