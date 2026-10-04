import { NavLink, Outlet, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Receipt,
  Wallet,
  Target,
  BarChart3,
  User,
  LogOut,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

const MainLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const navItems = [
    {
      label: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      label: "Expenses",
      path: "/expenses",
      icon: Receipt,
    },
    {
      label: "Budget",
      path: "/budget",
      icon: Wallet,
    },
    {
      label: "Savings Goals",
      path: "/savings-goals",
      icon: Target,
    },
    {
      label: "Analytics",
      path: "/analytics",
      icon: BarChart3,
    },
    {
      label: "Profile",
      path: "/profile",
      icon: User,
    },
  ];

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-inner">
          <div
            className="app-brand"
            onClick={() => navigate("/dashboard")}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                navigate("/dashboard");
              }
            }}
          >
            <div className="app-brand-icon">
              ₹
            </div>

            <div className="app-brand-text">
              <span className="app-brand-name">
                SpendWise
              </span>

              <span className="app-brand-tagline">
                Smart Expense Management
              </span>
            </div>
          </div>

          <nav className="main-navigation">
            {navItems.map((item) => {
              const Icon = item.icon;

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `nav-link ${isActive ? "active" : ""}`
                  }
                >
                  <Icon size={18} strokeWidth={2} />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          <div className="header-user-area">
            <div className="header-user">
              <div className="header-user-avatar">
                {(user?.name || user?.username || "U")
                  .charAt(0)
                  .toUpperCase()}
              </div>

              <div className="header-user-info">
                <span className="header-user-label">
                  Welcome
                </span>

                <strong>
                  {user?.name || user?.username || "User"}
                </strong>
              </div>
            </div>

            <button
              type="button"
              className="logout-button"
              onClick={handleLogout}
              title="Logout"
            >
              <LogOut size={17} />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
};

export default MainLayout;