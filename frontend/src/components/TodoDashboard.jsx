import { useEffect, useMemo, useRef, useState } from 'react'
import { useAuth } from '../context/AuthContext.jsx'
import { useTheme } from '../context/ThemeContext.jsx'
import { apiRequest } from '../services/api.js'

const FILTERS = ['all', 'active', 'completed']

function normalizeTodo(todo) {
  return { ...todo, completed: todo.is_completed }
}

export function TodoDashboard() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const [tasks, setTasks] = useState([])
  const [filter, setFilter] = useState('all')
  const [newTitle, setNewTitle] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [creating, setCreating] = useState(false)
  const [busyIds, setBusyIds] = useState(new Set())

  useEffect(() => {
    let active = true
    apiRequest('/todos')
      .then((items) => active && setTasks(items.map(normalizeTodo)))
      .catch((requestError) => {
        if (active && requestError.status !== 401) setError(requestError.message)
      })
      .finally(() => active && setLoading(false))

    return () => { active = false }
  }, [])

  const visibleTasks = useMemo(() => {
    if (filter === 'active') return tasks.filter((task) => !task.completed)
    if (filter === 'completed') return tasks.filter((task) => task.completed)
    return tasks
  }, [filter, tasks])

  const counts = useMemo(() => {
    const completed = tasks.filter((task) => task.completed).length
    return { all: tasks.length, active: tasks.length - completed, completed }
  }, [tasks])

  function setBusy(taskId, busy) {
    setBusyIds((current) => {
      const next = new Set(current)
      if (busy) next.add(taskId)
      else next.delete(taskId)
      return next
    })
  }

  async function loadTasks() {
    setLoading(true)
    setError('')
    try {
      const items = await apiRequest('/todos')
      setTasks(items.map(normalizeTodo))
    } catch (requestError) {
      if (requestError.status !== 401) setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  async function createTask(event) {
    event.preventDefault()
    const title = newTitle.trim()
    if (title.length < 3) return

    setCreating(true)
    setError('')
    try {
      const task = await apiRequest('/todos', {
        method: 'POST',
        body: JSON.stringify({ title }),
      })
      setTasks((current) => [normalizeTodo(task), ...current])
      setNewTitle('')
      setFilter('all')
    } catch (requestError) {
      if (requestError.status !== 401) setError(requestError.message)
    } finally {
      setCreating(false)
    }
  }

  async function updateTask(taskId, changes) {
    setBusy(taskId, true)
    setError('')
    try {
      const task = await apiRequest(`/todos/${taskId}`, {
        method: 'PATCH',
        body: JSON.stringify({
          ...(changes.title !== undefined ? { title: changes.title } : {}),
          ...(changes.completed !== undefined
            ? { is_completed: changes.completed }
            : {}),
        }),
      })
      setTasks((current) =>
        current.map((item) => item.id === taskId ? normalizeTodo(task) : item),
      )
      return true
    } catch (requestError) {
      if (requestError.status !== 401) setError(requestError.message)
      return false
    } finally {
      setBusy(taskId, false)
    }
  }

  async function deleteTask(taskId) {
    setBusy(taskId, true)
    setError('')
    try {
      await apiRequest(`/todos/${taskId}`, { method: 'DELETE' })
      setTasks((current) => current.filter((task) => task.id !== taskId))
    } catch (requestError) {
      if (requestError.status !== 401) setError(requestError.message)
    } finally {
      setBusy(taskId, false)
    }
  }

  return (
    <main className="app-page">
      <section className="app-panel" aria-labelledby="tasks-title">
        <header className="app-header">
          <button type="button" className="theme-toggle" onClick={toggleTheme}>
            {theme === 'light' ? 'Dark mode' : 'Light mode'}
          </button>
          <div className="account">
            <span title={user?.email}>{user?.email}</span>
            <button type="button" onClick={logout}>Log out</button>
          </div>
        </header>

        <div className="app-content">
          <div className="workspace-heading">
            <div>
              <p className="eyebrow">Your day, clearly planned</p>
              <h1 id="tasks-title">My tasks</h1>
            </div>
            <span className="task-summary">
              {counts.active} {counts.active === 1 ? 'task' : 'tasks'} left
            </span>
          </div>

          <form className="quick-add" onSubmit={createTask}>
            <label className="sr-only" htmlFor="new-task">Add a task</label>
            <input
              id="new-task"
              value={newTitle}
              onChange={(event) => setNewTitle(event.target.value)}
              placeholder="Add a task"
              disabled={creating}
              minLength={3}
              maxLength={120}
            />
            <button
              className="primary-button"
              disabled={creating || newTitle.trim().length < 3}
            >
              {creating ? 'Adding…' : 'Add'}
            </button>
          </form>

          <div className="filters" role="tablist" aria-label="Filter tasks">
            {FILTERS.map((item) => (
              <button
                type="button"
                role="tab"
                aria-selected={filter === item}
                key={item}
                onClick={() => setFilter(item)}
              >
                <span>{item[0].toUpperCase() + item.slice(1)}</span>
                <span className="filter-count">{counts[item]}</span>
              </button>
            ))}
          </div>

          {error && (
            <div className="load-error" role="alert">
              <span>{error}</span>
              <button type="button" onClick={loadTasks}>Retry</button>
            </div>
          )}

          {loading ? (
            <p className="status-text">Loading tasks…</p>
          ) : visibleTasks.length ? (
            <ul className="task-list">
              {visibleTasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  busy={busyIds.has(task.id)}
                  onToggle={() => updateTask(task.id, { completed: !task.completed })}
                  onUpdate={updateTask}
                  onDelete={deleteTask}
                />
              ))}
            </ul>
          ) : (
            <p className="empty-state">No {filter === 'all' ? '' : `${filter} `}tasks yet.</p>
          )}
        </div>
      </section>
    </main>
  )
}

