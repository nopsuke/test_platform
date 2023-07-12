import React, { useState, useEffect } from 'react'
import ProfileDashboard from './ProfileDashboard'
import TradeBoard from './TradeBoard'
import { Link } from 'react-router-dom'
import '../Design/Profile.css'

// This will hold the main "Profile" page/tab. Will hold "ProfileDashboard" and some other components which are tbd.


const Profile = () => {


  return (
    <div className="profile-container">
      <div className="profile-sidebar">
        
        <nav style={{ textAlign: "center", marginTop: "20px" }}>
          <Link to="/profile" style={{ padding: "10px" }}>
            Profile
          </Link>
          <Link to="/tradeboard" style={{ padding: "10px" }}>
            Tradeboard
          </Link>
          <Link to ="/Guessing" style={{ padding: "10px" }}>
            Guessing
          </Link>
          <Link to ="" style={{ padding: "10px" }}>
            Subscribe
          </Link>
          <Link to ="/logout" style={{ padding: "10px" }}>
            Logout
          </Link>
        </nav>
      </div>
      <div className="profile-dashboard">
        <ProfileDashboard />
      </div>
      
    </div>
    
    

    
  )
}

export default Profile