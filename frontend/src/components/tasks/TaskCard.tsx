import { zodResolver } from '@hookform/resolvers/zod'
import {
  Brain,
  Check,
  Pencil,
  Plus,
  Search,
  Tag as TagIcon,
  Tags,
  Trash2,
  X,
} from 'lucide-react'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'

import { DateTimePicker } from '../common/DateTimePicker'
import type { Category, Priority, Status, Tag, Task, TaskPrediction } from '../../types/api'
import {
  formatDueDate,
  formatPercent,
  formatPriority,
  formatReasoning,
  formatStatus,
  getCategoryIcon,
  getCategoryName,
  getPriorityIcon,
  getStatusIcon,
  toDateTimeLocalValue,
} from '../../utils/task-formatters'

export interface ApplySelection {
  apply_category: boolean
  apply_priority: boolean
}

const editTaskSchema = z.object({
  title: z.string().trim().min(1, 'Title is required'),
  description: z.string().trim().optional(),
  category_id: z.string().optional(),
  due_date: z.string().optional(),
  manual_priority: z.enum(['LOW', 'MEDIUM', 'HIGH']),
  status: z.enum(['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']),
})

export type EditTaskForm = z.infer<typeof editTaskSchema>

interface TaskCardProps {
  applySelection: ApplySelection
  categories: Category[]
  isApplyPredictionPending: boolean
  isAttachTagPending: boolean
  isCompletePending: boolean
  isCreateTagPending: boolean
  isEditing: boolean
  isGeneratePredictionPending: boolean
  isStatusUpdatePending: boolean
  isUpdatePending: boolean
  prediction?: TaskPrediction
  tags: Tag[]
  task: Task
  onApplyPrediction: (payload: {
    apply_category: boolean
    apply_priority: boolean
    predictionId: string
    taskId: string
  }) => void
  onAttachTag: (tagId: string) => void
  onComplete: () => void
  onCreateAndAttachTag: (name: string) => Promise<void>
  onDelete: () => void
  onDismissPrediction: () => void
  onGeneratePrediction: () => void
  onRemoveTag: (tagId: string) => void
  onToggleEdit: () => void
  onUpdateApplySelection: (value: Partial<ApplySelection>) => void
  onUpdateStatus: (status: Status) => void
  onUpdateTask: (values: EditTaskForm) => void
}

export function TaskCard({
  applySelection,
  categories,
  isApplyPredictionPending,
  isAttachTagPending,
  isCompletePending,
  isCreateTagPending,
  isEditing,
  isGeneratePredictionPending,
  isStatusUpdatePending,
  isUpdatePending,
  onApplyPrediction,
  onAttachTag,
  onComplete,
  onCreateAndAttachTag,
  onDelete,
  onDismissPrediction,
  onGeneratePrediction,
  onRemoveTag,
  onToggleEdit,
  onUpdateApplySelection,
  onUpdateStatus,
  onUpdateTask,
  prediction,
  tags,
  task,
}: TaskCardProps) {
  const canApply =
    prediction && (applySelection.apply_category || applySelection.apply_priority)

  return (
    <article className="task-card">
      <div className="task-card-header">
        <div className="task-copy">
          <h2 className="task-title">{task.title}</h2>
          {task.description ? (
            <p className="task-description">{task.description}</p>
          ) : null}
          <label
            className={`status-chip-control status-${task.status.toLowerCase()}`}
          >
            <span>Status</span>
            <select
              aria-label={`Change status for ${task.title}`}
              disabled={isStatusUpdatePending}
              value={task.status}
              onChange={(event) => onUpdateStatus(event.target.value as Status)}
            >
              {(['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'] satisfies Status[]).map(
                (status) => (
                  <option key={status} value={status}>
                    {getStatusIcon(status)} {formatStatus(status)}
                  </option>
                ),
              )}
            </select>
          </label>
        </div>
      </div>

      <div className="task-meta">
        <span className={`badge priority-${task.manual_priority.toLowerCase()}`}>
          {getPriorityIcon(task.manual_priority)} {formatPriority(task.manual_priority)}
        </span>
        <span className="badge">
          {getCategoryIcon(task.category_id, categories)}{' '}
          {getCategoryName(task.category_id, categories)}
        </span>
        {task.due_date ? (
          <span className="badge">📅 {formatDueDate(task.due_date)}</span>
        ) : null}
        {task.tags.map((tag) => (
          <span className="badge tag-badge" key={tag.id}>
            <TagIcon size={12} />
            {tag.name}
            <button
              aria-label={`Remove ${tag.name}`}
              type="button"
              onClick={() => onRemoveTag(tag.id)}
            >
              <X size={13} />
            </button>
          </span>
        ))}
      </div>

      {prediction ? (
        <PredictionCard
          applySelection={applySelection}
          isPending={isApplyPredictionPending}
          prediction={prediction}
          onApply={() =>
            onApplyPrediction({
              taskId: task.id,
              predictionId: prediction.id,
              apply_category: applySelection.apply_category,
              apply_priority: applySelection.apply_priority,
            })
          }
          onDismiss={onDismissPrediction}
          onUpdateSelection={onUpdateApplySelection}
          canApply={Boolean(canApply)}
        />
      ) : null}

      <div className="task-actions">
        <TagAttachControl
          disabled={isAttachTagPending || isCreateTagPending}
          isCreatePending={isCreateTagPending}
          tags={tags}
          task={task}
          onAttach={onAttachTag}
          onCreateAndAttach={onCreateAndAttachTag}
        />
        <button
          className="button button-ai"
          disabled={isGeneratePredictionPending}
          type="button"
          onClick={onGeneratePrediction}
        >
          <Brain size={17} />
          Generate prediction
        </button>
        {task.status !== 'COMPLETED' && task.status !== 'CANCELLED' ? (
          <button
            className="button button-secondary"
            disabled={isCompletePending}
            type="button"
            onClick={onComplete}
          >
            <Check size={17} />
            Complete
          </button>
        ) : null}
        <button className="button button-secondary" type="button" onClick={onToggleEdit}>
          <Pencil size={17} />
          Edit
        </button>
        <button className="button button-danger" type="button" onClick={onDelete}>
          <Trash2 size={17} />
          Delete
        </button>
      </div>

      {isEditing ? (
        <TaskEditForm
          categories={categories}
          isPending={isUpdatePending}
          task={task}
          onCancel={onToggleEdit}
          onSubmit={onUpdateTask}
        />
      ) : null}
    </article>
  )
}

