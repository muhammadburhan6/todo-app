const TOKEN_KEY = 'daymark_token'

export const authStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
}

export async function apiRequest(path, options = {}) {
  const token = authStore.get()
  const headers = {
    ...(options.body ? { 'Content-Type': 'application/json' } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  }

  const response = await fetch(path, { ...options, headers })
  const data = await response.json().catch(() => null)

  if (!response.ok) {
    if (response.status === 401 && token) {
      authStore.clear()
      window.dispatchEvent(new CustomEvent('daymark:unauthorized'))
    }

    const error = new Error(
      data?.detail || data?.message || 'Something went wrong. Please try again.',
    )
    error.status = response.status
    throw error
  }

  return data
}
