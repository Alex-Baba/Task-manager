import { zodResolver } from '@hookform/resolvers/zod'
import { Plus } from 'lucide-react'
import { useState } from 'react'
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
  onCreateTag: (name: string) => Promise<void>
  onSubmit: (values: TaskForm) => Promise<void>
}

export function TaskCreateForm({
  categories,
  isCreateError,
  isCreatePending,
  isTagCreatePending,
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

  async function submitTask(values: TaskForm) {
    await onSubmit(values)
    reset()
    setDueDateValue('')
  }

  async function createTag(formData: FormData) {
    const name = String(formData.get('tagName') ?? '').trim()

    if (!name) {
      return
    }

    await onCreateTag(name)
  }

  return (
    <>
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
          <label htmlFor="tag_ids">Tags</label>
          <select id="tag_ids" multiple {...register('tag_ids')}>
            {tags.map((tag) => (
              <option key={tag.id} value={tag.id}>
                {tag.name}
              </option>
            ))}
          </select>
          <span className="field-hint">Hold Ctrl to select multiple tags.</span>
        </div>

        <button
          className="button button-primary"
          disabled={isSubmitting || isCreatePending}
        >
          <Plus size={18} />
          Create task
        </button>

        {isCreateError ? (
          <span className="error-text">Could not create task.</span>
        ) : null}
      </form>

      {showTagCreation ? (
        <form action={createTag} className="tag-form">
          <div className="field">
            <label htmlFor="tagName">New tag</label>
            <input id="tagName" name="tagName" placeholder="e.g. backend" />
          </div>
          <button
            className="button button-secondary"
            disabled={isTagCreatePending}
            type="submit"
          >
            <Plus size={17} />
            Create tag
          </button>
        </form>
      ) : null}
    </>
  )
}
