export const API_BASE_URL = 'http://127.0.0.1:8000'

export const API_ENDPOINTS = {
  analyses: `${API_BASE_URL}/api/analyses/`,
}

export const FILE_UPLOAD = {
  maxFileSizeMb: 200,
  maxFileSizeBytes: 200 * 1024 * 1024,
  acceptedInputTypes: 'video/*',
  supportedFormatsLabel: 'MP4, MOV lub AVI',
}

export const ANALYSIS_STATUS = {
  completed: 'completed',
  processing: 'processing',
  pending: 'pending',
  failed: 'failed',
}

export const EVALUATION_STATUS = {
  ok: 'OK',
  warning: 'WARNING',
  info: 'INFO',
}

export const REP_VALIDITY = {
  valid: 'valid',
  partial: 'partial',
  invalid: 'invalid',
}

export const REP_VALIDITY_DISPLAY_STATUS = {
  partial: 'PARTIAL',
  invalid: 'INVALID',
}

export const STATUS_LABELS = {
  [EVALUATION_STATUS.ok]: 'Poprawnie',
  [EVALUATION_STATUS.warning]: 'Wymaga uwagi',
  [EVALUATION_STATUS.info]: 'Informacja',

  [REP_VALIDITY_DISPLAY_STATUS.partial]: 'Częściowe',
  [REP_VALIDITY_DISPLAY_STATUS.invalid]: 'Niepoprawne',

  [ANALYSIS_STATUS.completed]: 'Zakończono',
  [ANALYSIS_STATUS.processing]: 'Analiza trwa',
  [ANALYSIS_STATUS.pending]: 'Oczekuje',
  [ANALYSIS_STATUS.failed]: 'Błąd',
}

export const CHECK_LABELS = {
  hip_lockout: 'Wyprost biodra',
  knee_lockout: 'Wyprost kolana',
  bar_range: 'Zakres ruchu sztangi',
  start_position: 'Pozycja startowa',
  start_torso_position: 'Pozycja tułowia na starcie',
  torso_angle_change: 'Zmiana pochylenia tułowia',
  tempo: 'Tempo ruchu',

  bar_range_consistency: 'Powtarzalność zakresu ruchu',
  duration_consistency: 'Powtarzalność czasu',
  hip_lockout_consistency: 'Powtarzalność wyprostu biodra',
  knee_lockout_consistency: 'Powtarzalność wyprostu kolana',
}

export const ERROR_MESSAGES = {
  noVideoSelected: 'Wybierz plik video przed uruchomieniem analizy.',
  invalidVideoFile: 'Wybrany plik nie jest plikiem video.',
  analysisFailed: 'Nie udało się wykonać analizy.',
}

export const UI_TEXT = {
  appName: 'Dead Lift Evaluation',
  mainHeading: 'Analiza techniki martwego ciągu z nagrania video',
  heroDescription:
    'Prześlij nagranie wykonane z boku. Aplikacja wykryje powtórzenia, oceni wybrane elementy techniki i pokaże wynik w czytelnej formie.',
}