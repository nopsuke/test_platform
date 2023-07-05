import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import "../Design/Navbar.css"


const Navbar = () => {





  return (
    <nav className="navbar">
      <div className="navbar-links">
        <Link to="/" className="navbar-link">
          Home
        </Link>
        <Link to="/login" className="navbar-link">
          Login
        </Link>
        <Link to="/register" className="navbar-link">
          Register
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;