function PredictionCard({
  applySelection,
  canApply,
  isPending,
  onApply,
  onDismiss,
  onUpdateSelection,
  prediction,
}: {
  applySelection: ApplySelection
  canApply: boolean
  isPending: boolean
  onApply: () => void
  onDismiss: () => void
  onUpdateSelection: (value: Partial<ApplySelection>) => void
  prediction: TaskPrediction
}) {
  return (
    <section className="prediction-card">
      <div className="prediction-card-header">
        <div>
          <h3>Model suggestion</h3>
          <p>
            Score {formatPercent(prediction.smart_score)} · model{' '}
            {prediction.model_version ?? 'unknown'}
          </p>
        </div>
      </div>

      <div className="prediction-row">
        <span className="badge badge-priority">
          {prediction.predicted_priority} priority ·{' '}
          {formatPercent(prediction.priority_confidence)}
        </span>
        <span className="badge">
          {prediction.predicted_category} ·{' '}
          {formatPercent(prediction.category_confidence)}
        </span>
      </div>

      {prediction.reasoning ? (
        <p className="prediction-reasoning">
          {formatReasoning(prediction.reasoning)}
        </p>
      ) : null}

      <div className="prediction-options">
        <label>
          <input
            checked={applySelection.apply_category}
            type="checkbox"
            onChange={(event) =>
              onUpdateSelection({ apply_category: event.target.checked })
            }
          />
          Apply category
        </label>
        <label>
          <input
            checked={applySelection.apply_priority}
            type="checkbox"
            onChange={(event) =>
              onUpdateSelection({ apply_priority: event.target.checked })
            }
          />
          Apply priority
        </label>
      </div>

      <div className="prediction-actions">
        <button
          className="button button-primary"
          disabled={!canApply || isPending}
          type="button"
          onClick={onApply}
        >
          Apply selected
        </button>
        <button className="button button-ghost" type="button" onClick={onDismiss}>
          Dismiss
        </button>
      </div>
    </section>
  )
}

