import { API_ENDPOINTS, ERROR_MESSAGES } from '../config/constants'

export async function uploadVideoForAnalysis(videoFile) {
  const formData = new FormData()
  formData.append('video', videoFile)

  const response = await fetch(API_ENDPOINTS.analyses, {
    method: 'POST',
    body: formData,
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error_message || ERROR_MESSAGES.analysisFailed)
  }

  return data
}