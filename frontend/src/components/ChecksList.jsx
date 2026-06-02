import StatusBadge from './StatusBadge'
import { formatCheckName } from '../utils/formatters'

function ChecksList({ checks }) {
  if (!checks || Object.keys(checks).length === 0) {
    return <p className="muted">Brak szczegółowych ocen.</p>
  }

  return (
    <div className="checks-list">
      {Object.entries(checks).map(([checkName, check]) => (
        <div key={checkName} className="check-row">
          <div className="check-content">
            <p className="check-name">{formatCheckName(checkName)}</p>
            <p className="check-message">{check.message}</p>
          </div>

          <StatusBadge status={check.status} />
        </div>
      ))}
    </div>
  )
}

export default ChecksList