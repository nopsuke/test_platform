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
        <Link to="/tradeboard" style={{ padding: "10px" }}>
          Tradeboard
        </Link>
        <Link to ="" style={{ padding: "10px" }}>
          Leadboard
        </Link>
        <Link to ="" style={{ padding: "10px" }}>
          Subscribe
        </Link>
        <Link to ="" style={{ padding: "10px" }}>
          Logout
        </Link>
      </nav>
      <p>Profile</p>

      <ProfileDashboard />
      <LogoutButton />
    </div>
    
    

    
  )
}

export default Profile