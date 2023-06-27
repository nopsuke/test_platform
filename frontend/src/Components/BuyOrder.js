import React from 'react'
import axios from 'axios'
import { useState } from 'react'

// E - I don't know if the BuyOrder and SellOrder should be separate components or if they should be combined into one component. Thoughts?

// Need to take the user profile that is logged in (where can I access that?) and send it with the formdata, I think?
const BuyOrder = () => {
  const [formData, setFormData] = useState({
    symbol: "",
    quantity: "",
    price: "",
    size: "",
    stoploss: "",
  });

  const token = localStorage.getItem("token");

  const updateFormData = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.price) {
      alert("Please add a price");
      return;
    }
    if (!formData.quantity) {
      alert("Please enter a trade size");
      return;
    }

    const url = "http://localhost:8000/api/market_buy/" // Wrong API endpoint currently.
    console.log(`Attempting to post: ${url}`);
    axios({
      method: "post",
      url: url,
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Token " + token,
      },
      data: formData,
    
    })

      .then((response) => {
        console.log(response.data)
        if (response.status >= 200 && response.status < 300) {
          alert("Order placed successfully")
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

  return (
    <form>
      <div className="buyorder">

        <label>
          Symbol
          <input
            type="text"
            name="symbol"
            value={formData.symbol}
            onChange={updateFormData}
          />
        </label>

        <label>
          Size
          <input
            type="text"
            name="quantity"
            value={formData.quantity}
            onChange={updateFormData}
          />
        </label>

        <label>
          Price
          <input
            type="text"
            name="price"
            value={formData.price}
            onChange={updateFormData}
          />
        </label>
    
      
      
        <label>
          Stop Loss
          <input
            type="text"
            name="stoploss"
            value={formData.stoploss}
            onChange={updateFormData}
          />
        </label>
        <button type="submit" onClick={handleSubmit}>
          Submit Order
        </button>
      </div>
    </form>
  )
}

export default BuyOrder