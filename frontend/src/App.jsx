import { useEffect, useState } from 'react'
import { Login } from './components/Login.jsx'
import { Signup } from './components/Signup.jsx'
import { TodoDashboard } from './components/TodoDashboard.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { apiRequest, authStore } from './services/api.js'

export default function App() {
  const [user, setUser] = useState(null)
  const [authPage, setAuthPage] = useState('login')
  const [loading, setLoading] = useState(Boolean(authStore.get()))

  useEffect(() => {
    function clearSession() {
      setUser(null)
      setLoading(false)
    }

    window.addEventListener('daymark:unauthorized', clearSession)
    if (authStore.get()) {
      apiRequest('/auth/me')
        .then(setUser)
        .catch(clearSession)
        .finally(() => setLoading(false))
    }

    return () => window.removeEventListener('daymark:unauthorized', clearSession)
  }, [])

  function logout() {
    authStore.clear()
    setUser(null)
  }

  if (loading) return <main className="restore-screen"><p>Loading…</p></main>

  return (
    <AuthProvider value={{ user, setUser, logout }}>
      {user ? (
        <TodoDashboard />
      ) : authPage === 'signup' ? (
        <Signup onLogin={() => setAuthPage('login')} />
      ) : (
        <Login onSignup={() => setAuthPage('signup')} />
      )}
    </AuthProvider>
  )
}
