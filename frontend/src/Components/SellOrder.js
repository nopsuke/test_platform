import React from 'react'
import axios from 'axios'
import { useState } from 'react'

// E - I don't know if the BuyOrder and SellOrder should be separate components or if they should be combined into one component. Thoughts?


const SellOrder = () => {
  const [formData, setFormData] = useState({
    price: "",
    size: "",
    stoploss: "",
  });

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
    if (!formData.size) {
      alert("Please enter a trade size");
      return;
    }

    const url = "http://localhost:8000/api/buyorder/" // Wrong API endpoint currently.
    console.log(`Attempting to post: ${url}`);
    axios
      .post(url, formData)
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
      <div className="sellorder">
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
          Size
          <input
            type="text"
            name="size"
            value={formData.size}
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

export default SellOrder

