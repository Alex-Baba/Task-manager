import { zodResolver } from '@hookform/resolvers/zod'
import { AxiosError } from 'axios'
import { LogIn } from 'lucide-react'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { z } from 'zod'

import { useAuth } from '../auth/auth-context'

const loginSchema = z.object({
  username: z.string().min(1, 'Username or email is required'),
  password: z.string().min(1, 'Password is required'),
})

type LoginForm = z.infer<typeof loginSchema>

export function LoginPage() {
  const { login } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [formError, setFormError] = useState<string | null>(null)
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { username: '', password: '' },
  })

  async function onSubmit(values: LoginForm) {
    try {
      setFormError(null)
      await login(values)
      const redirectTo =
        (location.state as { from?: { pathname?: string } } | null)?.from
          ?.pathname ?? '/dashboard'
      navigate(redirectTo, { replace: true })
    } catch (error) {
      const message =
        error instanceof AxiosError
          ? error.response?.data?.detail ?? 'Login failed'
          : 'Login failed'
      setFormError(message)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-hero">
        <div className="brand">
          <span className="brand-mark">
            <LogIn size={18} />
          </span>
          TaskFlow
        </div>
        <div>
          <h1>Organize work with smart task suggestions.</h1>
          <p>
            Create tasks, manage tags, and use model-generated predictions to
            decide category and priority faster.
          </p>
        </div>
      </section>
      <section className="auth-panel">
        <div className="auth-card">
          <h2>Sign in</h2>
          <p>Use your account to manage tasks and predictions.</p>

          <form className="form" onSubmit={handleSubmit(onSubmit)}>
            <div className="field">
              <label htmlFor="username">Username or email</label>
              <input id="username" autoComplete="username" {...register('username')} />
              {errors.username ? (
                <span className="error-text">{errors.username.message}</span>
              ) : null}
            </div>

            <div className="field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                autoComplete="current-password"
                {...register('password')}
              />
              {errors.password ? (
                <span className="error-text">{errors.password.message}</span>
              ) : null}
            </div>

            {formError ? <span className="error-text">{formError}</span> : null}

            <button className="button button-primary" disabled={isSubmitting}>
              <LogIn size={18} />
              Sign in
            </button>
          </form>

          <p className="auth-switch">
            No account yet? <Link to="/register">Create one</Link>
          </p>
        </div>
      </section>
    </main>
  )
}