function TaskEditForm({
  categories,
  isPending,
  onCancel,
  onSubmit,
  task,
}: {
  categories: Category[]
  isPending: boolean
  onCancel: () => void
  onSubmit: (values: EditTaskForm) => void
  task: Task
}) {
  const {
    formState: { errors },
    handleSubmit,
    register,
    setValue,
  } = useForm<EditTaskForm>({
    resolver: zodResolver(editTaskSchema),
    defaultValues: {
      title: task.title,
      description: task.description ?? '',
      category_id: task.category_id ?? '',
      due_date: toDateTimeLocalValue(task.due_date),
      manual_priority: task.manual_priority,
      status: task.status,
    },
  })
  const [dueDateValue, setDueDateValue] = useState(toDateTimeLocalValue(task.due_date))

  return (
    <form className="edit-form" onSubmit={handleSubmit(onSubmit)}>
      <div className="field">
        <label htmlFor={`edit-title-${task.id}`}>Title</label>
        <input id={`edit-title-${task.id}`} {...register('title')} />
        {errors.title ? (
          <span className="error-text">{errors.title.message}</span>
        ) : null}
      </div>

      <div className="field">
        <label htmlFor={`edit-description-${task.id}`}>Description</label>
        <textarea id={`edit-description-${task.id}`} {...register('description')} />
      </div>

      <div className="form-grid">
        <div className="field">
          <label htmlFor={`edit-status-${task.id}`}>Status</label>
          <select id={`edit-status-${task.id}`} {...register('status')}>
            {(['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'] satisfies Status[]).map(
              (status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ),
            )}
          </select>
        </div>

        <div className="field">
          <label htmlFor={`edit-priority-${task.id}`}>Priority</label>
          <select id={`edit-priority-${task.id}`} {...register('manual_priority')}>
            {(['LOW', 'MEDIUM', 'HIGH'] satisfies Priority[]).map((priority) => (
              <option key={priority} value={priority}>
                {priority}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label htmlFor={`edit-category-${task.id}`}>Category</label>
          <select id={`edit-category-${task.id}`} {...register('category_id')}>
            <option value="">No category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <DateTimePicker
            id={`edit-due-date-${task.id}`}
            label="Due date"
            value={dueDateValue}
            onChange={(value) => {
              setDueDateValue(value)
              setValue('due_date', value, {
                shouldDirty: true,
                shouldValidate: true,
              })
            }}
          />
        </div>
      </div>

      <div className="edit-form-actions">
        <button className="button button-primary" disabled={isPending}>
          Save changes
        </button>
        <button className="button button-ghost" type="button" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  )
}

function TagAttachControl({
  disabled,
  isCreatePending,
  onAttach,
  onCreateAndAttach,
  tags,
  task,
}: {
  disabled: boolean
  isCreatePending: boolean
  onAttach: (tagId: string) => void
  onCreateAndAttach: (name: string) => Promise<void>
  tags: Tag[]
  task: Task
}) {
  const [isOpen, setIsOpen] = useState(false)
  const [query, setQuery] = useState('')
  const attachedTagIds = new Set(task.tags.map((tag) => tag.id))
  const availableTags = tags.filter((tag) => !attachedTagIds.has(tag.id))
  const normalizedQuery = query.trim().toLowerCase()
  const filteredTags = normalizedQuery
    ? availableTags.filter((tag) => tag.name.toLowerCase().includes(normalizedQuery))
    : availableTags
  const tagAlreadyExists = tags.some(
    (tag) => tag.name.toLowerCase() === normalizedQuery,
  )
  const canCreate = normalizedQuery.length > 0 && !tagAlreadyExists

  return (
    <div className="tag-attach">
      <button
        className="button button-secondary tag-attach-trigger"
        disabled={disabled}
        type="button"
        onClick={() => setIsOpen((current) => !current)}
      >
        <Tags size={16} />
        Add tag
      </button>

      {isOpen ? (
        <div className="tag-attach-menu">
          <div className="search-field">
            <Search size={15} />
            <input
              aria-label={`Search tags for ${task.title}`}
              placeholder="Search or create tag"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>

          <div className="tag-attach-list">
            {filteredTags.length > 0 ? (
              filteredTags.map((tag) => (
                <button
                  className="tag-option"
                  disabled={disabled}
                  key={tag.id}
                  type="button"
                  onClick={() => {
                    onAttach(tag.id)
                    setIsOpen(false)
                  }}
                >
                  #{tag.name}
                </button>
              ))
            ) : (
              <p className="empty-copy">
                {availableTags.length === 0
                  ? 'All tags are already attached.'
                  : 'No tags found.'}
              </p>
            )}
          </div>

          <form
            className="tag-attach-create"
            onSubmit={async (event) => {
              event.preventDefault()

              if (canCreate) {
                await onCreateAndAttach(query.trim())
                setQuery('')
                setIsOpen(false)
              }
            }}
          >
            <span>Create new tag</span>
            <button
              aria-label="Create and attach tag"
              className="icon-button icon-button-primary"
              disabled={!canCreate || isCreatePending}
              type="submit"
            >
              <Plus size={16} />
            </button>
          </form>
          {tagAlreadyExists && normalizedQuery.length > 0 ? (
            <p className="field-hint">This tag already exists above.</p>
          ) : null}
        </div>
      ) : null}
    </div>
  )
}
