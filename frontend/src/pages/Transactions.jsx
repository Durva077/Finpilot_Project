
import { useEffect, useState } from 'react'
import {
  Search,
  ArrowDownLeft,
  ArrowUpRight,
  Plus,
  X,
} from 'lucide-react'
import {
  getTransactions,
  createTransaction,
} from '../api/transactionService'
import { getCategories } from '../api/categoryService'

function Transactions() {
  const [transactions, setTransactions] = useState([])
  const [categories, setCategories] = useState([])
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('All')

  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const initialFormData = {
    category_id: '',
    amount: '',
    transaction_type: 'expense',
    description: '',
    transaction_date: new Date().toISOString().slice(0, 16),
  }

  const [formData, setFormData] = useState(initialFormData)

  const fetchData = async () => {
    try {
      setLoading(true)
      setError('')

      const [transactionData, categoryData] = await Promise.all([
        getTransactions(),
        getCategories(),
      ])

      setTransactions(transactionData)
      setCategories(categoryData)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to load transactions. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleInputChange = (event) => {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  const handleAddTransaction = async (event) => {
    event.preventDefault()

    setError('')
    setSuccess('')

    if (!formData.category_id || !formData.amount || !formData.transaction_date) {
      setError('Please fill in all required fields.')
      return
    }

    if (Number(formData.amount) <= 0) {
      setError('Amount must be greater than zero.')
      return
    }

    try {
      setSaving(true)

      const transactionData = {
        ...formData,
        category_id: Number(formData.category_id),
        amount: Number(formData.amount),
        transaction_date: new Date(formData.transaction_date).toISOString(),
      }

      await createTransaction(transactionData)

      await fetchData()

      setFormData({
        ...initialFormData,
        transaction_date: new Date().toISOString().slice(0, 16),
      })

      setShowForm(false)
      setSuccess('Transaction added successfully!')
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to add transaction. Please try again.'
      )
    } finally {
      setSaving(false)
    }
  }

  const getCategoryName = (categoryId) => {
    const category = categories.find(
      (item) => item.id === categoryId
    )

    return category?.name || 'Uncategorized'
  }

  const normalizedTransactions = transactions.map((transaction) => ({
    ...transaction,
    name: transaction.description || 'Untitled transaction',
    type: transaction.transaction_type === 'income' ? 'Income' : 'Expense',
    date: transaction.transaction_date,
    category: getCategoryName(transaction.category_id),
  }))

  const filteredTransactions = normalizedTransactions.filter((transaction) => {
    const matchesSearch = transaction.name
      .toLowerCase()
      .includes(search.toLowerCase())

    const matchesFilter =
      filter === 'All' || transaction.type === filter

    return matchesSearch && matchesFilter
  })

  const income = normalizedTransactions
    .filter((item) => item.type === 'Income')
    .reduce((sum, item) => sum + Number(item.amount), 0)

  const expenses = normalizedTransactions
    .filter((item) => item.type === 'Expense')
    .reduce((sum, item) => sum + Number(item.amount), 0)

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">YOUR MONEY, YOUR CONTROL</p>
          <h1>Transactions</h1>
          <p className="subtitle">
            Keep track of every rupee coming in and going out.
          </p>
        </div>
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

          <button
            type="button"
            className="add-transaction-btn"
            onClick={() => {
              setShowForm(!showForm)
              setError('')
              setSuccess('')
            }}
          >
            {showForm ? <X size={18} /> : <Plus size={18} />}
            {showForm ? 'Cancel' : 'Add Transaction'}
          </button>
        </div>

        {showForm && (
          <form
            className="transaction-form"
            onSubmit={handleAddTransaction}
          >
            <h3>New Transaction</h3>

            <div className="form-group">
              <label>Transaction Type *</label>
              <select
                name="transaction_type"
                value={formData.transaction_type}
                onChange={(event) => {
                  const value = event.target.value
                  setFormData((previous) => ({
                    ...previous,
                    transaction_type: value,
                    category_id: '',
                  }))
                }}
                required
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>

            <div className="form-group">
              <label>Category *</label>
              <select
                name="category_id"
                value={formData.category_id}
                onChange={handleInputChange}
                required
              >
                <option value="">Select a category</option>
                {categories
                  .filter(
                    (category) =>
                      category.category_type === formData.transaction_type
                  )
                  .map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
              </select>
            </div>

            <div className="form-group">
              <label>Amount (₹) *</label>
              <input
                type="number"
                name="amount"
                placeholder="Enter amount"
                value={formData.amount}
                onChange={handleInputChange}
                min="0.01"
                step="0.01"
                required
              />
            </div>

            <div className="form-group">
              <label>Description</label>
              <input
                type="text"
                name="description"
                placeholder="e.g. Grocery shopping"
                value={formData.description}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label>Date and Time *</label>
              <input
                type="datetime-local"
                name="transaction_date"
                value={formData.transaction_date}
                onChange={handleInputChange}
                required
              />
            </div>

            <button
              type="submit"
              className="add-transaction-btn"
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save Transaction'}
            </button>
          </form>
        )}

        {success && (
          <p className="success-message">{success}</p>
        )}

        {error && (
          <p className="error-message">{error}</p>
        )}

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

          <select
            value={filter}
            onChange={(event) => setFilter(event.target.value)}
          >
            <option value="All">All Transactions</option>
            <option value="Income">Income</option>
            <option value="Expense">Expenses</option>
          </select>
        </div>

        <div className="transaction-list">
          {loading && (
            <p className="empty-message">Loading transactions...</p>
          )}

          {!loading && filteredTransactions.map((transaction) => (
            <div className="transaction-row" key={transaction.id}>
              <div className={`transaction-icon ${transaction.type.toLowerCase()}`}>
                {transaction.type === 'Income'
                  ? <ArrowDownLeft size={20} />
                  : <ArrowUpRight size={20} />}
              </div>

              <div className="transaction-details">
                <strong>{transaction.name}</strong>
                <span>
                  {transaction.category} ·{' '}
                  {new Date(transaction.date).toLocaleDateString('en-IN')}
                </span>
              </div>

              <strong className={`transaction-amount ${transaction.type.toLowerCase()}`}>
                {transaction.type === 'Income' ? '+' : '-'}₹
                {Number(transaction.amount).toLocaleString('en-IN')}
              </strong>
            </div>
          ))}

          {!loading && filteredTransactions.length === 0 && (
            <p className="empty-message">No transactions found.</p>
          )}
        </div>
      </section>
    </div>
  )
}

export default Transactions
