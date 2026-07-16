import { FormEvent, useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CoachMessage, CoachStatus, fetchJson } from '../api'

interface ActivityLine {
  name: string
  summary: string
}

/** One in-flight assistant turn: streamed text plus tool-activity lines. */
interface LiveTurn {
  text: string
  activity: ActivityLine[]
}

export default function Coach() {
  const [messages, setMessages] = useState<CoachMessage[]>([])
  const [live, setLive] = useState<LiveTurn | null>(null)
  const [input, setInput] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [status, setStatus] = useState<CoachStatus | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const [searchParams, setSearchParams] = useSearchParams()

  // Quick links from other pages arrive as ?draft=… — pre-fill the input
  // (editable, not auto-sent) and clean the URL.
  useEffect(() => {
    const draft = searchParams.get('draft')
    if (draft) {
      setInput(draft)
      setSearchParams({}, { replace: true })
      inputRef.current?.focus()
    }
  }, [searchParams, setSearchParams])

  useEffect(() => {
    fetchJson<CoachStatus>('/api/coach/status')
      .then(setStatus)
      .catch(() => setStatus({ enabled: false, cli_available: false }))
    fetchJson<CoachMessage[]>('/api/coach/messages')
      .then(setMessages)
      .catch((e: Error) => setError(e.message))
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, live])

  const coachOff = status !== null && !status.enabled
  const cliMissing = status !== null && status.enabled && !status.cli_available

  const send = async (event: FormEvent) => {
    event.preventDefault()
    const text = input.trim()
    if (!text || busy || coachOff) return
    setInput('')
    setError(null)
    setBusy(true)
    setMessages((current) => [
      ...current,
      { id: -Date.now(), role: 'user', content: text, created_at: new Date().toISOString() }
    ])
    setLive({ text: '', activity: [] })

    try {
      const response = await fetch('/api/coach/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      })
      if (!response.ok || !response.body) {
        const detail = await response.json().catch(() => null)
        throw new Error(detail?.detail ?? `${response.status} ${response.statusText}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      for (;;) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const parts = buffer.split('\n\n')
        buffer = parts.pop() ?? ''
        for (const part of parts) {
          if (!part.startsWith('data: ')) continue
          const event = JSON.parse(part.slice(6))
          if (event.type === 'text') {
            setLive((cur) => cur && { ...cur, text: cur.text + (cur.text ? '\n\n' : '') + event.text })
          } else if (event.type === 'tool') {
            setLive((cur) => cur && {
              ...cur,
              activity: [...cur.activity, { name: event.name, summary: event.summary }]
            })
          } else if (event.type === 'error') {
            setError(event.message)
          }
        }
      }
      // Reload from the server so history matches what was persisted.
      setMessages(await fetchJson<CoachMessage[]>('/api/coach/messages'))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLive(null)
      setBusy(false)
    }
  }

  const reset = () => {
    if (!window.confirm('Start a new conversation? The chat history is cleared.')) return
    fetchJson('/api/coach/reset', { method: 'POST' })
      .then(() => setMessages([]))
      .catch((e: Error) => setError(e.message))
  }

  return (
    <div className="coach-page">
      <div className="coach-head">
        <h1>Coach</h1>
        <button className="ghost" onClick={reset} disabled={busy}>
          New conversation
        </button>
      </div>
      <p className="muted" style={{ marginTop: 0, fontSize: 13 }}>
        A Claude Code session running in the app — it can read your training data, analyze
        sessions and trends, and manage plans, notes and races through the same instructions
        as a terminal session. Uses your Claude subscription.
      </p>
      {coachOff && (
        <div className="notice-box">
          <strong>The Coach is turned off.</strong> It runs a Claude Code agent with
          shell access on this machine, so it ships disabled. To enable it, start the
          app with <code>FARTLEK_COACH_ENABLED=1</code> (only when bound to localhost).
        </div>
      )}
      {cliMissing && (
        <div className="notice-box">
          <strong>Claude Code CLI not found.</strong> Install it and run{' '}
          <code>claude</code> once to log in, then reload this page.
        </div>
      )}
      {error && <div className="error-box">{error}</div>}

      <div className="coach-thread">
        {messages.length === 0 && !live && (
          <div className="empty-state">
            Ask anything — “how was yesterday’s workout?”, “am I on track for the 5K?”,
            “move this week’s intervals to Friday”.
          </div>
        )}
        {messages.map((message) => (
          <div key={message.id} className={`coach-msg ${message.role}`}>
            {message.role === 'assistant' ? (
              <div className="markdown">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
              </div>
            ) : (
              message.content
            )}
          </div>
        ))}
        {live && (
          <div className="coach-msg assistant">
            {live.activity.map((line, i) => (
              <div key={i} className="coach-activity">
                🔧 {line.name}: <code>{line.summary}</code>
              </div>
            ))}
            {live.text ? (
              <div className="markdown">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{live.text}</ReactMarkdown>
              </div>
            ) : (
              <div className="muted">thinking…</div>
            )}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="coach-input" onSubmit={send}>
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              e.currentTarget.form?.requestSubmit()
            }
          }}
          placeholder={
            coachOff
              ? 'The coach is turned off'
              : busy
                ? 'The coach is working…'
                : 'Message the coach (Enter to send)'
          }
          rows={2}
          disabled={busy || coachOff}
        />
        <button type="submit" disabled={busy || coachOff || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}
