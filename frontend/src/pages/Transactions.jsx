
import { useState } from 'react'
import { Search, Plus, ArrowDownLeft, ArrowUpRight } from 'lucide-react'

const initialTransactions = [
  { id: 1, name: 'Monthly Salary', category: 'Income', date: '2026-11-01', amount: 45000, type: 'Income' },
  { id: 2, name: 'Grocery Shopping', category: 'Food', date: '2026-11-03', amount: 2500, type: 'Expense' },
  { id: 3, name: 'Electricity Bill', category: 'Bills', date: '2026-11-05', amount: 1800, type: 'Expense' },
  { id: 4, name: 'Freelance Project', category: 'Income', date: '2026-11-08', amount: 8000, type: 'Income' },
  { id: 5, name: 'Online Shopping', category: 'Shopping', date: '2026-11-10', amount: 3200, type: 'Expense' },
]

function Transactions() {
  const [transactions, setTransactions] = useState(initialTransactions)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('All')

  const filteredTransactions = transactions.filter((transaction) => {
    const matchesSearch = transaction.name.toLowerCase().includes(search.toLowerCase())
    const matchesFilter = filter === 'All' || transaction.type === filter
    return matchesSearch && matchesFilter
  })

  const income = transactions
    .filter((item) => item.type === 'Income')
    .reduce((sum, item) => sum + item.amount, 0)

  const expenses = transactions
    .filter((item) => item.type === 'Expense')
    .reduce((sum, item) => sum + item.amount, 0)

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">YOUR MONEY, YOUR CONTROL</p>
          <h1>Transactions</h1>
          <p className="subtitle">Keep track of every rupee coming in and going out.</p>
        </div>
        <button className="add-button" onClick={() => alert('Add transaction form coming next!')}>
          <Plus size={18} /> Add Transaction
        </button>
      </header>

      <section className="summary-grid">
        <article className="summary-card income">
          <p>Total Income</p>
          <h2>₹{income.toLocaleString('en-IN')}</h2>
          <span>Money received</span>
        </article>
        <article className="summary-card expense">
          <p>Total Expenses</p>
          <h2>₹{expenses.toLocaleString('en-IN')}</h2>
          <span>Money spent</span>
        </article>
        <article className="summary-card">
          <p>Net Balance</p>
          <h2>₹{(income - expenses).toLocaleString('en-IN')}</h2>
          <span>Income minus expenses</span>
        </article>
      </section>

      <section className="transactions-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">ACTIVITY</p>
            <h2>Recent Transactions</h2>
          </div>
        </div>

        <div className="transaction-controls">
          <div className="search-box">
            <Search size={18} />
            <input
              type="text"
              placeholder="Search transactions..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <select value={filter} onChange={(event) => setFilter(event.target.value)}>
            <option value="All">All Transactions</option>
            <option value="Income">Income</option>
            <option value="Expense">Expenses</option>
          </select>
        </div>

        <div className="transaction-list">
          {filteredTransactions.map((transaction) => (
            <div className="transaction-row" key={transaction.id}>
              <div className={`transaction-icon ${transaction.type.toLowerCase()}`}>
                {transaction.type === 'Income'
                  ? <ArrowDownLeft size={20} />
                  : <ArrowUpRight size={20} />}
              </div>

              <div className="transaction-details">
                <strong>{transaction.name}</strong>
                <span>{transaction.category} · {transaction.date}</span>
              </div>

              <strong className={`transaction-amount ${transaction.type.toLowerCase()}`}>
                {transaction.type === 'Income' ? '+' : '-'}₹
                {transaction.amount.toLocaleString('en-IN')}
              </strong>
            </div>
          ))}

          {filteredTransactions.length === 0 && (
            <p className="empty-message">No transactions found.</p>
          )}
        </div>
      </section>
    </div>
  )
}

export default Transactions
