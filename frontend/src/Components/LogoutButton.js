import React from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const LogoutButton = () => {
  const navigate = useNavigate();
  
  const logout = () => {
    const token = localStorage.getItem('token');
    

    axios({
      method: 'post',
      url: 'http://localhost:8000/api/logout/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token,
      },
    })
    .then((response) => {
      if(response.status === 200) {
        console.log('Logout successful');
        localStorage.removeItem('token');
        navigate("/");
      }
    })
    .catch((error) => {
      console.log('Logout failed:', error.response.data, 'Status:', error.response.status);
    });
  }

  return (
    <button onClick={logout}>
      Logout
    </button>
  );
}

export default LogoutButton;

