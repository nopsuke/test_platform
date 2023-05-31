import React from 'react'
import LogoutButton from './LogoutButton'
import ProfileDashboard from './ProfileDashboard'
import { Link } from 'react-router-dom'

// This will hold the main "Profile" page/tab. Will hold "ProfileDashboard" and some other components which are tbd.


const Profile = () => {
  return (
    <div>
      
      <nav style={{ textAlign: "center", marginTop: "20px" }}>
        <Link to="/profile" style={{ padding: "10px" }}>
          Profile
        </Link>
        <Link to="/Tradeboard" style={{ padding: "10px" }}>
          Tradeboard
        </Link>
      </nav>
      <p>Welcome to your dashboard, Evert!</p>

      <ProfileDashboard />
      <LogoutButton />
    </div>

    
  )
}

export default Profile