import { getStatusLabel } from '../utils/formatters'

function StatusBadge({ status }) {
  const normalizedStatus = String(status || '').toLowerCase()

  return (
    <span className={`status-badge status-${normalizedStatus}`}>
      {getStatusLabel(status)}
    </span>
  )
}

export default StatusBadge