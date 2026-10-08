import { useEffect, useMemo, useState } from "react";
import api from "../services/api";
import {
  Area,
  BarChart,
  Bar,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const CATEGORY_COLORS = [
  "#6366f1",
  "#14b8a6",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#ec4899",
  "#06b6d4",
  "#84cc16",
];

const Analytics = () => {
  const [monthlyData, setMonthlyData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [monthlyResponse, categoryResponse] = await Promise.all([
          api.get("/analytics/monthly"),
          api.get("/analytics/categories"),
        ]);

        const monthly =
          monthlyResponse.data.monthly_expenses || [];

        const categories =
          categoryResponse.data.category_expenses || [];

        setMonthlyData(
          Array.isArray(monthly) ? monthly : []
        );

        setCategoryData(
          Array.isArray(categories)
            ? categories
            : Object.entries(categories || {}).map(
                ([category, amount]) => ({
                  category,
                  total_expense: amount,
                })
              )
        );
      } catch (err) {
        setError(
          err.response?.data?.message ||
            err.response?.data?.error ||
            "Unable to load analytics."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  const formatMonth = (month, year) => {
    const date = new Date(year, month - 1);

    return date.toLocaleDateString("en-US", {
      month: "short",
      year: "numeric",
    });
  };

  const formattedMonthlyData = useMemo(() => {
    return [...monthlyData]
      .sort((a, b) => {
        const dateA = new Date(a.year, a.month - 1);
        const dateB = new Date(b.year, b.month - 1);

        return dateA - dateB;
      })
      .map((item) => ({
        ...item,
        total_expense: Number(item.total_expense || 0),
        monthLabel: formatMonth(item.month, item.year),
      }));
  }, [monthlyData]);

  const formattedCategoryData = useMemo(() => {
    return categoryData.map((item) => ({
      ...item,
      total_expense: Number(item.total_expense || 0),
    }));
  }, [categoryData]);

  const totalSpending = formattedCategoryData.reduce(
    (total, item) => total + item.total_expense,
    0
  );

  const highestCategory =
    formattedCategoryData.length > 0
      ? formattedCategoryData.reduce((highest, current) =>
          current.total_expense > highest.total_expense
            ? current
            : highest
        )
      : null;

  const spendingTrend = useMemo(() => {
    if (formattedMonthlyData.length < 2) {
      return {
        status: "Not enough data",
        message:
          "Track at least two months of expenses to identify your spending trend.",
        icon: "—",
        className: "analytics-trend-neutral",
      };
    }

    const previous =
      formattedMonthlyData[formattedMonthlyData.length - 2]
        .total_expense;

    const current =
      formattedMonthlyData[formattedMonthlyData.length - 1]
        .total_expense;

    if (previous === 0 && current === 0) {
      return {
        status: "Stable",
        message: "Your spending has remained stable.",
        icon: "→",
        className: "analytics-trend-neutral",
      };
    }

    if (previous === 0) {
      return {
        status: "Increasing",
        message: "Your latest month shows an increase in spending.",
        icon: "↗",
        className: "analytics-trend-up",
      };
    }

    const percentageChange =
      ((current - previous) / previous) * 100;

    if (Math.abs(percentageChange) < 5) {
      return {
        status: "Stable",
        message:
          "Your spending has remained relatively stable compared with the previous month.",
        icon: "→",
        className: "analytics-trend-neutral",
      };
    }

    if (percentageChange > 0) {
      return {
        status: "Increasing",
        message: `Your spending increased by ${percentageChange.toFixed(
          1
        )}% compared with the previous month.`,
        icon: "↗",
        className: "analytics-trend-up",
      };
    }

    return {
      status: "Decreasing",
      message: `Your spending decreased by ${Math.abs(
        percentageChange
      ).toFixed(1)}% compared with the previous month.`,
      icon: "↘",
      className: "analytics-trend-down",
    };
  }, [formattedMonthlyData]);

  const currencyFormatter = (value) =>
    `₹${Number(value || 0).toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="analytics-status-card">
          <div className="analytics-loading-spinner" />
          <p>Loading your analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-page">
        <div className="analytics-error">
          <strong>Unable to load analytics</strong>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1>Analytics</h1>

          <p>
            Understand your spending patterns and track where
            your money goes.
          </p>
        </div>
      </div>

      {/* Summary */}
      <section className="analytics-summary">
        <div className="analytics-summary-card">
          <span className="analytics-summary-label">
            Total Spending
          </span>

          <h3>₹{totalSpending.toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}</h3>

          <p>Across all tracked categories</p>
        </div>

        <div className="analytics-summary-card">
          <span className="analytics-summary-label">
            Categories
          </span>

          <h3>{formattedCategoryData.length}</h3>

          <p>Expense categories tracked</p>
        </div>

        <div className="analytics-summary-card">
          <span className="analytics-summary-label">
            Highest Spending
          </span>

          <h3>
            {highestCategory
              ? highestCategory.category
              : "No data"}
          </h3>

          <p>
            {highestCategory
              ? currencyFormatter(highestCategory.total_expense)
              : "Add expenses to see insights"}
          </p>
        </div>

        <div className="analytics-summary-card">
          <span className="analytics-summary-label">
            Months Tracked
          </span>

          <h3>{formattedMonthlyData.length}</h3>

          <p>Monthly spending history</p>
        </div>
      </section>

      {/* Spending Trend Insight */}
      <section className="analytics-trend-card">
        <div
          className={`analytics-trend-icon ${spendingTrend.className}`}
        >
          {spendingTrend.icon}
        </div>

        <div className="analytics-trend-content">
          <span>Spending Trend</span>

          <h3>{spendingTrend.status}</h3>

          <p>{spendingTrend.message}</p>
        </div>
      </section>

      {/* Monthly Trend */}
      <section className="analytics-section">
        <div className="analytics-section-header">
          <div>
            <h2>Monthly Spending Trend</h2>

            <p>
              Track how your total expenses change over time.
            </p>
          </div>
        </div>

        {formattedMonthlyData.length === 0 ? (
          <div className="analytics-empty">
            <p>No monthly analytics available yet.</p>
          </div>
        ) : (
          <div className="analytics-chart">
            <ResponsiveContainer width="100%" height={370}>
              <ComposedChart
                data={formattedMonthlyData}
                margin={{
                  top: 10,
                  right: 20,
                  left: 10,
                  bottom: 10,
                }}
              >
                <defs>
                  <linearGradient
                    id="spendingAreaGradient"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop
                      offset="0%"
                      stopColor="#6366f1"
                      stopOpacity={0.25}
                    />

                    <stop
                      offset="100%"
                      stopColor="#6366f1"
                      stopOpacity={0.02}
                    />
                  </linearGradient>
                </defs>

                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="monthLabel"
                  tick={{ fontSize: 12 }}
                  tickLine={false}
                  axisLine={false}
                />

                <YAxis
                  tick={{ fontSize: 12 }}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(value) =>
                    `₹${Number(value).toLocaleString("en-IN")}`
                  }
                />

                <Tooltip
                  formatter={(value) => [
                    currencyFormatter(value),
                    "Total Expense",
                  ]}
                  labelFormatter={(label) => `Month: ${label}`}
                  contentStyle={{
                    borderRadius: "12px",
                    border: "1px solid #e5e7eb",
                    boxShadow:
                      "0 8px 24px rgba(15, 23, 42, 0.10)",
                  }}
                />

                <Area
                  type="monotone"
                  dataKey="total_expense"
                  fill="url(#spendingAreaGradient)"
                  stroke="none"
                  activeDot={false}
                />

                <Line
                  type="monotone"
                  dataKey="total_expense"
                  name="Total Expense"
                  stroke="#6366f1"
                  strokeWidth={3}
                  dot={{
                    r: 5,
                    strokeWidth: 2,
                    fill: "#ffffff",
                  }}
                  activeDot={{
                    r: 7,
                    strokeWidth: 2,
                  }}
                />

                <Legend />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        )}
      </section>

      {/* Category Analytics */}
      <section className="analytics-section">
        <div className="analytics-section-header">
          <div>
            <h2>Category-wise Spending</h2>

            <p>
              Compare your spending across different categories.
            </p>
          </div>
        </div>

        {formattedCategoryData.length === 0 ? (
          <div className="analytics-empty">
            <p>No category analytics available yet.</p>
          </div>
        ) : (
          <div className="analytics-category-grid">
            {/* Bar Chart */}
            <div className="analytics-chart analytics-chart-card">
              <div className="analytics-chart-title">
                <h3>Category Comparison</h3>
                <p>See which categories take the largest share of your spending.</p>
              </div>

              <ResponsiveContainer width="100%" height={350}>
                <BarChart
                  data={formattedCategoryData}
                  margin={{
                    top: 10,
                    right: 20,
                    left: 10,
                    bottom: 10,
                  }}
                >
                  <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                  />

                  <XAxis
                    dataKey="category"
                    tick={{ fontSize: 12 }}
                    tickLine={false}
                    axisLine={false}
                  />

                  <YAxis
                    tick={{ fontSize: 12 }}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) =>
                      `₹${Number(value).toLocaleString("en-IN")}`
                    }
                  />

                  <Tooltip
                    formatter={(value) => [
                      currencyFormatter(value),
                      "Expense",
                    ]}
                    contentStyle={{
                      borderRadius: "12px",
                      border: "1px solid #e5e7eb",
                      boxShadow:
                        "0 8px 24px rgba(15, 23, 42, 0.10)",
                    }}
                  />

                  <Legend />

                  <Bar
                    dataKey="total_expense"
                    name="Expense"
                    radius={[10, 10, 0, 0]}
                  >
                    {formattedCategoryData.map(
                      (entry, index) => (
                        <Cell
                          key={`bar-cell-${entry.category}-${index}`}
                          fill={
                            CATEGORY_COLORS[
                              index % CATEGORY_COLORS.length
                            ]
                          }
                        />
                      )
                    )}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Pie Chart */}
            <div className="analytics-chart analytics-chart-card">
              <div className="analytics-chart-title">
                <h3>Spending Distribution</h3>
                <p>See how your total spending is distributed.</p>
              </div>

              <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                  <Pie
                    data={formattedCategoryData}
                    dataKey="total_expense"
                    nameKey="category"
                    cx="50%"
                    cy="48%"
                    outerRadius={115}
                    innerRadius={55}
                    paddingAngle={3}
                    labelLine={false}
                    label={({ percent }) =>
                      `${(percent * 100).toFixed(0)}%`
                    }
                  >
                    {formattedCategoryData.map(
                      (entry, index) => (
                        <Cell
                          key={`pie-cell-${entry.category}-${index}`}
                          fill={
                            CATEGORY_COLORS[
                              index % CATEGORY_COLORS.length
                            ]
                          }
                          stroke="#ffffff"
                          strokeWidth={2}
                        />
                      )
                    )}
                  </Pie>

                  <Tooltip
                    formatter={(value) => [
                      currencyFormatter(value),
                      "Expense",
                    ]}
                    contentStyle={{
                      borderRadius: "12px",
                      border: "1px solid #e5e7eb",
                      boxShadow:
                        "0 8px 24px rgba(15, 23, 42, 0.10)",
                    }}
                  />

                  <Legend
                    verticalAlign="bottom"
                    height={36}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </section>
    </div>
  );
};

export default Analytics;