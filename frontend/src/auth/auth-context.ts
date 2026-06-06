import { createContext, useContext } from 'react'

import type { User } from '../types/api'

interface LoginPayload {
  username: string
  password: string
}

interface RegisterPayload {
  username: string
  email: string
  password: string
}

export interface AuthContextValue {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  isLoadingUser: boolean
  login: (payload: LoginPayload) => Promise<void>
  register: (payload: RegisterPayload) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }

  return context
}
