import React from 'react'
import axios from 'axios'
import { useState, useEffect } from 'react'

// E - I don't know if the BuyOrder and SellOrder should be separate components or if they should be combined into one component. Thoughts?


const SellOrder = ( {tradingProfiles} ) => {
  const [formData, setFormData] = useState({
    profile_id: "",
    symbol: "",
    quantity: "",
    stop_loss: "",
    direction: "LONG",
  });

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (tradingProfiles.length > 0) {
      setFormData((prevFormData) => ({
        ...prevFormData,
        profile_id: tradingProfiles[0].id,
      }));
    }
  }, [tradingProfiles]);

  const updateFormData = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };
  console.log(formData)

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.quantity) {
      alert("Please enter a trade size");
      return;
    }
    console.log(formData);
    console.log({
      profile_id: formData.profile_id, 
      symbol: formData.symbol,
      quantity: formData.quantity,
      stop_loss: formData.stop_loss ? formData.stop_loss : null,
      direction: formData.direction,
    });


    const url = "http://localhost:8000/api/market_buy/" 
    console.log(`Attempting to post: ${url}`);
    axios({
      method: "post",
      url: url,
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Token " + token,
      },
      data: {
        profile_id: formData.profile_id, 
        symbol: formData.symbol,
        quantity: formData.quantity,
        stop_loss: formData.stop_loss ? formData.stop_loss : null,
        direction: formData.direction,
      },
    })
    .then((response) => {
        console.log(response.data)
        if (response.status >= 200 && response.status < 300) {
          alert("Order placed successfully")
          setFormData({
            profile_id: formData.profile_id, // keep the currently selected profile
            symbol: "",
            quantity: "",
            stop_loss: "",
            direction: "SHORT",
          });
        }
      })
      .catch((error) => {
        if (error.response) {
          console.log('Error status:', error.response.status);
          console.log('Error details:', error.response.data);
        } else if (error.request) {
          console.log('No response was received', error.request);
        } else {
          console.log('An error occurred', error.message);
        }
      });
  };

  const sellOrderStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    backgroundColor: 'red',
    padding: '20px',
    borderRadius: '5px',
  };

  const labelStyle = {
    marginBottom: '10px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    width: '100%',
    color: 'white',
    fontSize: '14px',
    fontWeight: 'bold',
  };

  const inputStyle = {
    marginBottom: '10px',
    padding: '5px',
    width: '100%',
  };

  const buttonStyle = {
    padding: '10px',
    backgroundColor: 'white',
    color: 'black',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  };
  return (
    <form onSubmit={handleSubmit}>

      <div style={sellOrderStyle}>
        <label style={labelStyle}>
          Profile
          <select name="profile_id" value={formData.profile_id} onChange={updateFormData} style={inputStyle}>
            {tradingProfiles.map((profile) => 
              <option key={profile.id} value={profile.id}>{profile.name}</option>
            )}
          </select>
        </label>
      
        <label style={labelStyle}>
          Symbol
          <input 
            type="text"
            name="symbol"
            value={formData.symbol}
            onChange={updateFormData}
            style={inputStyle}
          />
        </label>
      
      
        <label style={labelStyle}>
          Size
          <input
            type="text"
            name="quantity"
            value={formData.quantity}
            onChange={updateFormData}
            style={inputStyle}
          />
        </label>
      
      
        <label style={labelStyle}>
          Stop Loss
          <input
            type="text"
            name="stop_loss"
            value={formData.stop_loss}
            onChange={updateFormData}
            style={inputStyle}
          />
        </label>
        <button type="submit" onClick={handleSubmit} style={buttonStyle}>
          Submit Order
        </button>
      </div>
    </form>
  )
}

export default SellOrder

