import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

/*
    D - This code is definitely working and functional!

    1. You never set the value of the "inputs." For inputs and other stateful changes it's best to double bind the state (set it and read it). I'm changing the "username" input to reflect this. This also removes the need for a handle change callback, since it's all handled in state anyways. If you prefer the full form data obj then you should have a helper function like updateFormData
    2. I renamed "handleChange" to "updateFormData" for the sake of readability. Good practice to always name things in a more descriptive way
    3. Just for the sake of teaching you about destructuring, I destructured "e.target" in "updateFormData"
    4. What's the "form-control" class? That needs a much better name. Wrap the whole form area in a class called "formCont" and you can style easily from there

    Important note - you should be using a library to handle authentication. I'm pretty sure react-router has some of that functionality, but there are other great resources for this.
    

    E - Awesome man!

    1. Yes, like we discussed I'm still a little confused about the inputs and the state. I'll keep working on it and hopefully make it "click" soon.
    2. I like the name updateFormData. I'll use that from now on. 
    3. Funnily enough, I didn't destructure in my practise site because I thought just using generic "e" was easier to read. I'll try to use destructuring more often.
    4. I'll change the class name to formCont once I get some style ideas. It's just a generic class name I found on a tutorial :D.

    This works as intended.


*/

const RegisterForm = () => {
  const [authenticated, setAuthenticated] = useState(localStorage.getItem("token") ? true : false);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  // const [username, setUsername] = useState(""); E - I had to remove this. I couldn't figure out the double binding and I am desperate to try and register a user :D.
  const navigate = useNavigate();

  const updateFormData = (e) => {
    //destructuring
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
    if (!formData.email) {
        alert("Please add an email");
        return;
    }


    //D - Use error handling. On a very basic level check if username === ""
    // you did that in the other file
// axios wont work, need to implement a token system otherwise it'll send a 403 error. E - solved with django-cors-headers.
    const url = "http://localhost:8000/api/register/"

    console.log(`Attempting to post: ${url}`);
    
    axios
      .post(url, formData)
      .then((response) => {
        console.log(response.data)
        if (response.status >= 200 && response.status < 300) { 
          localStorage.setItem("token", response.data.token) 
          setAuthenticated(true)
          navigate("/profile/");
        }
      })
      .catch((error) => { // I added a bunch of error logging because I couldn't figure out what was going wrong. Is it good practise to keep this in? I'll add more error handling later.
        if (error.response) {
          console.log('Error status:', error.response.status);
          console.log('Error details:', error.response.data);
        } else if (error.request) {
            console.log('No response was received', error.request);
        } else {
            console.log('Something happened setting up the request', error.message);
        }

      });
  };
// I don't think the token is being received. Will need to look into that. Works

  return (
    <form className="container" onSubmit={handleSubmit}>
      <div className="form-control">
        <label>
          Username:
          <input
            type="text"
            name="username"
            value={formData.username} 
            onChange={updateFormData} /* E - I did some googling and I'm even more confused. We seem to want username as a controlled component but I don't know why. */
          />
        </label>
      </div>
      <div className="form-control">
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={updateFormData} /*E - am I wrong or should this work? */
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
           onChange={updateFormData} /*E - am I wrong or should this work? */
        />
        </label>
      </div>
      <input type="submit" value="Register" className="btn btn-block" />
    </form>
  );
};

export default RegisterForm;
