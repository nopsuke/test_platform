import React from 'react'
import { useState } from 'react'
import axios from 'axios'

const CloseOrder = () => {
    const [formData, setFormData] = useState({
        id: "",
    });

    const updateFormData = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
      };

    const handleSubmit = (e) => {
      e.preventDefault();
      if (!formData.id) {
        alert("Please add an order id");
        return;
      }


    const token = localStorage.getItem("token");
    const url = "http://localhost:8000/api/close_positions/"

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
            alert("Orders closed successfully")
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
          trade_id:
          <input
            type="text"
            name="id"
            value={formData.id}
            onChange={updateFormData}
          />
        </label>

        <button type="submit" onClick={handleSubmit}>
          Close order
        </button>
      </div>
    </form>
  )
}

export default CloseOrder