
import { useState } from 'react'
import {
  Plus, Utensils, ShoppingBag, Car, Home,
  HeartPulse, Film, GraduationCap, Briefcase,
  Wallet, Laptop, Gift, Trash2,
} from 'lucide-react'

const initialCategories = [
  { id: 1, name: 'Food & Dining', type: 'Expense', icon: Utensils, color: '#52775B' },
  { id: 2, name: 'Shopping', type: 'Expense', icon: ShoppingBag, color: '#D28A69' },
  { id: 3, name: 'Transportation', type: 'Expense', icon: Car, color: '#A5A779' },
  { id: 4, name: 'Bills & Utilities', type: 'Expense', icon: Home, color: '#8B9B8B' },
  { id: 5, name: 'Healthcare', type: 'Expense', icon: HeartPulse, color: '#C47759' },
  { id: 6, name: 'Entertainment', type: 'Expense', icon: Film, color: '#9B86A6' },
  { id: 7, name: 'Education', type: 'Expense', icon: GraduationCap, color: '#7894A5' },
  { id: 8, name: 'Salary', type: 'Income', icon: Briefcase, color: '#52775B' },
  { id: 9, name: 'Freelance', type: 'Income', icon: Laptop, color: '#7894A5' },
  { id: 10, name: 'Gifts', type: 'Income', icon: Gift, color: '#D28A69' },
]

function Categories() {
  const [categories, setCategories] = useState(initialCategories)
  const [filter, setFilter] = useState('All')
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [type, setType] = useState('Expense')

  const filteredCategories = categories.filter(
    (category) => filter === 'All' || category.type === filter
  )

  function addCategory(event) {
    event.preventDefault()

    const trimmedName = name.trim()
    if (!trimmedName) return

    const duplicate = categories.some(
      (category) => category.name.toLowerCase() === trimmedName.toLowerCase()
        && category.type === type
    )

    if (duplicate) {
      alert('This category already exists.')
      return
    }

    setCategories((previous) => [
      ...previous,
      {
        id: Date.now(),
        name: trimmedName,
        type,
        icon: Wallet,
        color: '#52775B',
      },
    ])

    setName('')
    setType('Expense')
    setShowForm(false)
  }

  function deleteCategory(id) {
    setCategories((previous) => previous.filter((item) => item.id !== id))
  }

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">ORGANIZE YOUR FINANCES</p>
          <h1>Categories</h1>
          <p className="subtitle">Organize your income and expenses your way.</p>
        </div>

        <button className="add-button" onClick={() => setShowForm(!showForm)}>
          <Plus size={18} /> Add Category
        </button>
      </header>

      {showForm && (
        <form className="category-form" onSubmit={addCategory}>
          <h2>Create a category</h2>

          <label htmlFor="category-name">Category name</label>
          <input
            id="category-name"
            type="text"
            placeholder="e.g. Groceries"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />

          <label htmlFor="category-type">Category type</label>
          <select
            id="category-type"
            value={type}
            onChange={(event) => setType(event.target.value)}
          >
            <option value="Expense">Expense</option>
            <option value="Income">Income</option>
          </select>

          <div className="category-form-actions">
            <button type="submit" className="add-button">Save Category</button>
            <button
              type="button"
              className="cancel-button"
              onClick={() => setShowForm(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <section className="summary-grid">
        <article className="summary-card">
          <p>Total Categories</p>
          <h2>{categories.length}</h2>
          <span>All categories</span>
        </article>

        <article className="summary-card income">
          <p>Income Categories</p>
          <h2>{categories.filter((item) => item.type === 'Income').length}</h2>
          <span>Money received</span>
        </article>

        <article className="summary-card expense">
          <p>Expense Categories</p>
          <h2>{categories.filter((item) => item.type === 'Expense').length}</h2>
          <span>Money spent</span>
        </article>
      </section>

      <section className="transactions-card categories-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">YOUR ORGANIZATION</p>
            <h2>All Categories</h2>
          </div>

          <select
            className="category-filter"
            value={filter}
            onChange={(event) => setFilter(event.target.value)}
          >
            <option value="All">All Categories</option>
            <option value="Income">Income</option>
            <option value="Expense">Expenses</option>
          </select>
        </div>

        <div className="category-grid">
          {filteredCategories.map((category) => {
            const Icon = category.icon

            return (
              <article className="category-card" key={category.id}>
                <div
                  className="category-icon"
                  style={{ backgroundColor: `${category.color}20`, color: category.color }}
                >
                  <Icon size={22} />
                </div>

                <div className="category-card-info">
                  <strong>{category.name}</strong>
                  <span>{category.type}</span>
                </div>

                <button
                  className="delete-category"
                  title={`Delete ${category.name}`}
                  aria-label={`Delete ${category.name}`}
                  onClick={() => deleteCategory(category.id)}
                >
                  <Trash2 size={17} />
                </button>
              </article>
            )
          })}
        </div>

        {filteredCategories.length === 0 && (
          <p className="empty-message">No categories found.</p>
        )}
      </section>
    </div>
  )
}

export default Categories
