import { useState } from 'react'
import './App.css'

import AnalysisResults from './components/AnalysisResults'
import FileUploadCard from './components/FileUploadCard'
import InstructionCard from './components/InstructionCard'
import { uploadVideoForAnalysis } from './services/analysisApi'
import { ERROR_MESSAGES, UI_TEXT } from './config/constants'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleFileChange = (file, validationError = '') => {
    setSelectedFile(file)
    setAnalysis(null)
    setErrorMessage(validationError)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!selectedFile) {
      setErrorMessage(ERROR_MESSAGES.noVideoSelected)
      return
    }

    setIsLoading(true)
    setErrorMessage('')
    setAnalysis(null)

    try {
      const data = await uploadVideoForAnalysis(selectedFile)
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
        <p className="eyebrow">{UI_TEXT.appName}</p>
        <h1>{UI_TEXT.mainHeading}</h1>
        <p className="hero-description">{UI_TEXT.heroDescription}</p>
      </section>

      <InstructionCard />

      <FileUploadCard
        selectedFile={selectedFile}
        isLoading={isLoading}
        errorMessage={errorMessage}
        onFileChange={handleFileChange}
        onSubmit={handleSubmit}
      />

      {analysis && <AnalysisResults analysis={analysis} />}
    </main>
  )
}

export default App