export const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function isValidEmail(email) {
  return emailRegex.test(email || '')
}

export function isPdfFile(file) {
  return file && file.name.toLowerCase().endsWith('.pdf')
}

export const MAX_RESUME_MB = 10

export function isWithinSizeLimit(file) {
  return file && file.size <= MAX_RESUME_MB * 1024 * 1024
}
