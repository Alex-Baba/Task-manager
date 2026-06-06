import { api } from '../lib/api'
import type { Category } from '../types/api'

export async function getCategories() {
  const response = await api.get<Category[]>('/categories')
  return response.data
}
