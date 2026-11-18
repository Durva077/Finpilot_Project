
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell,
} from 'recharts'
import { TrendingUp, TrendingDown, PiggyBank } from 'lucide-react'

const monthlyData = [
  { month: 'Jun', income: 40000, expenses: 22000 },
  { month: 'Jul', income: 42000, expenses: 25000 },
  { month: 'Aug', income: 45000, expenses: 28000 },
  { month: 'Sep', income: 43000, expenses: 24000 },
  { month: 'Oct', income: 47000, expenses: 26000 },
  { month: 'Nov', income: 45000, expenses: 18250 },
]

const categoryData = [
  { name: 'Shopping', value: 5200, color: '#D28A69' },
  { name: 'Food', value: 4500, color: '#52775B' },
  { name: 'Bills', value: 3750, color: '#8B9B8B' },
  { name: 'Travel', value: 2800, color: '#A5A779' },
  { name: 'Others', value: 2000, color: '#C7B99D' },
]

function Analytics() {
  const totalIncome = 45000
  const totalExpenses = 18250
  const savings = totalIncome - totalExpenses
  const savingsRate = Math.round((savings / totalIncome) * 100)

  return (
    <div className="page-content">
      <header className="page-header">
        <div>
          <p className="eyebrow">UNDERSTAND YOUR MONEY</p>
          <h1>Analytics</h1>
          <p className="subtitle">Insights into your income, spending, and savings.</p>
        </div>
        <span className="chart-period">November 2026</span>
      </header>

      <section className="summary-grid">
        <article className="summary-card income">
          <p><TrendingUp size={15} /> Total Income</p>
          <h2>₹{totalIncome.toLocaleString('en-IN')}</h2>
          <span>This month</span>
        </article>

        <article className="summary-card expense">
          <p><TrendingDown size={15} /> Total Expenses</p>
          <h2>₹{totalExpenses.toLocaleString('en-IN')}</h2>
          <span>This month</span>
        </article>

        <article className="summary-card">
          <p><PiggyBank size={15} /> Savings</p>
          <h2>₹{savings.toLocaleString('en-IN')}</h2>
          <span>{savingsRate}% of your income</span>
        </article>
      </section>

      <section className="transactions-card analytics-chart-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">FINANCIAL TRENDS</p>
            <h2>Income vs Expenses</h2>
          </div>
          <span className="chart-period">Last 6 months</span>
        </div>

        <div className="analytics-chart">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyData} margin={{ top: 15, right: 10, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#eeeae1" />
              <XAxis dataKey="month" axisLine={false} tickLine={false} />
              <YAxis
                axisLine={false}
                tickLine={false}
                tickFormatter={(value) => `₹${value / 1000}k`}
              />
              <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
              <Bar dataKey="income" name="Income" fill="#52775B" radius={[5, 5, 0, 0]} />
              <Bar dataKey="expenses" name="Expenses" fill="#D28A69" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="transactions-card analytics-chart-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">SPENDING BREAKDOWN</p>
            <h2>Expenses by Category</h2>
          </div>
        </div>

        <div className="analytics-category-layout">
          <div className="analytics-pie">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={categoryData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={65}
                  outerRadius={95}
                  paddingAngle={4}
                >
                  {categoryData.map((item) => (
                    <Cell key={item.name} fill={item.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="analytics-legend">
            {categoryData.map((item) => (
              <div className="legend-item" key={item.name}>
                <span className="legend-dot" style={{ backgroundColor: item.color }} />
                <span>{item.name}</span>
                <strong>₹{item.value.toLocaleString('en-IN')}</strong>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="welcome-card analytics-insight">
        <TrendingUp size={25} />
        <div>
          <p className="eyebrow">YOUR MONTHLY INSIGHT</p>
          <h2>You're saving {savingsRate}% of your income!</h2>
          <p>Your income is higher than your expenses this month. Keep building that healthy savings habit.</p>
        </div>
      </section>
    </div>
  )
}

export default Analytics
