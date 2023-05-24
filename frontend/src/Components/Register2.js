import React, { useState } from 'react';
import axios from "axios";


const Register2 = () => {
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
    });

    const handleChange = (e) => {
        setFormData({...formData, [e.target.name]: e.target.value});
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('/api/register/', formData)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }
  
  
  
    return (
        <form className="container" onSubmit={handleSubmit}>
        <div className="form-control">   
        <label>
            Username:
            <input type="text" name="username" onChange={handleChange} />
        </label>
        </div>
        <div className="form-control">  
        <label>
            Email:
            <input type="email" name="email" onChange={handleChange} />
        </label>
        </div>
        <div className="form-control">
        <label>
            Password:
            <input type="password" name="password" onChange={handleChange} />
        </label>
        </div>
        <input type="submit" value="Register" className="btn btn-block"/>
    </form>
    
  )
}

export default Register2