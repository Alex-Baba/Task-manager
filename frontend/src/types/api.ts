export type Status = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED'
export type Priority = 'LOW' | 'MEDIUM' | 'HIGH'
export type CategoryName =
  | 'WORK'
  | 'PERSONAL'
  | 'SHOPPING'
  | 'HEALTH'
  | 'FINANCE'
  | 'EDUCATION'
  | 'ENTERTAINMENT'
  | 'OTHER'

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface User {
  id: string
  username: string
  email: string
  is_admin?: boolean
  created_at?: string
  updated_at?: string
}

export interface AdminUser extends User {
  is_admin: boolean
}

export interface Category {
  id: string
  name: CategoryName
}

export interface Tag {
  id: string
  name: string
}

export interface Task {
  id: string
  title: string
  description: string | null
  status: Status
  manual_priority: Priority
  due_date: string | null
  completed_at: string | null
  user_id: string
  category_id: string | null
  tags: Tag[]
  created_at?: string
  updated_at?: string
}

export interface TaskPrediction {
  id: string
  task_id: string
  predicted_priority: Priority
  predicted_category: CategoryName
  category_confidence: number
  priority_confidence: number
  smart_score: number
  reasoning: Record<string, unknown> | null
  model_version: string | null
  is_active: boolean
  applied_category: boolean
  applied_priority: boolean
  applied_at: string | null
}
