import StatusBadge from './StatusBadge'
import SummaryItem from './SummaryItem'
import RepetitionCard from './RepetitionCard'
import ChecksList from './ChecksList'
import { buildConsistencySummary } from '../utils/formatters'

function AnalysisResults({ analysis }) {
  const result = analysis.result

  if (!result) {
    return null
  }

  return (
    <section className="results">
      <div className="results-header">
        <div>
          <p className="eyebrow">Wyniki analizy</p>
          <h2>{analysis.video_filename}</h2>
        </div>

        <StatusBadge status={analysis.status} />
      </div>

      <div className="summary-grid">
        <SummaryItem label="Status analizy" value={analysis.status} />
        <SummaryItem
          label="Liczba powtórzeń"
          value={result.repetitions_count ?? '-'}
        />
        <SummaryItem
          label="Czas analizy"
          value={
            analysis.analysis_duration_seconds
              ? `${analysis.analysis_duration_seconds}s`
              : '-'
          }
        />
      </div>

      <section className="card">
        <div className="section-title-row">
          <div>
            <h3>Ocena powtórzeń</h3>
            <p className="muted">
              Każde powtórzenie oceniane jest osobno na podstawie wybranych
              parametrów biomechanicznych.
            </p>
          </div>
        </div>

        {result.evaluations?.length > 0 ? (
          <div className="repetitions-list">
            {result.evaluations.map((evaluation) => (
              <RepetitionCard
                key={evaluation.rep_number}
                evaluation={evaluation}
              />
            ))}
          </div>
        ) : (
          <p className="muted">Nie wykryto powtórzeń w przesłanym filmie.</p>
        )}
      </section>

        {result.consistency_evaluation && (
          <section className="card">
            <div className="section-title-row">
              <div>
                <h3>Spójność serii</h3>
                <p className="muted consistency-summary">
                  {buildConsistencySummary(result.consistency_evaluation)}
                </p>
              </div>

              <StatusBadge status={result.consistency_evaluation.overall_status} />
            </div>

            <ChecksList checks={result.consistency_evaluation.checks} />
          </section>
        )}
    </section>
  )
}

export default AnalysisResults