function TaskItem({ task, busy, onToggle, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false)
  const [title, setTitle] = useState(task.title)
  const inputRef = useRef(null)

  useEffect(() => {
    if (editing) inputRef.current?.focus()
  }, [editing])

  function cancelEdit() {
    setTitle(task.title)
    setEditing(false)
  }

  async function saveEdit(event) {
    event.preventDefault()
    const cleanTitle = title.trim()
    if (cleanTitle.length < 3) return
    if (cleanTitle === task.title || await onUpdate(task.id, { title: cleanTitle })) {
      setEditing(false)
    }
  }

  return (
    <li className={`task-row ${task.completed ? 'task-row--complete' : ''} ${busy ? 'task-row--busy' : ''}`}>
      <button
        type="button"
        className="task-check"
        aria-label={`Mark ${task.title} ${task.completed ? 'active' : 'completed'}`}
        aria-pressed={task.completed}
        onClick={onToggle}
        disabled={busy}
      >
        {task.completed ? '✓' : ''}
      </button>

      <div className="task-main">
        {editing ? (
          <form className="edit-form" onSubmit={saveEdit}>
            <input
              ref={inputRef}
              aria-label="Edit task"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              onKeyDown={(event) => event.key === 'Escape' && cancelEdit()}
              minLength={3}
              maxLength={120}
            />
            <button className="text-action" disabled={busy}>Save</button>
            <button type="button" className="text-action muted" onClick={cancelEdit}>Cancel</button>
          </form>
        ) : (
          <span className="task-title">{task.title}</span>
        )}
      </div>

      {!editing && (
        <div className="task-actions">
          <button type="button" className="text-action" onClick={() => setEditing(true)} disabled={busy}>Edit</button>
          <button type="button" className="text-action danger" onClick={() => onDelete(task.id)} disabled={busy}>Delete</button>
        </div>
      )}
    </li>
  )
}
