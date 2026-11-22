import { useState } from 'react'
import './App.css'

type FitResult = {
  matched: string[]
  missing: string[]
  strong_fit: boolean
  summary: string
}

async function postJson(url: string, body: unknown) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Something went wrong')
  return data
}

function App() {
  const [posting, setPosting] = useState('')
  const [skills, setSkills] = useState('')
  const [result, setResult] = useState<FitResult | null>(null)
  const [plan, setPlan] = useState('')
  const [declined, setDeclined] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function checkFit() {
    setLoading(true)
    setError('')
    setResult(null)
    setPlan('')
    setDeclined(false)
    try {
      setResult(await postJson('/api/fit', { posting, skills }))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  async function getPlan() {
    if (!result) return
    setLoading(true)
    setError('')
    try {
      const data = await postJson('/api/plan', { missing: result.missing })
      setPlan(data.plan)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const askAboutPlan =
    result && result.missing.length > 0 && !plan && !declined

  return (
    <main className="app">
      <h1>SkillSync</h1>
      <p className="subtitle">
        Paste a job posting and your skills to see how well you fit.
      </p>

      <label>
        Job posting
        <textarea
          rows={8}
          value={posting}
          onChange={(e) => setPosting(e.target.value)}
        />
      </label>

      <label>
        My skills
        <textarea
          rows={3}
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          placeholder="Python, SQL, Git..."
        />
      </label>

      <button onClick={checkFit} disabled={loading}>
        {loading ? 'Working...' : 'Check my fit'}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="card">
          <h2>{result.strong_fit ? 'Strong fit' : 'Not a strong fit yet'}</h2>
          <p>{result.summary}</p>
          <p>
            <strong>Matched:</strong> {result.matched.join(', ') || 'None'}
          </p>
          <p>
            <strong>Missing:</strong> {result.missing.join(', ') || 'None'}
          </p>

          {askAboutPlan && (
            <div className="ask">
              <p>Want a short plan to learn the missing skills?</p>
              <button onClick={getPlan} disabled={loading}>
                Yes, show me a plan
              </button>{' '}
              <button onClick={() => setDeclined(true)} disabled={loading}>
                No thanks
              </button>
            </div>
          )}

          {plan && <pre className="plan">{plan}</pre>}
        </section>
      )}
    </main>
  )
}

export default App