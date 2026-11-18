
import { useState } from 'react'
import { Plus, Wallet, TrendingUp } from 'lucide-react'

const initialBudgets = [
  { id: 1, category: 'Food & Dining', limit: 8000, spent: 5200, color: '#52775B' },
  { id: 2, category: 'Shopping', limit: 6000, spent: 4200, color: '#D28A69' },
  { id: 3, category: 'Transportation', limit: 4000, spent: 1800, color: '#A5A779' },
  { id: 4, category: 'Bills & Utilities', limit: 5000, spent: 3750, color: '#8B9B8B' },
  { id: 5, category: 'Entertainment', limit: 3000, spent: 1200, color: '#C7B99D' },
]

function Budgets() {
  const [budgets] = useState(initialBudgets)

  const totalLimit = budgets.reduce((sum, item) => sum + item.limit, 0)
  const totalSpent = budgets.reduce((sum, item) => sum + item.spent, 0)
  const remaining = totalLimit - totalSpent

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">PLAN YOUR SPENDING</p>
          <h1>Budgets</h1>
          <p className="subtitle">Set limits, track progress, and stay in control.</p>
        </div>
        <button
          className="add-button"
          onClick={() => alert('Budget creation form coming next!')}
        >
          <Plus size={18} /> Create Budget
        </button>
      </header>

      <section className="summary-grid">
        <article className="summary-card">
          <p>Total Budget</p>
          <h2>₹{totalLimit.toLocaleString('en-IN')}</h2>
          <span>Planned spending</span>
        </article>

        <article className="summary-card expense">
          <p>Total Spent</p>
          <h2>₹{totalSpent.toLocaleString('en-IN')}</h2>
          <span>Spent this month</span>
        </article>

        <article className="summary-card income">
          <p>Remaining</p>
          <h2>₹{remaining.toLocaleString('en-IN')}</h2>
          <span>Available to spend</span>
        </article>
      </section>

      <section className="transactions-card budgets-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">MONTHLY OVERVIEW</p>
            <h2>Category Budgets</h2>
          </div>
          <span className="chart-period">November 2026</span>
        </div>

        <div className="budget-list">
          {budgets.map((budget) => {
            const percentage = Math.round((budget.spent / budget.limit) * 100)
            const isOverBudget = percentage >= 100

            return (
              <div className="budget-item" key={budget.id}>
                <div className="budget-info">
                  <div className="budget-category">
                    <span
                      className="budget-dot"
                      style={{ backgroundColor: budget.color }}
                    />
                    <strong>{budget.category}</strong>
                  </div>

                  <span className="budget-percentage">
                    {percentage}% used
                  </span>
                </div>

                <div className="budget-progress">
                  <div
                    className={`budget-progress-fill ${isOverBudget ? 'over-budget' : ''}`}
                    style={{
                      width: `${Math.min(percentage, 100)}%`,
                      backgroundColor: isOverBudget ? '#c47759' : budget.color,
                    }}
                  />
                </div>

                <div className="budget-amounts">
                  <span>
                    ₹{budget.spent.toLocaleString('en-IN')} spent
                  </span>
                  <strong>
                    ₹{budget.limit.toLocaleString('en-IN')} limit
                  </strong>
                </div>
              </div>
            )
          })}
        </div>
      </section>

      <section className="welcome-card budget-tip">
        <Wallet size={24} />
        <div>
          <p className="eyebrow">A LITTLE FINANCIAL TIP</p>
          <h2>Keep an eye on your spending.</h2>
          <p>Review your category budgets regularly to avoid overspending.</p>
        </div>
        <TrendingUp size={28} />
      </section>
    </div>
  )
}

export default Budgets
