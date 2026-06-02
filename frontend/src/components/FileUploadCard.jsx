import { FILE_UPLOAD, ERROR_MESSAGES } from '../config/constants'
import { formatFileSize } from '../utils/formatters'

function FileUploadCard({
  selectedFile,
  isLoading,
  errorMessage,
  onFileChange,
  onSubmit,
}) {
  const validateAndHandleFileChange = (event) => {
    const file = event.target.files[0]

    if (!file) {
      onFileChange(null, '')
      return
    }

    if (!file.type.startsWith('video/')) {
      onFileChange(null, ERROR_MESSAGES.invalidVideoFile)
      event.target.value = ''
      return
    }

    if (file.size > FILE_UPLOAD.maxFileSizeBytes) {
      onFileChange(
        null,
        `Plik jest za duży. Maksymalny rozmiar to ${FILE_UPLOAD.maxFileSizeMb} MB.`
      )
      event.target.value = ''
      return
    }

    onFileChange(file, '')
  }

  return (
    <section className="card">
      <h2>Prześlij film do analizy</h2>
      <p className="muted">
        Obsługiwane są standardowe pliki video, np. {FILE_UPLOAD.supportedFormatsLabel}.
      </p>

      <form onSubmit={onSubmit} className="upload-form">
        <label className="file-input">
          <span>Plik video</span>
          <input
            type="file"
            accept={FILE_UPLOAD.acceptedInputTypes}
            onChange={validateAndHandleFileChange}
            disabled={isLoading}
          />
        </label>

        {selectedFile && (
          <div className="selected-file-box">
            <p>
              <span>Wybrany plik:</span>
              <strong>{selectedFile.name}</strong>
            </p>
            <p>
              <span>Rozmiar:</span>
              <strong>{formatFileSize(selectedFile.size)}</strong>
            </p>
          </div>
        )}

        <button type="submit" disabled={isLoading || !selectedFile}>
          {isLoading ? 'Analiza w toku...' : 'Uruchom analizę'}
        </button>
      </form>

      {isLoading && (
        <div className="loading-box">
          <div className="spinner" />
          <p>
            Trwa analiza filmu. W zależności od długości nagrania może to
            potrwać kilkanaście lub kilkadziesiąt sekund.
          </p>
        </div>
      )}

      {errorMessage && (
        <div className="error-box">
          <strong>Błąd:</strong> {errorMessage}
        </div>
      )}
    </section>
  )
}

export default FileUploadCard