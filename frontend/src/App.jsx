
import './App.css'
import { BrowserRouter, Routes, Route, Link, useLocation, Navigate, Outlet, useNavigate } from 'react-router-dom'
import { LayoutDashboard, ArrowLeftRight, Wallet, ChartNoAxesCombined, Tags, UserCircle, LogOut } from 'lucide-react'

import ExpenseChart from './components/ExpenseChart.jsx'
import Transactions from './pages/Transactions.jsx'
import Budgets from './pages/Budgets.jsx'
import Analytics from './pages/Analytics.jsx'
import Categories from './pages/Categories.jsx'
import Profile from './pages/Profile.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import { useAuth } from './context/AuthContext.jsx'
import ProtectedRoute from './routes/ProtectedRoute.jsx'

function Dashboard() {
  const { user } = useAuth()

  const firstName = user?.full_name?.split(' ')[0] || 'there'
  const initial = user?.full_name?.charAt(0)?.toUpperCase() || 'U'

  return (
    <>
      <header className="topbar">
        <div>
          <p className="eyebrow">PERSONAL FINANCE</p>
          <h1>Good morning, {firstName}!</h1>
          <p className="subtitle">Here's what's happening with your money.</p>
        </div>
        <div className="profile">{initial}</div>
      </header>

      <section className="summary-grid">
        <article className="summary-card">
          <p>Total Balance</p>
          <h2>₹84,500.00</h2>
          <span>Across all accounts</span>
        </article>
        <article className="summary-card income">
          <p>Monthly Income</p>
          <h2>₹45,000.00</h2>
          <span>This month</span>
        </article>
        <article className="summary-card expense">
          <p>Monthly Expenses</p>
          <h2>₹18,250.00</h2>
          <span>This month</span>
        </article>
      </section>

      <ExpenseChart />

      <section className="welcome-card">
        <p className="eyebrow">YOUR MONEY, BETTER MANAGED</p>
        <h2>Make every rupee count.</h2>
        <p>Track your spending, stay on budget, and build better financial habits.</p>
      </section>
    </>
  )
}

const navigation = [
  { name: 'Overview', path: '/', icon: LayoutDashboard },
  { name: 'Transactions', path: '/transactions', icon: ArrowLeftRight },
  { name: 'Budgets', path: '/budgets', icon: Wallet },
  { name: 'Analytics', path: '/analytics', icon: ChartNoAxesCombined },
  { name: 'Categories', path: '/categories', icon: Tags },
  { name: 'Profile', path: '/profile', icon: UserCircle },
]

function AppLayout() {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <Link to="/" className="brand">fin<span>pilot.</span></Link>

        <p className="nav-label">MENU</p>

        <nav>
          {navigation.map(({ name, path, icon: Icon }) => (
            <Link
              key={path}
              to={path}
              className={location.pathname === path ? 'active' : ''}
            >
              <Icon size={18} />
              {name}
            </Link>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <button type="button" onClick={handleLogout}>
            <LogOut size={17} /> Logout
          </button>
          <p>YOUR FINANCES, IN FOCUS.</p>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/budgets" element={<Budgets />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
