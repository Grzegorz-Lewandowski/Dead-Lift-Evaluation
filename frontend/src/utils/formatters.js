import {
  CHECK_LABELS,
  STATUS_LABELS,
  EVALUATION_STATUS,
  REP_VALIDITY,
  REP_VALIDITY_DISPLAY_STATUS,
} from '../config/constants'

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

export function getRepetitionDisplayStatus(evaluation) {
  const validity = evaluation?.rep_validity

  if (validity === REP_VALIDITY.invalid) {
    return REP_VALIDITY_DISPLAY_STATUS.invalid
  }

  if (validity === REP_VALIDITY.partial) {
    return REP_VALIDITY_DISPLAY_STATUS.partial
  }

  return evaluation?.overall_status
}

export function buildConsistencySummary(consistencyEvaluation) {
  if (!consistencyEvaluation?.checks) {
    return 'Brak danych do oceny spójności serii.'
  }

  const checks = Object.entries(consistencyEvaluation.checks)

  const warningChecks = checks.filter(
    ([, check]) => check.status === EVALUATION_STATUS.warning
  )

  const infoChecks = checks.filter(
    ([, check]) => check.status === EVALUATION_STATUS.info
  )

  if (warningChecks.length > 0) {
    const warningNames = warningChecks
      .map(([checkName]) => formatCheckName(checkName).toLowerCase())
      .join(', ')

    return (
      `Seria wymaga uwagi. Największe różnice między powtórzeniami wykryto w obszarach: ` +
      `${warningNames}. Oznacza to, że kolejne powtórzenia nie były wykonywane w pełni powtarzalnie.`
    )
  }

  if (infoChecks.length > 0) {
    const infoNames = infoChecks
      .map(([checkName]) => formatCheckName(checkName).toLowerCase())
      .join(', ')

    return (
      `Seria jest ogólnie spójna, ale system wykrył elementy warte obserwacji: ` +
      `${infoNames}.`
    )
  }

  return (
    'Seria wygląda spójnie. Nie wykryto istotnych różnic między powtórzeniami ' +
    'w ocenianych parametrach.'
  )
}