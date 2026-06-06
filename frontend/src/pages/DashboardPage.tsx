import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'

import { ConfirmDialog } from '../components/common/ConfirmDialog'
import {
  type ApplySelection,
  type EditTaskForm,
  TaskCard,
} from '../components/tasks/TaskCard'
import { TaskCreateForm, type TaskForm } from '../components/tasks/TaskCreateForm'
import { TagManagement } from '../components/tags/TagManagement'
import { getCategories } from '../services/categories-api'
import {
  applyPrediction,
  generatePrediction,
  getActivePrediction,
} from '../services/predictions-api'
import {
  attachTagToTask,
  completeTask,
  createTask,
  deleteTask,
  getTasks,
  removeTagFromTask,
  updateTask,
  updateTaskStatus,
} from '../services/tasks-api'
import {
  createTag,
  deleteTag,
  getTags,
  updateTag,
} from '../services/tags-api'
import {
  formatPriorityLabel,
  formatStatusLabel,
  getAiInsights,
  getFocusIcon,
  getFocusTasks,
  matchesOverviewFilter,
  sortTasks,
  type TaskOverviewFilter,
} from '../utils/task-dashboard'
import type { Status, Tag, Task, TaskPrediction } from '../types/api'

export function DashboardPage() {
  const queryClient = useQueryClient()
  const [predictionsByTaskId, setPredictionsByTaskId] = useState<
    Record<string, TaskPrediction>
  >({})
  const [applySelections, setApplySelections] = useState<
    Record<string, ApplySelection>
  >({})
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null)
  const [taskPendingDelete, setTaskPendingDelete] = useState<Task | null>(null)
  const [editingTagId, setEditingTagId] = useState<string | null>(null)
  const [tagPendingDelete, setTagPendingDelete] = useState<Tag | null>(null)
  const [selectedCategoryId, setSelectedCategoryId] = useState<string>('all')
  const [selectedOverviewFilter, setSelectedOverviewFilter] =
    useState<TaskOverviewFilter>('all')
  const [selectedFocusTaskId, setSelectedFocusTaskId] = useState<string | null>(null)
  const [isCreateTaskOpen, setIsCreateTaskOpen] = useState(false)

  const tasksQuery = useQuery({
    queryKey: ['tasks'],
    queryFn: getTasks,
  })
  const categoriesQuery = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  })
  const tagsQuery = useQuery({
    queryKey: ['tags'],
    queryFn: getTags,
  })
  const activeTaskIds = tasksQuery.data
    ?.filter((task) => task.status !== 'COMPLETED' && task.status !== 'CANCELLED')
    .map((task) => task.id)
    .sort() ?? []
  const activePredictionsQuery = useQuery({
    enabled: activeTaskIds.length > 0,
    queryKey: ['active-predictions', activeTaskIds],
    queryFn: async () => {
      const results = await Promise.all(
        activeTaskIds.map(async (taskId) => {
          try {
            const prediction = await getActivePrediction(taskId)
            return [taskId, prediction] as const
          } catch {
            return null
          }
        }),
      )

      return Object.fromEntries(
        results.filter((result): result is [string, TaskPrediction] =>
          Boolean(result),
        ),
      )
    },
  })

  const createTaskMutation = useMutation({
    mutationFn: async (values: TaskForm) => {
      return createTask({
        title: values.title,
        description: values.description || undefined,
        category_id: values.category_id || undefined,
        due_date: values.due_date ? new Date(values.due_date).toISOString() : undefined,
        manual_priority: values.manual_priority,
        tag_ids: values.tag_ids,
      })
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const generatePredictionMutation = useMutation({
    mutationFn: generatePrediction,
    onSuccess: (prediction) => {
      setPredictionsByTaskId((current) => ({
        ...current,
        [prediction.task_id]: prediction,
      }))
      setApplySelections((current) => ({
        ...current,
        [prediction.task_id]: {
          apply_category: true,
          apply_priority: true,
        },
      }))
      void queryClient.invalidateQueries({ queryKey: ['active-predictions'] })
    },
  })

  const applyPredictionMutation = useMutation({
    mutationFn: async ({
      apply_category,
      apply_priority,
      predictionId,
      taskId,
    }: {
      apply_category: boolean
      apply_priority: boolean
      predictionId: string
      taskId: string
    }) => {
      return applyPrediction(
        taskId,
        predictionId,
        { apply_category, apply_priority },
      )
    },
    onSuccess: (_task, variables) => {
      dismissPrediction(variables.taskId)
      void queryClient.invalidateQueries({ queryKey: ['active-predictions'] })
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const createTagMutation = useMutation({
    mutationFn: createTag,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['tags'] })
    },
  })

  const attachTagMutation = useMutation({
    mutationFn: async ({ tagId, taskId }: { tagId: string; taskId: string }) => {
      return attachTagToTask(taskId, tagId)
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const removeTagMutation = useMutation({
    mutationFn: async ({ tagId, taskId }: { tagId: string; taskId: string }) => {
      return removeTagFromTask(taskId, tagId)
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  async function createAndAttachTag(taskId: string, name: string) {
    const tag = await createTagMutation.mutateAsync(name)
    await attachTagMutation.mutateAsync({ taskId, tagId: tag.id })
  }

  const updateTagMutation = useMutation({
    mutationFn: async ({ name, tagId }: { name: string; tagId: string }) => {
      return updateTag(tagId, name)
    },
    onSuccess: () => {
      setEditingTagId(null)
      void queryClient.invalidateQueries({ queryKey: ['tags'] })
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const deleteTagMutation = useMutation({
    mutationFn: deleteTag,
    onSuccess: () => {
      setTagPendingDelete(null)
      void queryClient.invalidateQueries({ queryKey: ['tags'] })
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const completeTaskMutation = useMutation({
    mutationFn: completeTask,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const updateTaskStatusMutation = useMutation({
    mutationFn: async ({
      status,
      taskId,
    }: {
      status: Status
      taskId: string
    }) => {
      return updateTaskStatus(taskId, status)
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const updateTaskMutation = useMutation({
    mutationFn: async ({
      taskId,
      values,
    }: {
      taskId: string
      values: EditTaskForm
    }) => {
      return updateTask(taskId, {
        title: values.title,
        description: values.description || null,
        category_id: values.category_id || null,
        due_date: values.due_date ? new Date(values.due_date).toISOString() : null,
        manual_priority: values.manual_priority,
        status: values.status,
      })
    },
    onSuccess: () => {
      setEditingTaskId(null)
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const deleteTaskMutation = useMutation({
    mutationFn: deleteTask,
    onSuccess: (_data, taskId) => {
      dismissPrediction(taskId)
      setTaskPendingDelete(null)
      void queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const tasks = tasksQuery.data ?? []
  const categories = categoriesQuery.data ?? []
  const tags = tagsQuery.data ?? []
  const activePredictionsByTaskId = {
    ...(activePredictionsQuery.data ?? {}),
    ...predictionsByTaskId,
  }
  const categoryFilteredTasks =
    selectedCategoryId === 'all'
      ? tasks
      : tasks.filter((task) => task.category_id === selectedCategoryId)
  const visibleTasks = categoryFilteredTasks.filter((task) =>
    matchesOverviewFilter(task, selectedOverviewFilter, activePredictionsByTaskId),
  )
  const focusedVisibleTasks = selectedFocusTaskId
    ? visibleTasks.filter((task) => task.id === selectedFocusTaskId)
    : visibleTasks
  const sortedVisibleTasks = sortTasks(focusedVisibleTasks)
  const focusTasks = getFocusTasks(tasks).slice(0, 3)
  const aiInsights = getAiInsights(tasks, activePredictionsByTaskId)
  const taskStats = {
    total: tasks.length,
    pending: tasks.filter((task) => task.status === 'PENDING').length,
    inProgress: tasks.filter((task) => task.status === 'IN_PROGRESS').length,
    completed: tasks.filter((task) => task.status === 'COMPLETED').length,
    cancelled: tasks.filter((task) => task.status === 'CANCELLED').length,
    highPriority: tasks.filter((task) => task.manual_priority === 'HIGH').length,
  }

  function dismissPrediction(taskId: string) {
    setPredictionsByTaskId((current) => {
      const { [taskId]: _removedPrediction, ...remaining } = current
      void _removedPrediction
      return remaining
    })
    setApplySelections((current) => {
      const { [taskId]: _removedSelection, ...remaining } = current
      void _removedSelection
      return remaining
    })
  }

  function updateApplySelection(
    taskId: string,
    value: Partial<ApplySelection>,
  ) {
    setApplySelections((current) => ({
      ...current,
      [taskId]: {
        ...(current[taskId] ?? {
          apply_category: true,
          apply_priority: true,
        }),
        ...value,
      },
    }))
  }

  function toggleOverviewFilter(filter: TaskOverviewFilter) {
    setSelectedFocusTaskId(null)
    setSelectedOverviewFilter((current) => (current === filter ? 'all' : filter))
  }

  function toggleCategoryFilter(categoryId: string) {
    setSelectedFocusTaskId(null)
    setSelectedCategoryId((current) => (current === categoryId ? 'all' : categoryId))
  }

  function toggleFocusTask(taskId: string) {
    setSelectedCategoryId('all')
    setSelectedOverviewFilter('all')
    setSelectedFocusTaskId((current) => (current === taskId ? null : taskId))
  }

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <h1>Tasks</h1>
          <p>Create tasks, organize them, and apply model suggestions.</p>
        </div>
      </header>

      <section className="overview-panel" aria-label="Task overview">
        <div className="stats-grid">
          <StatCard
            isActive={selectedOverviewFilter === 'all'}
            label="Total"
            value={taskStats.total}
            onClick={() => toggleOverviewFilter('all')}
          />
          <StatCard
            isActive={selectedOverviewFilter === 'pending'}
            label="Pending"
            value={taskStats.pending}
            tone="muted"
            onClick={() => toggleOverviewFilter('pending')}
          />
          <StatCard
            isActive={selectedOverviewFilter === 'in_progress'}
            label="In progress"
            value={taskStats.inProgress}
            tone="info"
            onClick={() => toggleOverviewFilter('in_progress')}
          />
          <StatCard
            isActive={selectedOverviewFilter === 'completed'}
            label="Completed"
            value={taskStats.completed}
            tone="success"
            onClick={() => toggleOverviewFilter('completed')}
          />
          <StatCard
            isActive={selectedOverviewFilter === 'high_priority'}
            label="High priority"
            value={taskStats.highPriority}
            tone="danger"
            onClick={() => toggleOverviewFilter('high_priority')}
          />
          <StatCard
            isActive={selectedOverviewFilter === 'cancelled'}
            label="Cancelled"
            value={taskStats.cancelled}
            tone="cancelled"
            onClick={() => toggleOverviewFilter('cancelled')}
          />
        </div>

        <div className="overview-categories" aria-label="Category filters">
          <span>Categories</span>
          <button
            className={`filter-chip ${selectedCategoryId === 'all' ? 'active' : ''}`}
            type="button"
            onClick={() => toggleCategoryFilter('all')}
          >
            All
            <span>{tasks.length}</span>
          </button>
          {categories.map((category) => {
            const count = tasks.filter(
              (task) => task.category_id === category.id,
            ).length

            return (
              <button
                className={`filter-chip ${
                  selectedCategoryId === category.id ? 'active' : ''
                }`}
                key={category.id}
                type="button"
                onClick={() => toggleCategoryFilter(category.id)}
              >
                {category.name}
                <span>{count}</span>
              </button>
            )
          })}
        </div>
      </section>

      <section className="dashboard-grid">
        <aside className="dashboard-sidebar">
          <section className="panel">
            <h2>Quick actions</h2>
            <p className="panel-subtitle">
              Create tasks from a focused dialog and keep tags organized here.
            </p>

            <button
              className="button button-primary full-width"
              type="button"
              onClick={() => setIsCreateTaskOpen(true)}
            >
              New task
            </button>
          </section>

          <section className="panel">
            <TagManagement
              editingTagId={editingTagId}
              isCreateError={createTagMutation.isError}
              isCreatePending={createTagMutation.isPending}
              isDeleteError={deleteTagMutation.isError}
              isUpdateError={updateTagMutation.isError}
              isUpdatePending={updateTagMutation.isPending}
              tags={tags}
              onCancelEdit={() => setEditingTagId(null)}
              onCreate={(name) => createTagMutation.mutateAsync(name)}
              onDelete={(tag) => setTagPendingDelete(tag)}
              onEdit={setEditingTagId}
              onSave={(tagId, name) => updateTagMutation.mutate({ tagId, name })}
            />
          </section>

          <section className="panel sidebar-panel">
            <div>
              <h2>Today's focus</h2>
              <p className="panel-subtitle">Tasks that deserve attention first.</p>
            </div>

            <div className="focus-list">
              {focusTasks.length > 0 ? (
                focusTasks.map((task) => (
                  <button
                    className={`focus-item ${
                      selectedFocusTaskId === task.id ? 'active' : ''
                    }`}
                    key={task.id}
                    type="button"
                    onClick={() => toggleFocusTask(task.id)}
                  >
                    <span>{getFocusIcon(task)}</span>
                    <div>
                      <strong>{task.title}</strong>
                      <small>
                        {formatPriorityLabel(task.manual_priority)} ·{' '}
                        {formatStatusLabel(task.status)}
                      </small>
                    </div>
                  </button>
                ))
              ) : (
                <p className="empty-copy">Nothing urgent right now.</p>
              )}
            </div>
          </section>

          <section className="panel sidebar-panel">
            <div>
              <h2>AI insights</h2>
              <p className="panel-subtitle">A quick read on model support.</p>
            </div>

            <div className="insight-grid">
              <InsightMetric
                isActive={selectedOverviewFilter === 'needs_prediction'}
                label="Need prediction"
                value={aiInsights.needsPrediction}
                onClick={() => toggleOverviewFilter('needs_prediction')}
              />
              <InsightMetric
                isActive={selectedOverviewFilter === 'ready_to_apply'}
                label="Ready to apply"
                value={aiInsights.readyToApply}
                onClick={() => toggleOverviewFilter('ready_to_apply')}
              />
              <InsightMetric
                isActive={selectedOverviewFilter === 'high_priority'}
                label="High priority"
                value={aiInsights.highPriority}
                onClick={() => toggleOverviewFilter('high_priority')}
              />
              <InsightMetric
                isActive={selectedOverviewFilter === 'due_soon'}
                label="Due soon"
                value={aiInsights.dueSoon}
                onClick={() => toggleOverviewFilter('due_soon')}
              />
              <InsightMetric
                isActive={selectedOverviewFilter === 'overdue'}
                label="Overdue"
                value={aiInsights.overdue}
                onClick={() => toggleOverviewFilter('overdue')}
              />
            </div>
          </section>
        </aside>

        <section className="task-list">
          {tasksQuery.isLoading ? (
            <div className="empty-state">Loading tasks...</div>
          ) : null}

          {!tasksQuery.isLoading && sortedVisibleTasks.length === 0 ? (
            <div className="empty-state">
              <p>
                {tasks.length === 0
                  ? 'No tasks yet.'
                  : 'No tasks match this filter.'}
              </p>
            </div>
          ) : null}

          {sortedVisibleTasks.map((task) => (
            <TaskCard
              applySelection={
                applySelections[task.id] ?? {
                  apply_category: true,
                  apply_priority: true,
                }
              }
              categories={categories}
              isApplyPredictionPending={applyPredictionMutation.isPending}
              isAttachTagPending={attachTagMutation.isPending}
              isCompletePending={completeTaskMutation.isPending}
              isCreateTagPending={createTagMutation.isPending}
              isEditing={editingTaskId === task.id}
              isGeneratePredictionPending={generatePredictionMutation.isPending}
              isStatusUpdatePending={updateTaskStatusMutation.isPending}
              isUpdatePending={updateTaskMutation.isPending}
              key={task.id}
              prediction={predictionsByTaskId[task.id]}
              tags={tags}
              task={task}
              onApplyPrediction={(payload) => applyPredictionMutation.mutate(payload)}
              onAttachTag={(tagId) => attachTagMutation.mutate({ taskId: task.id, tagId })}
              onComplete={() => completeTaskMutation.mutate(task.id)}
              onCreateAndAttachTag={(name) => createAndAttachTag(task.id, name)}
              onDelete={() => setTaskPendingDelete(task)}
              onDismissPrediction={() => dismissPrediction(task.id)}
              onGeneratePrediction={() => generatePredictionMutation.mutate(task.id)}
              onRemoveTag={(tagId) => removeTagMutation.mutate({ taskId: task.id, tagId })}
              onToggleEdit={() =>
                setEditingTaskId((current) => (current === task.id ? null : task.id))
              }
              onUpdateApplySelection={(value) => updateApplySelection(task.id, value)}
              onUpdateStatus={(status) =>
                updateTaskStatusMutation.mutate({
                  taskId: task.id,
                  status,
                })
              }
              onUpdateTask={(values) =>
                updateTaskMutation.mutate({ taskId: task.id, values })
              }
            />
          ))}

          {tasksQuery.isError ? (
            <p className="error-text">Could not load tasks.</p>
          ) : null}
          {generatePredictionMutation.isError ? (
            <p className="error-text">Could not generate prediction.</p>
          ) : null}
          {applyPredictionMutation.isError ? (
            <p className="error-text">Could not apply selected prediction.</p>
          ) : null}
          {attachTagMutation.isError || removeTagMutation.isError ? (
            <p className="error-text">Could not update task tags.</p>
          ) : null}
          {updateTaskMutation.isError ? (
            <p className="error-text">Could not update task.</p>
          ) : null}
          {updateTaskStatusMutation.isError ? (
            <p className="error-text">Could not update task status.</p>
          ) : null}
          {deleteTaskMutation.isError ? (
            <p className="error-text">Could not delete task.</p>
          ) : null}
        </section>
      </section>

      {taskPendingDelete ? (
        <ConfirmDialog
          confirmLabel="Delete task"
          description={
            <>
              This will permanently remove <strong>{taskPendingDelete.title}</strong>{' '}
              and its predictions.
            </>
          }
          isPending={deleteTaskMutation.isPending}
          title="Delete task?"
          onCancel={() => setTaskPendingDelete(null)}
          onConfirm={() => deleteTaskMutation.mutate(taskPendingDelete.id)}
        />
      ) : null}
      {tagPendingDelete ? (
        <ConfirmDialog
          confirmLabel="Delete tag"
          description="This will remove the tag and detach it from all tasks."
          isPending={deleteTagMutation.isPending}
          title="Delete tag?"
          onCancel={() => setTagPendingDelete(null)}
          onConfirm={() => deleteTagMutation.mutate(tagPendingDelete.id)}
        />
      ) : null}
      {isCreateTaskOpen ? (
        <CreateTaskDialog
          categories={categories}
          isCreateError={createTaskMutation.isError}
          isCreatePending={createTaskMutation.isPending}
          tags={tags}
          onCancel={() => setIsCreateTaskOpen(false)}
          onSubmit={async (values) => {
            await createTaskMutation.mutateAsync(values)
            setIsCreateTaskOpen(false)
          }}
        />
      ) : null}
    </main>
  )
}

function CreateTaskDialog({
  categories,
  isCreateError,
  isCreatePending,
  onCancel,
  onSubmit,
  tags,
}: {
  categories: Awaited<ReturnType<typeof getCategories>>
  isCreateError: boolean
  isCreatePending: boolean
  onCancel: () => void
  onSubmit: (values: TaskForm) => Promise<void>
  tags: Tag[]
}) {
  return (
    <div className="modal-backdrop" role="presentation">
      <section
        aria-labelledby="create-task-title"
        aria-modal="true"
        className="modal modal-wide"
        role="dialog"
      >
        <div>
          <h2 id="create-task-title">New task</h2>
          <p>Add the details now or let the model suggest category and priority later.</p>
        </div>

        <TaskCreateForm
          categories={categories}
          isCreateError={isCreateError}
          isCreatePending={isCreatePending}
          isTagCreatePending={false}
          showTagCreation={false}
          tags={tags}
          onCreateTag={async () => undefined}
          onSubmit={onSubmit}
        />

        <div className="modal-actions">
          <button className="button button-ghost" type="button" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </section>
    </div>
  )
}

function StatCard({
  isActive,
  label,
  onClick,
  tone = 'default',
  value,
}: {
  isActive: boolean
  label: string
  onClick: () => void
  tone?: 'default' | 'muted' | 'info' | 'success' | 'danger' | 'cancelled'
  value: number
}) {
  return (
    <button
      aria-pressed={isActive}
      className={`stat-card stat-${tone} ${isActive ? 'active' : ''}`}
      type="button"
      onClick={onClick}
    >
      <span>{label}</span>
      <strong>{value}</strong>
    </button>
  )
}

function InsightMetric({
  isActive,
  label,
  onClick,
  value,
}: {
  isActive: boolean
  label: string
  onClick: () => void
  value: number
}) {
  return (
    <button
      aria-pressed={isActive}
      className={`insight-metric ${isActive ? 'active' : ''}`}
      type="button"
      onClick={onClick}
    >
      <strong>{value}</strong>
      <span>{label}</span>
    </button>
  )
}
