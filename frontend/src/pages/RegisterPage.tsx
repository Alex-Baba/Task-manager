import { zodResolver } from '@hookform/resolvers/zod'
import { AxiosError } from 'axios'
import { UserPlus } from 'lucide-react'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import { z } from 'zod'

import { useAuth } from '../auth/auth-context'

const registerSchema = z.object({
  username: z.string().min(3, 'Username must have at least 3 characters'),
  email: z.email('Enter a valid email'),
  password: z.string().min(8, 'Password must have at least 8 characters'),
})

type RegisterForm = z.infer<typeof registerSchema>

export function RegisterPage() {
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()
  const [formError, setFormError] = useState<string | null>(null)
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
    defaultValues: { username: '', email: '', password: '' },
  })

  async function onSubmit(values: RegisterForm) {
    try {
      setFormError(null)
      await registerUser(values)
      navigate('/login', { replace: true })
    } catch (error) {
      const message =
        error instanceof AxiosError
          ? error.response?.data?.detail ?? 'Registration failed'
          : 'Registration failed'
      setFormError(message)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-hero">
        <div className="brand">
          <span className="brand-mark">
            <UserPlus size={18} />
          </span>
          TaskFlow
        </div>
        <div>
          <h1>Build a focused task workspace.</h1>
          <p>
            Register an account and keep your tasks, tags, and prediction
            history scoped to your own user.
          </p>
        </div>
      </section>
      <section className="auth-panel">
        <div className="auth-card">
          <h2>Create account</h2>
          <p>Start with a username, email, and secure password.</p>

          <form className="form" onSubmit={handleSubmit(onSubmit)}>
            <div className="field">
              <label htmlFor="username">Username</label>
              <input id="username" autoComplete="username" {...register('username')} />
              {errors.username ? (
                <span className="error-text">{errors.username.message}</span>
              ) : null}
            </div>

            <div className="field">
              <label htmlFor="email">Email</label>
              <input id="email" autoComplete="email" {...register('email')} />
              {errors.email ? (
                <span className="error-text">{errors.email.message}</span>
              ) : null}
            </div>

            <div className="field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                autoComplete="new-password"
                {...register('password')}
              />
              {errors.password ? (
                <span className="error-text">{errors.password.message}</span>
              ) : null}
            </div>

            {formError ? <span className="error-text">{formError}</span> : null}

            <button className="button button-primary" disabled={isSubmitting}>
              <UserPlus size={18} />
              Create account
            </button>
          </form>

          <p className="auth-switch">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </div>
      </section>
    </main>
  )
}
