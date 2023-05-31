import React, { useState } from "react"
import axios from "axios"
import { useNavigate, Link } from "react-router-dom"

const LoginForm = (props) => {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });
    const navigate = useNavigate();
    const [error, setError] = useState("");

    

    const updateFormData = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!formData.username) {
            alert("Please add a username");
            return;
        }
        if (!formData.password) {
            alert("Please add a password");
            return;
        }

        const url = "http://localhost:8000/api/login/"

        console.log(`Attempting to post: ${url}`);

        axios
            .post(url, formData)
            .then((response) => {
                console.log(response.data)
                if (response.status >= 200 && response.status < 300) {
                    localStorage.setItem("token", response.data.token);
                    props.onLogin();
                    navigate("/profile/")
                }
            })
            .catch((error) => {
                if (error.response) {
                    console.log('Error status:', error.response.status);
                    console.log('Error details:', error.response.data);
                    setError("Login failed");
                } else if (error.request) {
                    console.log('No response was received', error.request);
                    setError("Login failed - no response from server");
                } else {
                    console.log('Something happened setting up the request', error.message);
                    setError("Login failed - something happened with the request");
                }
            });
    };



  return (
    <form className="container" onSubmit={handleSubmit}>
        <div className="form-control">
            <label>
                Username:
                <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={updateFormData}
                />
            </label>
        </div>
        <div className="form-control">
            <label>
                Password:
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={updateFormData}
                />
            </label>
        </div>
        {error && <p>{error}</p>}
        <input type="submit" value="Login" className="btn btn-block"/>
        <p> Don't have an account? <Link to="/register">Register</Link> </p>
    </form>

  );
};

export default LoginForm