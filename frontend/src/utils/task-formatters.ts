import type { Category, CategoryName, Priority, Status } from '../types/api'

export function getCategoryName(categoryId: string | null, categories: Category[]) {
  if (!categoryId) {
    return 'None'
  }

  const categoryName = categories.find((category) => category.id === categoryId)?.name

  return categoryName ? formatCategoryName(categoryName) : 'Unknown'
}

export function getCategoryIcon(categoryId: string | null, categories: Category[]) {
  const categoryName = categories.find((category) => category.id === categoryId)?.name

  if (!categoryName) {
    return '🏷️'
  }

  const icons: Record<CategoryName, string> = {
    WORK: '💼',
    PERSONAL: '🏠',
    SHOPPING: '🛒',
    HEALTH: '🏥',
    FINANCE: '💳',
    EDUCATION: '🎓',
    ENTERTAINMENT: '🎬',
    OTHER: '🏷️',
  }

  return icons[categoryName]
}

export function getPriorityIcon(priority: Priority) {
  const icons: Record<Priority, string> = {
    LOW: '🌱',
    MEDIUM: '⚡',
    HIGH: '🔥',
  }

  return icons[priority]
}

export function formatPriority(priority: Priority) {
  return priority.charAt(0) + priority.slice(1).toLowerCase()
}

export function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`
}

export function formatStatus(status: Status) {
  return status.replace('_', ' ')
}

export function getStatusIcon(status: Status) {
  const icons: Record<Status, string> = {
    PENDING: '🟡',
    IN_PROGRESS: '🔵',
    COMPLETED: '🟢',
    CANCELLED: '🔴',
  }

  return icons[status]
}

export function formatDueDate(value: string) {
  const date = new Date(value)
  const now = new Date()
  const tomorrow = new Date(now)
  tomorrow.setDate(now.getDate() + 1)
  const time = new Intl.DateTimeFormat(undefined, {
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)

  if (isSameDay(date, now)) {
    return `Today ${time}`
  }

  if (isSameDay(date, tomorrow)) {
    return `Tomorrow ${time}`
  }

  return new Intl.DateTimeFormat(undefined, {
    day: 'numeric',
    month: 'short',
  }).format(date)
}

export function toDateTimeLocalValue(value: string | null) {
  if (!value) {
    return ''
  }

  const date = new Date(value)
  const offsetMs = date.getTimezoneOffset() * 60 * 1000
  return new Date(date.getTime() - offsetMs).toISOString().slice(0, 16)
}

export function formatReasoning(reasoning: Record<string, unknown>) {
  const explanation = reasoning.explanation

  if (typeof explanation === 'string') {
    return explanation
  }

  return Object.entries(reasoning)
    .slice(0, 3)
    .map(([key, value]) => `${key}: ${String(value)}`)
    .join(' · ')
}

function formatCategoryName(categoryName: CategoryName) {
  return categoryName.charAt(0) + categoryName.slice(1).toLowerCase()
}

function isSameDay(left: Date, right: Date) {
  return (
    left.getFullYear() === right.getFullYear() &&
    left.getMonth() === right.getMonth() &&
    left.getDate() === right.getDate()
  )
}
