
import { useEffect, useState } from 'react'
import {
  Utensils, ShoppingBag, Car, Home,
  HeartPulse, Film, GraduationCap, Briefcase,
  Wallet, Laptop, Gift,
} from 'lucide-react'
import { getCategories } from '../api/categoryService'

const categoryIcons = [
  Utensils, ShoppingBag, Car, Home,
  HeartPulse, Film, GraduationCap, Briefcase,
  Wallet, Laptop, Gift,
]

const categoryColors = [
  '#52775B', '#D28A69', '#A5A779', '#8B9B8B',
  '#C47759', '#9B86A6', '#7894A5',
]

function Categories() {
  const [categories, setCategories] = useState([])
  const [filter, setFilter] = useState('All')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchCategories() {
      try {
        setLoading(true)
        setError('')

        const data = await getCategories()
        setCategories(data)
      } catch (err) {
        setError(
          err.response?.data?.detail || 'Unable to load categories. Please try again.'
        )
      } finally {
        setLoading(false)
      }
    }

    fetchCategories()
  }, [])

  const normalizedCategories = categories.map((category, index) => ({
    ...category,
    type: category.category_type === 'income' ? 'Income' : 'Expense',
    icon: categoryIcons[index % categoryIcons.length],
    color: categoryColors[index % categoryColors.length],
  }))

  const filteredCategories = normalizedCategories.filter(
    (category) => filter === 'All' || category.type === filter
  )

  const incomeCount = normalizedCategories.filter(
    (category) => category.type === 'Income'
  ).length

  const expenseCount = normalizedCategories.filter(
    (category) => category.type === 'Expense'
  ).length

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">ORGANIZE YOUR FINANCES</p>
          <h1>Categories</h1>
          <p className="subtitle">
            Organize your income and expenses your way.
          </p>
        </div>
      </header>

      <section className="summary-grid">
        <article className="summary-card">
          <p>Total Categories</p>
          <h2>{categories.length}</h2>
          <span>All categories</span>
        </article>

        <article className="summary-card income">
          <p>Income Categories</p>
          <h2>{incomeCount}</h2>
          <span>Money received</span>
        </article>

        <article className="summary-card expense">
          <p>Expense Categories</p>
          <h2>{expenseCount}</h2>
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

        {loading && <p className="empty-message">Loading categories...</p>}

        {error && <p className="empty-message">{error}</p>}

        {!loading && !error && (
          <>
            <div className="category-grid">
              {filteredCategories.map((category) => {
                const Icon = category.icon

                return (
                  <article className="category-card" key={category.id}>
                    <div
                      className="category-icon"
                      style={{
                        backgroundColor: `${category.color}20`,
                        color: category.color,
                      }}
                    >
                      <Icon size={22} />
                    </div>

                    <div className="category-card-info">
                      <strong>{category.name}</strong>
                      <span>{category.type}</span>
                    </div>
                  </article>
                )
              })}
            </div>

            {filteredCategories.length === 0 && (
              <p className="empty-message">No categories found.</p>
            )}
          </>
        )}
      </section>
    </div>
  )
}

export default Categories
