import React from 'react'
import { Link } from 'react-router-dom'


const Navbar = () => {
    return (
      <nav style={{ textAlign: "center", marginTop: "20px" }}>
        <Link to="/" style={{ padding: "10px" }}>
          Home
        </Link>
        <Link to="/Login" style={{ padding: "10px" }}>
          Login
        </Link>
        <Link to="/register" style={{ padding: "10px" }}>
          Register
        </Link>
      </nav>
    );
  };
  export default Navbar;