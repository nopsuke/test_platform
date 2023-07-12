import React, { useState, useEffect } from 'react'
import axios from 'axios'
import "../Design/ProfileDashboard.css"

const ProfileDashboard = () => {
  const [profileData, setProfileData] = useState(null);

  useEffect(() => {
    // Make an API request to retrieve the user profile data
    const fetchProfileData = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:8000/api/profile_dashboard/", {
          headers: {
            "Authorization": "Token " + token,
          },
        }); 
        setProfileData(response.data); 
      } catch (error) {
        console.log('Error retrieving profile data:', error);
      }
    };

    fetchProfileData();
  }, []);

  return (
    <div className="profile-dashboard">
      {profileData ? (
        <>
          <h2>Your Profile</h2>
          <p>Balance: {(parseFloat(profileData.balance)).toFixed(2)}</p>
          {profileData.bestTrade && 
            <div>
              <p>Best Trade Symbol: {profileData.bestTrade.symbol}</p>
              <p>Best Trade Profit or Loss: {(parseFloat(profileData.bestTrade.profit_or_loss)).toFixed(2)}</p>
            </div>
          }
          {profileData.worstTrade &&
            <div>
              <p>Worst Trade Symbol: {profileData.worstTrade.symbol}</p>
              <p>Worst Trade Profit or Loss: {(parseFloat(profileData.worstTrade.profit_or_loss)).toFixed(2)}</p>
            </div>
          }
        </>
       ) : (
        <p>Loading profile data...</p>
      )}
    </div>
  );
};

export default ProfileDashboard