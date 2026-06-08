import { zodResolver } from '@hookform/resolvers/zod'
import { AxiosError } from 'axios'
import { CheckCircle2, UserPlus } from 'lucide-react'
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
  const [isSuccessDialogOpen, setIsSuccessDialogOpen] = useState(false)
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    reset,
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
    defaultValues: { username: '', email: '', password: '' },
  })

  async function onSubmit(values: RegisterForm) {
    try {
      setFormError(null)
      await registerUser(values)
      reset()
      setIsSuccessDialogOpen(true)
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

      {isSuccessDialogOpen ? (
        <div className="modal-backdrop" role="presentation">
          <section
            aria-labelledby="registration-success-title"
            aria-modal="true"
            className="modal"
            role="dialog"
          >
            <div className="success-dialog-copy">
              <CheckCircle2 className="success-icon" size={34} />
              <div>
                <h2 id="registration-success-title">Account created</h2>
                <p>Your account is ready. You can now sign in and start managing tasks.</p>
              </div>
            </div>

            <div className="modal-actions">
              <button
                className="button button-primary"
                type="button"
                onClick={() => navigate('/login', { replace: true })}
              >
                Go to login
              </button>
            </div>
          </section>
        </div>
      ) : null}
    </main>
  )
}
