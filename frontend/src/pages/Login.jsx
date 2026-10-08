import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  Wallet,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    if (error) {
      setError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/login", formData);

      const { access_token, user } = response.data;

      login(access_token, user);

      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Invalid email or password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* =========================
            BRAND PANEL
        ========================== */}
        <div className="auth-brand-panel">
          <div className="auth-brand-content">
            <button
              type="button"
              className="auth-logo"
              onClick={() => navigate("/login")}
            >
              <span className="auth-logo-icon">
                <Wallet size={22} />
              </span>

              <span>SpendWise</span>
            </button>

            <div className="auth-brand-copy">
              <div className="auth-eyebrow">
                <Sparkles size={15} />
                Smart personal finance
              </div>

              <h1>
                Take control of
                <br />
                your money.
              </h1>

              <p>
                Track your spending, understand your habits,
                and make smarter financial decisions with
                AI-powered insights.
              </p>
            </div>

            <div className="auth-feature-list">
              <div className="auth-feature">
                <div className="auth-feature-icon">
                  <TrendingUp size={18} />
                </div>

                <div>
                  <strong>Understand your spending</strong>
                  <span>
                    See where your money goes every month.
                  </span>
                </div>
              </div>

              <div className="auth-feature">
                <div className="auth-feature-icon">
                  <Sparkles size={18} />
                </div>

                <div>
                  <strong>AI-powered predictions</strong>
                  <span>
                    Get intelligent insights from your history.
                  </span>
                </div>
              </div>

              <div className="auth-feature">
                <div className="auth-feature-icon">
                  <ShieldCheck size={18} />
                </div>

                <div>
                  <strong>Build better habits</strong>
                  <span>
                    Stay on track with budgets and goals.
                  </span>
                </div>
              </div>
            </div>

            <div className="auth-brand-footer">
              <span className="auth-footer-dot" />
              Your smarter financial journey starts here.
            </div>
          </div>
        </div>

        {/* =========================
            LOGIN PANEL
        ========================== */}
        <div className="auth-form-panel">
          <div className="auth-form-wrapper">
            <div className="auth-mobile-brand">
              <div className="auth-mobile-logo">
                <Wallet size={20} />
              </div>

              <span>SpendWise</span>
            </div>

            <div className="auth-form-header">
              <span className="auth-form-kicker">
                Welcome back
              </span>

              <h2>Sign in to your account</h2>

              <p>
                Continue managing your finances with SpendWise.
              </p>
            </div>

            {error && (
              <div className="auth-message auth-message-error">
                <span>{error}</span>
              </div>
            )}

            <form
              className="auth-form"
              onSubmit={handleSubmit}
            >
              <div className="auth-field">
                <label htmlFor="login-email">
                  Email address
                </label>

                <div className="auth-input-wrapper">
                  <Mail
                    size={18}
                    className="auth-input-icon"
                  />

                  <input
                    id="login-email"
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="you@example.com"
                    autoComplete="email"
                    required
                  />
                </div>
              </div>

              <div className="auth-field">
                <label htmlFor="login-password">
                  Password
                </label>

                <div className="auth-input-wrapper">
                  <LockKeyhole
                    size={18}
                    className="auth-input-icon"
                  />

                  <input
                    id="login-password"
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    autoComplete="current-password"
                    required
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowPassword(!showPassword)
                    }
                    aria-label={
                      showPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showPassword ? (
                      <EyeOff size={18} />
                    ) : (
                      <Eye size={18} />
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="auth-submit-button"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="auth-spinner" />
                    Signing in...
                  </>
                ) : (
                  <>
                    Sign in
                    <ArrowRight size={18} />
                  </>
                )}
              </button>
            </form>

            <div className="auth-divider">
              <span />
              <span>New to SpendWise?</span>
              <span />
            </div>

            <button
              type="button"
              className="auth-secondary-button"
              onClick={() => navigate("/register")}
            >
              Create a new account
            </button>

            <p className="auth-security-note">
              <ShieldCheck size={15} />
              Your financial data stays private and secure.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;