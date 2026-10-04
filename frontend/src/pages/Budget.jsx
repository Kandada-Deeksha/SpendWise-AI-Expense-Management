import { useEffect, useState } from "react";
import { Pencil, X } from "lucide-react";
import api from "../services/api";

const MONTHS = [
  { value: 1, label: "January" },
  { value: 2, label: "February" },
  { value: 3, label: "March" },
  { value: 4, label: "April" },
  { value: 5, label: "May" },
  { value: 6, label: "June" },
  { value: 7, label: "July" },
  { value: 8, label: "August" },
  { value: 9, label: "September" },
  { value: 10, label: "October" },
  { value: 11, label: "November" },
  { value: 12, label: "December" },
];

const Budget = () => {
  const today = new Date();

  const [budgets, setBudgets] = useState([]);
  const [selectedMonth, setSelectedMonth] = useState(
    today.getMonth() + 1
  );
  const [selectedYear, setSelectedYear] = useState(
    today.getFullYear()
  );

  const [amount, setAmount] = useState("");
  const [editing, setEditing] = useState(false);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const currentBudget = budgets.find(
    (item) =>
      item.month === Number(selectedMonth) &&
      item.year === Number(selectedYear)
  );

  const fetchBudgets = async () => {
    try {
      setError("");

      const response = await api.get("/budget/");
      const data = response.data || [];

      setBudgets(data);
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to load budgets."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBudgets();
  }, []);

  useEffect(() => {
    if (currentBudget && !editing) {
      setAmount(currentBudget.amount);
    }

    if (!currentBudget && !editing) {
      setAmount("");
    }
  }, [selectedMonth, selectedYear, currentBudget, editing]);

  const handleMonthChange = (e) => {
    setSelectedMonth(Number(e.target.value));
    setEditing(false);
    setMessage("");
    setError("");
  };

  const handleYearChange = (e) => {
    setSelectedYear(Number(e.target.value));
    setEditing(false);
    setMessage("");
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setMessage("");
    setSaving(true);

    try {
      const budgetData = {
        amount: Number(amount),
        month: Number(selectedMonth),
        year: Number(selectedYear),
      };

      if (currentBudget) {
        await api.put(
          `/budget/${currentBudget.id}`,
          budgetData
        );

        setMessage(
          "Budget updated successfully."
        );
      } else {
        await api.post("/budget/", budgetData);

        setMessage(
          "Budget created successfully."
        );
      }

      setEditing(false);

      await fetchBudgets();
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to save budget."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = () => {
    if (!currentBudget) {
      return;
    }

    setAmount(currentBudget.amount);
    setEditing(true);
    setMessage("");
    setError("");
  };

  const handleCancelEdit = () => {
    setEditing(false);
    setError("");
    setMessage("");

    if (currentBudget) {
      setAmount(currentBudget.amount);
    }
  };

  const selectedMonthName =
    MONTHS.find(
      (month) => month.value === Number(selectedMonth)
    )?.label || "";

  if (loading) {
    return (
      <div className="budget-page">
        <p className="budget-status">
          Loading budgets...
        </p>
      </div>
    );
  }

  return (
    <div className="budget-page">
      <div className="budget-header">
        <h1>Budget</h1>

        <p>
          Set and manage your monthly spending limits
          with SpendWise.
        </p>
      </div>

      {error && (
        <div className="budget-message budget-error">
          {error}
        </div>
      )}

      {message && (
        <div className="budget-message budget-success">
          {message}
        </div>
      )}

      <section className="page-section">
        <div className="budget-section-header">
          <div>
            <h2>
              {currentBudget && !editing
                ? "Manage Monthly Budget"
                : currentBudget && editing
                ? "Update Monthly Budget"
                : "Set Monthly Budget"}
            </h2>

            <p>
              Select a month and year, then set your
              spending limit.
            </p>
          </div>
        </div>

        <form
          onSubmit={handleSubmit}
          className="budget-form"
        >
          <div className="budget-form-row">
            <div className="form-group">
              <label htmlFor="budget-month">
                Month
              </label>

              <select
                id="budget-month"
                value={selectedMonth}
                onChange={handleMonthChange}
              >
                {MONTHS.map((month) => (
                  <option
                    key={month.value}
                    value={month.value}
                  >
                    {month.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="budget-year">
                Year
              </label>

              <select
                id="budget-year"
                value={selectedYear}
                onChange={handleYearChange}
              >
                {Array.from(
                  { length: 5 },
                  (_, index) =>
                    today.getFullYear() - 1 + index
                ).map((year) => (
                  <option
                    key={year}
                    value={year}
                  >
                    {year}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="budget-amount">
              Budget Amount
            </label>

            <input
              id="budget-amount"
              type="number"
              value={amount}
              onChange={(e) =>
                setAmount(e.target.value)
              }
              placeholder="Enter monthly budget"
              min="0"
              step="0.01"
              required
            />
          </div>

          <div className="budget-form-actions">
            <button
              type="submit"
              disabled={saving}
            >
              {saving
                ? "Saving..."
                : currentBudget
                ? "Update Budget"
                : "Set Budget"}
            </button>

            {editing && (
              <button
                type="button"
                className="budget-cancel-button"
                onClick={handleCancelEdit}
                disabled={saving}
              >
                <X size={16} />
                Cancel
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="page-section">
        <div className="budget-section-header">
          <div>
            <h2>
              {selectedMonthName} {selectedYear}
            </h2>

            <p>
              Budget information for the selected
              month.
            </p>
          </div>

          {currentBudget && !editing && (
            <button
              type="button"
              className="budget-edit-button"
              onClick={handleEdit}
            >
              <Pencil size={16} />
              Edit Budget
            </button>
          )}
        </div>

        {currentBudget ? (
          <div className="budget-summary">
            <div className="budget-summary-card">
              <span>Monthly Budget</span>

              <strong>
                ₹
                {Number(
                  currentBudget.amount || 0
                ).toFixed(2)}
              </strong>
            </div>

            <div className="budget-summary-card">
              <span>Month</span>

              <strong>
                {selectedMonthName}
              </strong>
            </div>

            <div className="budget-summary-card">
              <span>Year</span>

              <strong>
                {selectedYear}
              </strong>
            </div>
          </div>
        ) : (
          <div className="budget-empty">
            <p>
              No budget has been set for{" "}
              <strong>
                {selectedMonthName} {selectedYear}
              </strong>
              .
            </p>

            <span>
              Enter an amount above to create a
              budget for this month.
            </span>
          </div>
        )}
      </section>
    </div>
  );
};

export default Budget;