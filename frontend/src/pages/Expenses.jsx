import { useEffect, useState } from "react";
import api from "../services/api";

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    category: "",
    amount: "",
    description: "",
    date: "",
  });

  const fetchExpenses = async () => {
    try {
      const response = await api.get("/expenses/");
      setExpenses(response.data.expenses || response.data);
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to load expenses."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    setError("");
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setMessage("");
    setSaving(true);

    try {
      await api.post("/expenses/", {
        category: formData.category,
        amount: Number(formData.amount),
        description: formData.description,
        expense_date: formData.date,
      });

      setFormData({
        category: "",
        amount: "",
        description: "",
        date: "",
      });

      await fetchExpenses();

      setMessage("Expense added successfully.");
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to add expense."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    setError("");
    setMessage("");
    setDeletingId(id);

    try {
      await api.delete(`/expenses/${id}`);

      await fetchExpenses();

      setMessage("Expense deleted successfully.");
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to delete expense."
      );
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) {
    return (
      <div>
        <p>Loading expenses...</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Expenses</h1>

      {error && (
        <div className="action-message action-error">
          {error}
        </div>
      )}

      {message && (
        <div className="action-message action-success">
          {message}
        </div>
      )}

      <section className="page-section">
        <h2>Add Expense</h2>

        <form
          onSubmit={handleSubmit}
          className="expense-form"
        >
          <div className="form-group">
            <label>Category</label>

            <input
              type="text"
              name="category"
              value={formData.category}
              onChange={handleChange}
              placeholder="Food, Travel, Entertainment..."
              required
            />
          </div>

          <div className="form-group">
            <label>Amount</label>

            <input
              type="number"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              placeholder="Enter amount"
              min="0"
              step="0.01"
              required
            />
          </div>

          <div className="form-group">
            <label>Description</label>

            <input
              type="text"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Optional description"
            />
          </div>

          <div className="form-group">
            <label>Date</label>

            <input
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              required
            />
          </div>

          <button
            type="submit"
            disabled={saving}
          >
            {saving ? "Adding..." : "Add Expense"}
          </button>
        </form>
      </section>

      <section className="page-section">
        <h2>Expense History</h2>

        {expenses.length === 0 ? (
          <p>No expenses found.</p>
        ) : (
          <table className="expense-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Category</th>
                <th>Description</th>
                <th>Amount</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {expenses.map((expense) => (
                <tr key={expense.id}>
                  <td>{expense.expense_date}</td>

                  <td>{expense.category}</td>

                  <td>
                    {expense.description || "-"}
                  </td>

                  <td>
                    ₹
                    {Number(
                      expense.amount
                    ).toFixed(2)}
                  </td>

                  <td>
                    <button
                      onClick={() =>
                        handleDelete(expense.id)
                      }
                      disabled={
                        deletingId === expense.id
                      }
                    >
                      {deletingId === expense.id
                        ? "Deleting..."
                        : "Delete"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
};

export default Expenses;