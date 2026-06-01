import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000/api/analyses/'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleFileChange = (event) => {
    const file = event.target.files[0]

    setSelectedFile(file)
    setAnalysis(null)
    setErrorMessage('')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!selectedFile) {
      setErrorMessage('Wybierz plik video przed uruchomieniem analizy.')
      return
    }

    const formData = new FormData()
    formData.append('video', selectedFile)

    setIsLoading(true)
    setErrorMessage('')
    setAnalysis(null)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error_message || 'Nie udało się wykonać analizy.')
      }

      setAnalysis(data)
    } catch (error) {
      setErrorMessage(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">Dead Lift Evaluation</p>
        <h1>Analiza techniki martwego ciągu z nagrania video</h1>
        <p className="hero-description">
          Prześlij nagranie z boku, uruchom analizę i otrzymaj ocenę każdego
          powtórzenia oraz spójności całej serii.
        </p>
      </section>

      <section className="card">
        <h2>Prześlij film do analizy</h2>

        <form onSubmit={handleSubmit} className="upload-form">
          <label className="file-input">
            <span>Plik video</span>
            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              disabled={isLoading}
            />
          </label>

          {selectedFile && (
            <p className="selected-file">
              Wybrany plik: <strong>{selectedFile.name}</strong>
            </p>
          )}

          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Analiza w toku...' : 'Uruchom analizę'}
          </button>
        </form>

        {isLoading && (
          <div className="loading-box">
            <div className="spinner" />
            <p>
              Trwa analiza filmu. To może potrwać kilkanaście lub kilkadziesiąt
              sekund.
            </p>
          </div>
        )}

        {errorMessage && (
          <div className="error-box">
            <strong>Błąd:</strong> {errorMessage}
          </div>
        )}
      </section>

      {analysis && <AnalysisResults analysis={analysis} />}
    </main>
  )
}

function AnalysisResults({ analysis }) {
  const result = analysis.result

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
        <SummaryItem label="Status" value={analysis.status} />
        <SummaryItem
          label="Liczba powtórzeń"
          value={result?.repetitions_count ?? '-'}
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

      <div className="card">
        <h3>Ocena powtórzeń</h3>

        {result?.evaluations?.length > 0 ? (
          <div className="repetitions-list">
            {result.evaluations.map((evaluation) => (
              <RepetitionCard
                key={evaluation.rep_number}
                evaluation={evaluation}
              />
            ))}
          </div>
        ) : (
          <p>Brak wykrytych powtórzeń.</p>
        )}
      </div>

      {result?.consistency_evaluation && (
        <div className="card">
          <div className="section-title-row">
            <h3>Spójność serii</h3>
            <StatusBadge status={result.consistency_evaluation.overall_status} />
          </div>

          <ChecksList checks={result.consistency_evaluation.checks} />
        </div>
      )}
    </section>
  )
}

function RepetitionCard({ evaluation }) {
  return (
    <article className="rep-card">
      <div className="section-title-row">
        <h4>Powtórzenie {evaluation.rep_number}</h4>
        <StatusBadge status={evaluation.overall_status} />
      </div>

      <ChecksList checks={evaluation.checks} />
    </article>
  )
}

function ChecksList({ checks }) {
  return (
    <div className="checks-list">
      {Object.entries(checks).map(([checkName, check]) => (
        <div key={checkName} className="check-row">
          <StatusBadge status={check.status} />
          <div>
            <p className="check-name">{formatCheckName(checkName)}</p>
            <p className="check-message">{check.message}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

function SummaryItem({ label, value }) {
  return (
    <div className="summary-item">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function StatusBadge({ status }) {
  const normalizedStatus = String(status || '').toLowerCase()

  return (
    <span className={`status-badge status-${normalizedStatus}`}>
      {status}
    </span>
  )
}

function formatCheckName(checkName) {
  const names = {
    hip_lockout: 'Wyprost biodra',
    knee_lockout: 'Wyprost kolana',
    bar_range: 'Zakres ruchu sztangi',
    torso_angle_change: 'Zmiana pochylenia tułowia',
    tempo: 'Tempo ruchu',
    bar_range_consistency: 'Powtarzalność zakresu ruchu',
    duration_consistency: 'Powtarzalność czasu',
    hip_lockout_consistency: 'Powtarzalność wyprostu biodra',
    knee_lockout_consistency: 'Powtarzalność wyprostu kolana',
  }

  return names[checkName] || checkName
}

export default App