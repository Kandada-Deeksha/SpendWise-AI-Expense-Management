import { useEffect, useState } from "react";
import api from "../services/api";

const Profile = () => {
  const [profile, setProfile] = useState(null);

  const [formData, setFormData] = useState({
    age: "",
    occupation: "",
    city_tier: "",
    income: "",
    desired_savings_percentage: "",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const fetchProfile = async () => {
    try {
      const response = await api.get(
        "/financial-profile/"
      );

      const data =
        response.data.profile ||
        response.data;

      setProfile(data);

      setFormData({
        age: data.age ?? "",
        occupation: data.occupation ?? "",
        city_tier: data.city_tier ?? "",
        income: data.monthly_income ?? "",
        desired_savings_percentage:
          data.desired_savings_percentage ?? "",
      });
    } catch (err) {
      if (err.response?.status === 404) {
        setProfile(null);

        setFormData({
          age: "",
          occupation: "",
          city_tier: "",
          income: "",
          desired_savings_percentage: "",
        });
      } else {
        setError(
          err.response?.data?.message ||
            err.response?.data?.error ||
            "Unable to load financial profile."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
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

    const updatedProfileData = {
      age: Number(formData.age),
      occupation: formData.occupation,
      city_tier: formData.city_tier,
      monthly_income: Number(formData.income),
      desired_savings_percentage: Number(
        formData.desired_savings_percentage
      ),
    };

    try {
      const response = await api.post(
        "/financial-profile/",
        updatedProfileData
      );

      const savedProfile =
        response.data.profile ||
        response.data;

      /*
       * Immediately update the displayed profile.
       * If the backend returns only a success message,
       * use the values that were just submitted.
       */
      const updatedProfile = {
        ...savedProfile,

        age:
          savedProfile.age ??
          updatedProfileData.age,

        occupation:
          savedProfile.occupation ??
          updatedProfileData.occupation,

        city_tier:
          savedProfile.city_tier ??
          updatedProfileData.city_tier,

        monthly_income:
          savedProfile.monthly_income ??
          updatedProfileData.monthly_income,

        desired_savings_percentage:
          savedProfile.desired_savings_percentage ??
          updatedProfileData.desired_savings_percentage,
      };

      setProfile(updatedProfile);

      /*
       * Keep the form synchronized with the saved
       * values as well.
       */
      setFormData({
        age: updatedProfile.age ?? "",
        occupation:
          updatedProfile.occupation ?? "",
        city_tier:
          updatedProfile.city_tier ?? "",
        income:
          updatedProfile.monthly_income ?? "",
        desired_savings_percentage:
          updatedProfile.desired_savings_percentage ??
          "",
      });

      setMessage(
        "Financial profile updated successfully."
      );
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Unable to save financial profile."
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="profile-page">
        <p className="profile-status">
          Loading profile...
        </p>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <h1>Financial Profile</h1>

        <p>
          Your financial profile helps SpendWise
          generate personalized predictions and
          recommendations.
        </p>
      </div>

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
        <h2>
          Personal & Financial Information
        </h2>

        <form
          onSubmit={handleSubmit}
          className="profile-form"
        >
          <div className="form-group">
            <label>Age</label>

            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleChange}
              min="1"
              required
            />
          </div>

          <div className="form-group">
            <label>Occupation</label>

            <select
              name="occupation"
              value={formData.occupation}
              onChange={handleChange}
              required
            >
              <option value="">
                Select occupation
              </option>

              <option value="Salaried">
                Salaried
              </option>

              <option value="Self-employed/Business">
                Self-employed / Business
              </option>

              <option value="Student">
                Student
              </option>
            </select>
          </div>

          <div className="form-group">
            <label>City Tier</label>

            <select
              name="city_tier"
              value={formData.city_tier}
              onChange={handleChange}
              required
            >
              <option value="">
                Select city tier
              </option>

              <option value="Tier 1">
                Tier 1
              </option>

              <option value="Tier 2">
                Tier 2
              </option>

              <option value="Tier 3">
                Tier 3
              </option>
            </select>
          </div>

          <div className="form-group">
            <label>Monthly Income</label>

            <input
              type="number"
              name="income"
              value={formData.income}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </div>

          <div className="form-group">
            <label>
              Desired Savings Percentage
            </label>

            <input
              type="number"
              name="desired_savings_percentage"
              value={
                formData.desired_savings_percentage
              }
              onChange={handleChange}
              min="0"
              max="100"
              step="0.01"
              placeholder="Example: 20"
              required
            />
          </div>

          <button
            type="submit"
            className="profile-save-button"
            disabled={saving}
          >
            {saving
              ? "Saving..."
              : "Save Profile"}
          </button>
        </form>
      </section>

      {profile && (
        <section className="page-section">
          <h2>Current Profile</h2>

          <div className="profile-summary">
            <div className="profile-summary-card">
              <span>Age</span>

              <strong>
                {profile.age}
              </strong>
            </div>

            <div className="profile-summary-card">
              <span>Occupation</span>

              <strong>
                {profile.occupation}
              </strong>
            </div>

            <div className="profile-summary-card">
              <span>City Tier</span>

              <strong>
                {profile.city_tier}
              </strong>
            </div>

            <div className="profile-summary-card">
              <span>Monthly Income</span>

              <strong>
                ₹
                {Number(
                  profile.monthly_income || 0
                ).toFixed(2)}
              </strong>
            </div>

            <div className="profile-summary-card">
              <span>Desired Savings</span>

              <strong>
                {Number(
                  profile.desired_savings_percentage ||
                    0
                ).toFixed(2)}
                %
              </strong>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default Profile;