import { useEffect, useState } from "react";
import api from "../services/api";

const SavingsGoals = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    name: "",
    target_amount: "",
    current_amount: "",
    target_date: "",
  });

  const fetchGoals = async () => {
    try {
      const response = await api.get("/savings-goals/");
      setGoals(response.data.goals || response.data);
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to load savings goals."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGoals();
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
      await api.post("/savings-goals/", {
        goal_name: formData.name,
        target_amount: Number(
          formData.target_amount
        ),
        current_amount: Number(
          formData.current_amount || 0
        ),
        target_date: formData.target_date,
      });

      setFormData({
        name: "",
        target_amount: "",
        current_amount: "",
        target_date: "",
      });

      await fetchGoals();

      setMessage(
        "Savings goal created successfully."
      );
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to create savings goal."
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
      await api.delete(
        `/savings-goals/${id}`
      );

      await fetchGoals();

      setMessage(
        "Savings goal deleted successfully."
      );
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to delete savings goal."
      );
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) {
    return (
      <div>
        <p>Loading savings goals...</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Savings Goals</h1>

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
        <h2>Create Savings Goal</h2>

        <form
          onSubmit={handleSubmit}
          className="savings-form"
        >
          <div className="form-group">
            <label>Goal Name</label>

            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Emergency Fund, New Laptop..."
              required
            />
          </div>

          <div className="form-group">
            <label>Target Amount</label>

            <input
              type="number"
              name="target_amount"
              value={formData.target_amount}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </div>

          <div className="form-group">
            <label>Current Amount</label>

            <input
              type="number"
              name="current_amount"
              value={formData.current_amount}
              onChange={handleChange}
              min="0"
              step="0.01"
            />
          </div>

          <div className="form-group">
            <label>Target Date</label>

            <input
              type="date"
              name="target_date"
              value={formData.target_date}
              onChange={handleChange}
            />
          </div>

          <button
            type="submit"
            disabled={saving}
          >
            {saving
              ? "Creating..."
              : "Create Goal"}
          </button>
        </form>
      </section>

      <section className="page-section">
        <h2>Your Goals</h2>

        {goals.length === 0 ? (
          <p>No savings goals yet.</p>
        ) : (
          goals.map((goal) => {
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
                <h3>{goal.goal_name}</h3>

                <p>
                  ₹{current.toFixed(2)} / ₹
                  {target.toFixed(2)}
                </p>

                <p>
                  Progress:{" "}
                  {progress.toFixed(1)}%
                </p>

                <div className="savings-goal-progress">
                  <div
                    className="savings-goal-progress-bar"
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

                <button
                  onClick={() =>
                    handleDelete(goal.id)
                  }
                  disabled={
                    deletingId === goal.id
                  }
                >
                  {deletingId === goal.id
                    ? "Deleting..."
                    : "Delete"}
                </button>
              </div>
            );
          })
        )}
      </section>
    </div>
  );
};

export default SavingsGoals;