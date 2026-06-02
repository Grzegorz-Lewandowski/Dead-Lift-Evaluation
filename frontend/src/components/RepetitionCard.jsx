import { useState } from 'react'
import StatusBadge from './StatusBadge'
import ChecksList from './ChecksList'

function RepetitionCard({ evaluation }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <article className="rep-card">
      <button
        type="button"
        className="rep-header"
        onClick={() => setIsOpen((current) => !current)}
      >
        <div>
          <h4>Powtórzenie {evaluation.rep_number}</h4>
          <p>
            {isOpen
              ? 'Ukryj szczegóły oceny techniki'
              : 'Pokaż szczegóły oceny techniki'}
          </p>
        </div>

        <StatusBadge status={evaluation.overall_status} />
      </button>

      {isOpen && <ChecksList checks={evaluation.checks} />}
    </article>
  )
}

export default RepetitionCard