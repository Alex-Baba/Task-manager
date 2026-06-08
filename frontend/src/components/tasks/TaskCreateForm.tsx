import { zodResolver } from '@hookform/resolvers/zod'
import { Plus, Search } from 'lucide-react'
import { useRef, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'

import { DateTimePicker } from '../common/DateTimePicker'
import type { Category, Priority, Tag } from '../../types/api'

const taskSchema = z.object({
  title: z.string().trim().min(1, 'Title is required'),
  description: z.string().trim().optional(),
  category_id: z.string().optional(),
  due_date: z.string().optional(),
  manual_priority: z.enum(['LOW', 'MEDIUM', 'HIGH']),
  tag_ids: z.array(z.string()),
})

export type TaskForm = z.infer<typeof taskSchema>

interface TaskCreateFormProps {
  categories: Category[]
  isCreatePending: boolean
  isCreateError: boolean
  isTagCreatePending: boolean
  showTagCreation?: boolean
  tags: Tag[]
  onCancel?: () => void
  onCreateTag: (name: string) => Promise<Tag>
  onSubmit: (values: TaskForm) => Promise<void>
}

export function TaskCreateForm({
  categories,
  isCreateError,
  isCreatePending,
  isTagCreatePending,
  onCancel,
  onCreateTag,
  onSubmit,
  showTagCreation = true,
  tags,
}: TaskCreateFormProps) {
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    reset,
    setValue,
  } = useForm<TaskForm>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: '',
      description: '',
      category_id: '',
      due_date: '',
      manual_priority: 'LOW',
      tag_ids: [],
    },
  })
  const [dueDateValue, setDueDateValue] = useState('')
  const [selectedTagIds, setSelectedTagIds] = useState<string[]>([])
  const [tagQuery, setTagQuery] = useState('')
  const tagSearchInputRef = useRef<HTMLInputElement | null>(null)

  async function submitTask(values: TaskForm) {
    await onSubmit(values)
    reset()
    setDueDateValue('')
    setSelectedTagIds([])
    setTagQuery('')
  }

  function updateSelectedTags(nextTagIds: string[]) {
    setSelectedTagIds(nextTagIds)
    setValue('tag_ids', nextTagIds, {
      shouldDirty: true,
      shouldValidate: true,
    })
  }

  function toggleTag(tagId: string) {
    const nextTagIds = selectedTagIds.includes(tagId)
      ? selectedTagIds.filter((selectedTagId) => selectedTagId !== tagId)
      : [...selectedTagIds, tagId]

    updateSelectedTags(nextTagIds)
  }

  async function createAndSelectTag() {
    const name = tagQuery.trim()

    if (!name || tagAlreadyExists) {
      tagSearchInputRef.current?.focus()
      return
    }

    const tag = await onCreateTag(name)
    updateSelectedTags([...selectedTagIds, tag.id])
    setTagQuery('')
  }

  const normalizedTagQuery = tagQuery.trim().toLowerCase()
  const filteredTags = normalizedTagQuery
    ? tags.filter((tag) => tag.name.toLowerCase().includes(normalizedTagQuery))
    : tags
  const tagAlreadyExists = tags.some(
    (tag) => tag.name.toLowerCase() === normalizedTagQuery,
  )
  const canCreateTag = normalizedTagQuery.length > 0 && !tagAlreadyExists

  return (
    <form className="form" onSubmit={handleSubmit(submitTask)}>
        <div className="field">
          <label htmlFor="title">Title</label>
          <input id="title" {...register('title')} />
          {errors.title ? (
            <span className="error-text">{errors.title.message}</span>
          ) : null}
        </div>

        <div className="field">
          <label htmlFor="description">Description</label>
          <textarea id="description" {...register('description')} />
        </div>

        <div className="field">
          <label htmlFor="category">Category</label>
          <select id="category" {...register('category_id')}>
            <option value="">No category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label htmlFor="manual_priority">Manual priority</label>
          <select id="manual_priority" {...register('manual_priority')}>
            {(['LOW', 'MEDIUM', 'HIGH'] satisfies Priority[]).map((priority) => (
              <option key={priority} value={priority}>
                {priority}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <DateTimePicker
            id="due_date"
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

      <div className="field">
        <label htmlFor="task-tag-search">Tags</label>
        <div className="tag-picker">
          <div className="search-field">
            <Search size={15} />
            <input
              id="task-tag-search"
              ref={tagSearchInputRef}
              placeholder="Search or create tag"
              value={tagQuery}
              onChange={(event) => setTagQuery(event.target.value)}
            />
          </div>

          <div className="tag-attach-list">
            {filteredTags.length > 0 ? (
              filteredTags.map((tag) => {
                const isSelected = selectedTagIds.includes(tag.id)

                return (
                  <button
                    aria-pressed={isSelected}
                    className={`tag-option ${isSelected ? 'selected' : ''}`}
                    key={tag.id}
                    type="button"
                    onClick={() => toggleTag(tag.id)}
                  >
                    #{tag.name}
                  </button>
                )
              })
            ) : (
              <p className="empty-copy">No tags found.</p>
            )}
          </div>

          {showTagCreation ? (
            <>
              <div className="tag-attach-create">
                <button
                  className="tag-create-action"
                  type="button"
                  onClick={() => void createAndSelectTag()}
                >
                  {canCreateTag ? `Create "${tagQuery.trim()}"` : 'Create new tag'}
                </button>
                <button
                  aria-label="Create tag"
                  className="icon-button icon-button-primary"
                  disabled={isTagCreatePending}
                  type="button"
                  onClick={() => void createAndSelectTag()}
                >
                  <Plus size={16} />
                </button>
              </div>
              {tagAlreadyExists && normalizedTagQuery.length > 0 ? (
                <p className="field-hint">This tag already exists above.</p>
              ) : null}
            </>
          ) : null}
        </div>
      </div>

      <div className="form-actions">
        {onCancel ? (
          <button className="button button-ghost" type="button" onClick={onCancel}>
            Cancel
          </button>
        ) : null}
        <button
          className="button button-primary"
          disabled={isSubmitting || isCreatePending}
        >
          <Plus size={18} />
          Create task
        </button>
      </div>

      {isCreateError ? (
        <span className="error-text">Could not create task.</span>
      ) : null}
    </form>
  )
}
