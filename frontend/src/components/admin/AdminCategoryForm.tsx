import { useState } from 'react'

import type { Category, CategoryName } from '../../types/api'

const CATEGORY_OPTIONS: CategoryName[] = [
  'WORK',
  'PERSONAL',
  'SHOPPING',
  'HEALTH',
  'FINANCE',
  'EDUCATION',
  'ENTERTAINMENT',
  'OTHER',
]

interface AdminCategoryFormProps {
  categories: Category[]
  isError: boolean
  isPending: boolean
  onCreateCategory: (name: CategoryName) => void
}

export function AdminCategoryForm({
  categories,
  isError,
  isPending,
  onCreateCategory,
}: AdminCategoryFormProps) {
  const [categoryName, setCategoryName] = useState<CategoryName>('WORK')
  const existingCategoryNames = new Set(
    categories.map((category) => category.name),
  )
  const missingCategories = CATEGORY_OPTIONS.filter(
    (category) => !existingCategoryNames.has(category),
  )

  return (
    <>
      <form
        className="form"
        onSubmit={(event) => {
          event.preventDefault()
          onCreateCategory(categoryName)
        }}
      >
        <div className="field">
          <label htmlFor="admin-category">Category</label>
          <select
            id="admin-category"
            value={categoryName}
            onChange={(event) => setCategoryName(event.target.value as CategoryName)}
          >
            {CATEGORY_OPTIONS.map((category) => (
              <option
                disabled={existingCategoryNames.has(category)}
                key={category}
                value={category}
              >
                {category}
              </option>
            ))}
          </select>
        </div>

        <button
          className="button button-primary"
          disabled={isPending || missingCategories.length === 0}
        >
          Create category
        </button>
      </form>

      {missingCategories.length === 0 ? (
        <p className="status-line">All categories already exist.</p>
      ) : null}
      {isError ? <p className="error-text">Could not create category.</p> : null}
    </>
  )
}
