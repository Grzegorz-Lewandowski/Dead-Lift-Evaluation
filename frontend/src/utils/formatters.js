import { CHECK_LABELS, STATUS_LABELS } from '../config/constants'

export function formatCheckName(checkName) {
  return CHECK_LABELS[checkName] || checkName
}

export function formatFileSize(sizeInBytes) {
  if (!sizeInBytes) {
    return '-'
  }

  const sizeInMb = sizeInBytes / (1024 * 1024)
  return `${sizeInMb.toFixed(2)} MB`
}

export function getStatusLabel(status) {
  return STATUS_LABELS[status] || status
}