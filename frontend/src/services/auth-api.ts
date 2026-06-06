import { api } from '../lib/api'
import type { TokenResponse, User } from '../types/api'

export interface LoginPayload {
  username: string
  password: string
}

export interface RegisterPayload {
  username: string
  email: string
  password: string
}

export async function getCurrentUser() {
  const response = await api.get<User>('/auth/me')
  return response.data
}

export async function loginUser({ username, password }: LoginPayload) {
  const formData = new URLSearchParams()
  formData.set('username', username)
  formData.set('password', password)

  const response = await api.post<TokenResponse>('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export async function registerUser(payload: RegisterPayload) {
  await api.post('/users', payload)
}
