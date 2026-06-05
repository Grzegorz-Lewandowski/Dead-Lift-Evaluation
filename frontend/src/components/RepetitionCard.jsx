import { useState } from 'react'
import StatusBadge from './StatusBadge'
import ChecksList from './ChecksList'
import { getRepetitionDisplayStatus } from '../utils/formatters'

function RepetitionCard({ evaluation }) {
  const [isOpen, setIsOpen] = useState(false)

  const displayStatus = getRepetitionDisplayStatus(evaluation)
  const hasValidityReasons = evaluation.validity_reasons?.length > 0

  return (
    <article className="rep-card">
      <button
        type="button"
        className="rep-header"
        onClick={() => setIsOpen((current) => !current)}
      >
        <div className="rep-header-content">
          <h4>Powtórzenie {evaluation.rep_number}</h4>

          <p>
            {isOpen
              ? 'Ukryj szczegóły oceny techniki'
              : 'Pokaż szczegóły oceny techniki'}
          </p>
        </div>

        <StatusBadge status={displayStatus} />
      </button>

      {isOpen && hasValidityReasons && (
        <div className="validity-reasons">
          <strong>Powody:</strong>

          <ul>
            {evaluation.validity_reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </div>
      )}

      {isOpen && <ChecksList checks={evaluation.checks} />}
    </article>
  )
}

export default RepetitionCard