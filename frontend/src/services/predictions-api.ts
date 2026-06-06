import { api } from '../lib/api'
import type { Task, TaskPrediction } from '../types/api'

export interface ApplyPredictionPayload {
  apply_category: boolean
  apply_priority: boolean
}

export async function generatePrediction(taskId: string) {
  const response = await api.post<TaskPrediction>(
    `/tasks/${taskId}/predictions/generate`,
  )
  return response.data
}

export async function getActivePrediction(taskId: string) {
  const response = await api.get<TaskPrediction>(`/tasks/${taskId}/predictions/active`)
  return response.data
}

export async function applyPrediction(
  taskId: string,
  predictionId: string,
  payload: ApplyPredictionPayload,
) {
  const response = await api.post<Task>(
    `/tasks/${taskId}/predictions/${predictionId}/apply`,
    payload,
  )
  return response.data
}
