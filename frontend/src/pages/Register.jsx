
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Wallet } from 'lucide-react'

function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  })
  const [error, setError] = useState('')

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value })
    setError('')
  }

  function handleSubmit(event) {
    event.preventDefault()

    if (form.password.length < 8) {
      setError('Password must contain at least 8 characters.')
      return
    }

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    navigate('/login')
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h1 className="brand">fin<span>pilot.</span></h1>
        <div className="auth-icon"><Wallet size={25} /></div>
        <p className="eyebrow">GET STARTED</p>
        <h2>Create your account</h2>
        <p className="subtitle">Start managing your money smarter.</p>

        <label>Full Name</label>
        <input name="name" value={form.name} onChange={handleChange} placeholder="Your name" required />

        <label>Email Address</label>
        <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="you@example.com" required />

        <label>Password</label>
        <input name="password" type="password" value={form.password} onChange={handleChange} placeholder="At least 8 characters" required />

        <label>Confirm Password</label>
        <input name="confirmPassword" type="password" value={form.confirmPassword} onChange={handleChange} placeholder="Enter password again" required />

        {error && <p className="error-message">{error}</p>}

        <button className="add-button auth-submit" type="submit">Create Account</button>

        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </form>
    </div>
  )
}

export default Register
