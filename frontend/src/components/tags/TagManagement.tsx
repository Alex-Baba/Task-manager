import { Check, Pencil, Plus, Search, Tags, Trash2, X } from 'lucide-react'
import { useState } from 'react'

import type { Tag } from '../../types/api'

interface TagManagementProps {
  isCreateError: boolean
  isCreatePending: boolean
  editingTagId: string | null
  isDeleteError: boolean
  isUpdateError: boolean
  isUpdatePending: boolean
  tags: Tag[]
  onCancelEdit: () => void
  onCreate: (name: string) => Promise<unknown>
  onDelete: (tag: Tag) => void
  onEdit: (tagId: string) => void
  onSave: (tagId: string, name: string) => void
}

export function TagManagement({
  editingTagId,
  isCreateError,
  isCreatePending,
  isDeleteError,
  isUpdateError,
  isUpdatePending,
  onCancelEdit,
  onCreate,
  onDelete,
  onEdit,
  onSave,
  tags,
}: TagManagementProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [query, setQuery] = useState('')
  const normalizedQuery = query.trim().toLowerCase()
  const filteredTags = normalizedQuery
    ? tags.filter((tag) => tag.name.toLowerCase().includes(normalizedQuery))
    : tags
  const tagAlreadyExists = tags.some(
    (tag) => tag.name.toLowerCase() === normalizedQuery,
  )
  const canCreate = normalizedQuery.length > 0 && !tagAlreadyExists

  return (
    <section className="tag-management">
      <button
        className="button button-secondary full-width tag-management-trigger"
        type="button"
        onClick={() => setIsOpen((current) => !current)}
      >
        <Tags size={17} />
        Manage tags
        <span>{tags.length}</span>
      </button>

      {isOpen ? (
        <div className="tag-management-menu">
          <form
            className="tag-search-row"
            onSubmit={async (event) => {
              event.preventDefault()

              if (canCreate) {
                await onCreate(query.trim())
                setQuery('')
              }
            }}
          >
            <div className="search-field">
              <Search size={15} />
              <input
                aria-label="Search tags"
                placeholder="Search or create tag"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
            </div>
            <button
              aria-label="Create tag"
              className="icon-button icon-button-primary"
              disabled={!canCreate || isCreatePending}
              type="submit"
            >
              <Plus size={16} />
            </button>
          </form>

          <div className="tag-list">
            {filteredTags.length === 0 ? (
              <p className="empty-copy">
                {tags.length === 0 ? 'No tags created yet.' : 'No tags found.'}
              </p>
            ) : (
              filteredTags.map((tag) => (
                <TagManagementItem
                  isEditing={editingTagId === tag.id}
                  isPending={isUpdatePending}
                  key={tag.id}
                  tag={tag}
                  onCancel={onCancelEdit}
                  onDelete={() => onDelete(tag)}
                  onEdit={() => onEdit(tag.id)}
                  onSave={(name) => onSave(tag.id, name)}
                />
              ))
            )}
          </div>
          {tagAlreadyExists && normalizedQuery.length > 0 ? (
            <p className="field-hint">This tag already exists.</p>
          ) : null}
        </div>
      ) : null}
      {isCreateError ? (
        <span className="error-text">Could not create tag.</span>
      ) : null}
      {isUpdateError ? (
        <span className="error-text">Could not update tag.</span>
      ) : null}
      {isDeleteError ? (
        <span className="error-text">Could not delete tag.</span>
      ) : null}
    </section>
  )
}

function TagManagementItem({
  isEditing,
  isPending,
  onCancel,
  onDelete,
  onEdit,
  onSave,
  tag,
}: {
  isEditing: boolean
  isPending: boolean
  onCancel: () => void
  onDelete: () => void
  onEdit: () => void
  onSave: (name: string) => void
  tag: Tag
}) {
  const [name, setName] = useState(tag.name)

  if (isEditing) {
    return (
      <form
        className="tag-management-row"
        onSubmit={(event) => {
          event.preventDefault()
          const trimmedName = name.trim()

          if (trimmedName) {
            onSave(trimmedName)
          }
        }}
      >
        <input
          aria-label={`Edit ${tag.name}`}
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        <button className="icon-button" disabled={isPending} type="submit">
          <Check size={15} />
        </button>
        <button className="icon-button" type="button" onClick={onCancel}>
          <X size={15} />
        </button>
      </form>
    )
  }

  return (
    <div className="tag-management-row">
      <span className="tag-pill">#{tag.name}</span>
      <button aria-label={`Edit ${tag.name}`} className="icon-button" type="button" onClick={onEdit}>
        <Pencil size={15} />
      </button>
      <button
        aria-label={`Delete ${tag.name}`}
        className="icon-button icon-button-danger"
        type="button"
        onClick={onDelete}
      >
        <Trash2 size={15} />
      </button>
    </div>
  )
}
