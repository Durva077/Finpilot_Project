
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

const expenseData = [
  { name: 'Shopping', value: 5200, color: '#52775B' },
  { name: 'Food', value: 4500, color: '#D28A69' },
  { name: 'Bills', value: 3750, color: '#A5A779' },
  { name: 'Travel', value: 2800, color: '#8B9B8B' },
  { name: 'Others', value: 2000, color: '#C7B99D' },
]

function ExpenseChart() {
  return (
    <div className="chart-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">SPENDING OVERVIEW</p>
          <h2>Where your money goes</h2>
        </div>
        <span className="chart-period">This month</span>
      </div>

      <div className="chart-content">
        <div className="chart">
          <ResponsiveContainer width="100%" height={155}>
            <PieChart>
              <Pie
                data={expenseData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={43}
                outerRadius={62}
                paddingAngle={4}
              >
                {expenseData.map((item) => (
                  <Cell key={item.name} fill={item.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-legend">
          {expenseData.map((item) => (
            <div className="legend-item" key={item.name}>
              <span
                className="legend-dot"
                style={{ backgroundColor: item.color }}
              />
              <span>{item.name}</span>
              <strong>₹{item.value.toLocaleString('en-IN')}</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ExpenseChart
