import type { Task, TaskPrediction } from '../types/api'

export type TaskOverviewFilter =
  | 'all'
  | 'pending'
  | 'in_progress'
  | 'completed'
  | 'cancelled'
  | 'high_priority'
  | 'needs_prediction'
  | 'ready_to_apply'
  | 'due_soon'
  | 'overdue'

export function matchesOverviewFilter(
  task: Task,
  filter: TaskOverviewFilter,
  activePredictionsByTaskId: Record<string, TaskPrediction>,
) {
  if (filter === 'pending') {
    return task.status === 'PENDING'
  }

  if (filter === 'in_progress') {
    return task.status === 'IN_PROGRESS'
  }

  if (filter === 'completed') {
    return task.status === 'COMPLETED'
  }

  if (filter === 'cancelled') {
    return task.status === 'CANCELLED'
  }

  if (filter === 'high_priority') {
    return task.manual_priority === 'HIGH'
  }

  if (filter === 'needs_prediction') {
    return (
      task.status !== 'COMPLETED' &&
      task.status !== 'CANCELLED' &&
      !activePredictionsByTaskId[task.id]
    )
  }

  if (filter === 'ready_to_apply') {
    const prediction = activePredictionsByTaskId[task.id]

    return Boolean(
      prediction && (!prediction.applied_category || !prediction.applied_priority),
    )
  }

  if (filter === 'due_soon') {
    return (
      task.status !== 'COMPLETED' &&
      task.status !== 'CANCELLED' &&
      isDueSoon(task.due_date)
    )
  }

  if (filter === 'overdue') {
    return (
      task.status !== 'COMPLETED' &&
      task.status !== 'CANCELLED' &&
      isOverdue(task.due_date)
    )
  }

  return true
}

export function sortTasks(tasks: Task[]) {
  return [...tasks].sort((left, right) => {
    const statusDifference = getStatusRank(left.status) - getStatusRank(right.status)

    if (statusDifference !== 0) {
      return statusDifference
    }

    const priorityDifference =
      getPriorityRank(right.manual_priority) - getPriorityRank(left.manual_priority)

    if (priorityDifference !== 0) {
      return priorityDifference
    }

    return getCreatedTime(right) - getCreatedTime(left)
  })
}

export function getFocusTasks(tasks: Task[]) {
  return sortTasks(
    tasks.filter((task) => task.status !== 'COMPLETED' && task.status !== 'CANCELLED'),
  )
}

export function getAiInsights(
  tasks: Task[],
  activePredictionsByTaskId: Record<string, TaskPrediction>,
) {
  const activeTasks = tasks.filter(
    (task) => task.status !== 'COMPLETED' && task.status !== 'CANCELLED',
  )

  return {
    dueSoon: activeTasks.filter((task) => isDueSoon(task.due_date)).length,
    highPriority: activeTasks.filter((task) => task.manual_priority === 'HIGH').length,
    needsPrediction: activeTasks.filter((task) => !activePredictionsByTaskId[task.id])
      .length,
    overdue: activeTasks.filter((task) => isOverdue(task.due_date)).length,
    readyToApply: Object.values(activePredictionsByTaskId).filter(
      (prediction) => !prediction.applied_category || !prediction.applied_priority,
    ).length,
  }
}

export function getFocusIcon(task: Task) {
  if (task.manual_priority === 'HIGH') {
    return '🔥'
  }

  if (isDueSoon(task.due_date)) {
    return '📅'
  }

  if (task.status === 'IN_PROGRESS') {
    return '🔵'
  }

  return '⚡'
}

export function isDueSoon(value: string | null) {
  if (!value) {
    return false
  }

  const dueDate = new Date(value)
  const now = new Date()
  const threeDaysFromNow = new Date(now)
  threeDaysFromNow.setDate(now.getDate() + 3)

  return dueDate >= now && dueDate <= threeDaysFromNow
}

export function isOverdue(value: string | null) {
  if (!value) {
    return false
  }

  return new Date(value) < new Date()
}

export function formatPriorityLabel(priority: Task['manual_priority']) {
  return priority.charAt(0) + priority.slice(1).toLowerCase()
}

export function formatStatusLabel(status: Task['status']) {
  return status
    .split('_')
    .map((part) => part.charAt(0) + part.slice(1).toLowerCase())
    .join(' ')
}

function getStatusRank(status: Task['status']) {
  const ranks: Record<Task['status'], number> = {
    PENDING: 1,
    IN_PROGRESS: 1,
    CANCELLED: 2,
    COMPLETED: 3,
  }

  return ranks[status]
}

function getPriorityRank(priority: Task['manual_priority']) {
  const ranks: Record<Task['manual_priority'], number> = {
    LOW: 1,
    MEDIUM: 2,
    HIGH: 3,
  }

  return ranks[priority]
}

function getCreatedTime(task: Task) {
  if (!task.created_at) {
    return 0
  }

  const time = new Date(task.created_at).getTime()
  return Number.isNaN(time) ? 0 : time
}
