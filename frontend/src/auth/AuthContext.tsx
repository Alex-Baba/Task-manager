import { useMemo, useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'

import { clearStoredToken, getStoredToken, storeToken } from '../lib/api'
import {
  getCurrentUser,
  loginUser,
  registerUser,
} from '../services/auth-api'
import { AuthContext, type AuthContextValue } from './auth-context'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const queryClient = useQueryClient()
  const [token, setToken] = useState(() => getStoredToken())

  const currentUserQuery = useQuery({
    queryKey: ['current-user'],
    queryFn: getCurrentUser,
    enabled: Boolean(token),
  })

  const value = useMemo<AuthContextValue>(
    () => ({
      token,
      user: currentUserQuery.data ?? null,
      isAuthenticated: Boolean(token),
      isLoadingUser: currentUserQuery.isLoading,
      login: async (payload) => {
        const response = await loginUser(payload)
        storeToken(response.access_token)
        setToken(response.access_token)
        await queryClient.invalidateQueries({ queryKey: ['current-user'] })
      },
      register: async (payload) => {
        await registerUser(payload)
      },
      logout: () => {
        clearStoredToken()
        setToken(null)
        queryClient.clear()
      },
    }),
    [currentUserQuery.data, currentUserQuery.isLoading, queryClient, token],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
