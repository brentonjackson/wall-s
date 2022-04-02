import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div className="navbar">
      <Link to="/">
        <img src="images/robotech.png" alt="logo" className="navbar-logo" />
      </Link>
    </div>
  );
};

export default Navbar;
