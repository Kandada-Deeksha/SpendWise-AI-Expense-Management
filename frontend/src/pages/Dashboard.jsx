import { useEffect, useState } from "react";
import api from "../services/api";
import {
  Wallet,
  TrendingUp,
  PiggyBank,
  Target,
} from "lucide-react";

const Dashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [savingsGoals, setSavingsGoals] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [
          dashboardResponse,
          alertsResponse,
          savingsGoalsResponse,
        ] = await Promise.all([
          api.get("/dashboard/summary"),
          api.get("/alerts/"),
          api.get("/savings-goals/"),
        ]);

        setDashboard(dashboardResponse.data);

        setAlerts(alertsResponse.data.alerts || []);

        setSavingsGoals(
          savingsGoalsResponse.data.goals ||
            savingsGoalsResponse.data ||
            []
        );
      } catch (err) {
        setError(
          err.response?.data?.message ||
            err.response?.data?.error ||
            "Unable to load dashboard."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!dashboard) {
    return <p>No dashboard data available.</p>;
  }

  const currency = dashboard.currency || "INR";

  const predictedExpense =
    dashboard.prediction?.predicted_next_month_expense;

  const recommendedBudget =
    dashboard.prediction?.recommended_next_month_budget;

  const predictionAvailable =
    predictedExpense !== null &&
    predictedExpense !== undefined;

  const recommendationAvailable =
    recommendedBudget !== null &&
    recommendedBudget !== undefined;

  return (
    <div>
      <h1>SpendWise Dashboard</h1>

      {/* =========================
          MONTHLY OVERVIEW
      ========================== */}
      <section>
        <h2>Monthly Overview</h2>

        <div className="dashboard-cards">
          <div className="dashboard-card">
            <Wallet size={28} />

            <h3>Monthly Expenses</h3>

            <p>
              {currency}{" "}
              {Number(
                dashboard.monthly_expenses || 0
              ).toFixed(2)}
            </p>
          </div>

          <div className="dashboard-card">
            <TrendingUp size={28} />

            <h3>Total Expenses</h3>

            <p>
              {currency}{" "}
              {Number(
                dashboard.total_expenses || 0
              ).toFixed(2)}
            </p>
          </div>

          <div className="dashboard-card">
            <PiggyBank size={28} />

            <h3>Budget</h3>

            <p>
              {currency}{" "}
              {Number(
                dashboard.budget?.amount || 0
              ).toFixed(2)}
            </p>
          </div>

          <div className="dashboard-card">
            <Target size={28} />

            <h3>Next Month Prediction</h3>

            <p>
              {predictionAvailable
                ? `${currency} ${Number(
                    predictedExpense
                  ).toFixed(2)}`
                : "Not available"}
            </p>
          </div>
        </div>
      </section>

      {/* =========================
          BUDGET OVERVIEW
      ========================== */}
      <section>
        <h2>Budget Overview</h2>

        <p>
          Budget: {currency}{" "}
          {Number(
            dashboard.budget?.amount || 0
          ).toFixed(2)}
        </p>

        <p>
          Spent: {currency}{" "}
          {Number(
            dashboard.budget?.spent || 0
          ).toFixed(2)}
        </p>

        <p>
          Remaining: {currency}{" "}
          {Number(
            dashboard.budget?.remaining || 0
          ).toFixed(2)}
        </p>

        <p>
          Usage:{" "}
          {Number(
            dashboard.budget?.usage_percentage || 0
          ).toFixed(2)}
          %
        </p>

        <div className="budget-progress">
          <div
            className="budget-progress-bar"
            style={{
              width: `${Math.min(
                Number(
                  dashboard.budget?.usage_percentage || 0
                ),
                100
              )}%`,
            }}
          />
        </div>
      </section>

      {/* =========================
          AI FINANCIAL INSIGHTS
      ========================== */}
      <section>
        <h2>AI Financial Insights</h2>

        <div className="insight-card">
          <h3>Predicted Next Month Expense</h3>

          {predictionAvailable ? (
            <>
              <p>
                {currency}{" "}
                {Number(predictedExpense).toFixed(2)}
              </p>

              <small>
                Based on your historical spending patterns.
              </small>
            </>
          ) : (
            <>
              <p>Prediction not available yet</p>

              <small>
                Add at least 3 months of expense history
                to receive an AI-based prediction.
              </small>
            </>
          )}
        </div>

        <div className="insight-card">
          <h3>Recommended Next Month Budget</h3>

          {recommendationAvailable ? (
            <>
              <p>
                {currency}{" "}
                {Number(recommendedBudget).toFixed(2)}
              </p>

              <small>
                Includes an AI-based safety buffer to help
                control overspending.
              </small>
            </>
          ) : (
            <>
              <p>Recommendation not available yet</p>

              <small>
                Your personalized budget recommendation
                will appear after enough spending history
                is available for the AI model.
              </small>
            </>
          )}
        </div>
      </section>

      {/* =========================
          CATEGORY-WISE EXPENSES
      ========================== */}
      <section>
        <h2>Category-wise Expenses</h2>

        {Object.entries(
          dashboard.category_wise_expenses || {}
        ).length === 0 ? (
          <p>
            No category expenses available yet.
          </p>
        ) : (
          <div className="category-expenses">
            {Object.entries(
              dashboard.category_wise_expenses || {}
            ).map(([category, amount]) => (
              <div
                className="category-expense-card"
                key={category}
              >
                <h3>{category}</h3>

                <p>
                  {currency}{" "}
                  {Number(amount).toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* =========================
          ALERTS
      ========================== */}
      <section>
        <h2>Alerts</h2>

        {alerts.length === 0 ? (
          <p>
            No alerts. Your spending is currently
            under control.
          </p>
        ) : (
          alerts.map((alert, index) => (
            <div
              key={index}
              className={`alert-card ${
                alert.severity || "medium"
              }`}
            >
              <strong>
                {alert.severity === "high"
                  ? "High Priority"
                  : alert.severity === "medium"
                  ? "Warning"
                  : "Notice"}
              </strong>

              <p>{alert.message}</p>
            </div>
          ))
        )}
      </section>

      {/* =========================
          SAVINGS GOALS
      ========================== */}
      <section>
        <h2>Savings Goals</h2>

        {savingsGoals.length === 0 ? (
          <p>
            No savings goals yet. Create a savings goal
            to start tracking your progress.
          </p>
        ) : (
          <div className="savings-goals-dashboard">
            {savingsGoals.map((goal) => {
              const target = Number(
                goal.target_amount || 0
              );

              const current = Number(
                goal.current_amount || 0
              );

              const progress =
                target > 0
                  ? Math.min(
                      (current / target) * 100,
                      100
                    )
                  : 0;

              return (
                <div
                  className="savings-goal-card"
                  key={goal.id}
                >
                  <h3>
                    {goal.goal_name ||
                      goal.name ||
                      "Savings Goal"}
                  </h3>

                  <p>
                    {currency}{" "}
                    {current.toFixed(2)} /{" "}
                    {currency}{" "}
                    {target.toFixed(2)}
                  </p>

                  <p>
                    Progress:{" "}
                    {progress.toFixed(1)}%
                  </p>

                  <div className="savings-progress">
                    <div
                      className="savings-progress-bar"
                      style={{
                        width: `${progress}%`,
                      }}
                    />
                  </div>

                  {goal.target_date && (
                    <p>
                      Target Date:{" "}
                      {goal.target_date}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
};

export default Dashboard;