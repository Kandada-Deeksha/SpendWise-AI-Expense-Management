import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
  Sparkles,
  User,
  Wallet,
  XCircle,
} from "lucide-react";
import api from "../services/api";

const usernameRegex = /^[A-Za-z][A-Za-z0-9_.]{2,19}$/;

const passwordRules = {
  minLength: (value) => value.length >= 8,
  uppercase: (value) => /[A-Z]/.test(value),
  lowercase: (value) => /[a-z]/.test(value),
  number: (value) => /[0-9]/.test(value),
  special: (value) => /[^A-Za-z0-9\s]/.test(value),
  noSpaces: (value) => !/\s/.test(value),
};

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [focusedField, setFocusedField] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const usernameValid = usernameRegex.test(formData.username);

  const passwordValid =
    passwordRules.minLength(formData.password) &&
    passwordRules.uppercase(formData.password) &&
    passwordRules.lowercase(formData.password) &&
    passwordRules.number(formData.password) &&
    passwordRules.special(formData.password) &&
    passwordRules.noSpaces(formData.password);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setError("");
    setSuccess("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!usernameValid) {
      setError(
        "Username must be 3–20 characters, start with a letter, and contain only letters, numbers, underscores, or dots."
      );
      return;
    }

    if (!passwordValid) {
      setError(
        "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character, with no spaces."
      );
      return;
    }

    setLoading(true);

    try {
      await api.post("/auth/register", formData);

      setSuccess("Registration successful! Redirecting to login...");

      setTimeout(() => {
        navigate("/login");
      }, 1500);
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Brand Section */}
        <section className="auth-brand-panel">
          <div className="auth-brand">
            <div className="auth-logo">
              <Wallet size={26} />
            </div>
            <span>SpendWise</span>
          </div>

          <div className="auth-brand-copy">
            <div className="auth-eyebrow">
              <Sparkles size={15} />
              Smart money management
            </div>

            <h1>
              Build better
              <br />
              financial habits.
            </h1>

            <p>
              Track your expenses, understand your spending patterns, and make
              smarter financial decisions with SpendWise.
            </p>
          </div>

          <div className="auth-feature-list">
            <div className="auth-feature-item">
              <CheckCircle2 size={19} />
              <span>Track and categorize daily expenses</span>
            </div>

            <div className="auth-feature-item">
              <CheckCircle2 size={19} />
              <span>Get AI-powered spending predictions</span>
            </div>

            <div className="auth-feature-item">
              <CheckCircle2 size={19} />
              <span>Set budgets and savings goals</span>
            </div>
          </div>
        </section>

        {/* Form Section */}
        <section className="auth-form-panel">
          <div className="auth-mobile-brand">
            <div className="auth-logo">
              <Wallet size={24} />
            </div>
            <span>SpendWise</span>
          </div>

          <div className="auth-form-header">
            <span className="auth-form-kicker">GET STARTED</span>

            <h2>Create your account</h2>

            <p>
              Start managing your finances smarter with SpendWise.
            </p>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            {/* Username */}
            <div className="auth-field">
              <label htmlFor="username">Username</label>

              <div
                className={`auth-input-wrapper ${
                  focusedField === "username" ? "auth-input-focused" : ""
                }`}
              >
                <User size={18} />

                <input
                  id="username"
                  type="text"
                  name="username"
                  placeholder="Enter your username"
                  value={formData.username}
                  onChange={handleChange}
                  onFocus={() => setFocusedField("username")}
                  onBlur={() => setFocusedField("")}
                  autoComplete="username"
                  maxLength={20}
                  required
                />
              </div>

              {focusedField === "username" && (
                <div
                  className={`auth-field-hint ${
                    formData.username && !usernameValid
                      ? "auth-field-hint-error"
                      : formData.username && usernameValid
                      ? "auth-field-hint-success"
                      : ""
                  }`}
                >
                  {formData.username && usernameValid ? (
                    <>
                      <CheckCircle2 size={14} />
                      Username is valid.
                    </>
                  ) : (
                    <>
                      <span>
                        Use 3–20 characters, start with a letter, and use only
                        letters, numbers, underscores (_) or dots (.).
                      </span>
                    </>
                  )}
                </div>
              )}
            </div>

            {/* Email */}
            <div className="auth-field">
              <label htmlFor="email">Email address</label>

              <div className="auth-input-wrapper">
                <Mail size={18} />

                <input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleChange}
                  autoComplete="email"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div className="auth-field">
              <label htmlFor="password">Password</label>

              <div
                className={`auth-input-wrapper ${
                  focusedField === "password" ? "auth-input-focused" : ""
                }`}
              >
                <LockKeyhole size={18} />

                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Create a strong password"
                  value={formData.password}
                  onChange={handleChange}
                  onFocus={() => setFocusedField("password")}
                  onBlur={() => setFocusedField("")}
                  autoComplete="new-password"
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((previous) => !previous)}
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                >
                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>
              </div>

              {focusedField === "password" && (
                <div
                  className={`auth-field-hint ${
                    formData.password && !passwordValid
                      ? "auth-field-hint-error"
                      : formData.password && passwordValid
                      ? "auth-field-hint-success"
                      : ""
                  }`}
                >
                  {formData.password && passwordValid ? (
                    <>
                      <CheckCircle2 size={14} />
                      Password meets all requirements.
                    </>
                  ) : (
                    <span>
                      Use at least 8 characters with one uppercase letter, one
                      lowercase letter, one number, one special character, and
                      no spaces.
                    </span>
                  )}
                </div>
              )}
            </div>

            {/* Error */}
            {error && (
              <div className="auth-message auth-message-error">
                <XCircle size={17} />
                <span>{error}</span>
              </div>
            )}

            {/* Success */}
            {success && (
              <div className="auth-message auth-message-success">
                <CheckCircle2 size={17} />
                <span>{success}</span>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              className="auth-submit-button"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="auth-spinner"></span>
                  Creating account...
                </>
              ) : (
                <>
                  Create account
                  <ArrowRight size={18} />
                </>
              )}
            </button>

            <div className="auth-security-note">
              <ShieldCheck size={17} />
              <span>Your account data is protected and secure.</span>
            </div>
          </form>

          {/* Login link */}
          <div className="auth-account-switch">
            <span>Already have an account?</span>

            <button
              type="button"
              onClick={() => navigate("/login")}
            >
              Sign in
              <ArrowRight size={15} />
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Register;