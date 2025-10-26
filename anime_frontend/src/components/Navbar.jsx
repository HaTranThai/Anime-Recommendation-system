import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/Navbar.css";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      {/* LOGO */}
      <div className="navbar-left">
        <Link to="/" className="navbar-logo-link">
          <img
            src="https://i.etsystatic.com/25683926/r/il/8b9921/2650373813/il_fullxfull.2650373813_h7ga.jpg"
            alt="AnimeVui Logo"
            className="navbar-logo-img"
          />
          <h2 className="navbar-logo-text">Recommend <span>Anime</span></h2>
        </Link>
      </div>

      {/* LINKS */}
      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/recommend">Recommend</Link>

        {user ? (
          <>
            <Link to="/profile" className="user-link">
              👋 {user.full_name || user.email}
            </Link>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
