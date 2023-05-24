import React, { useState } from "react";
import axios from "axios";

/*
    D - This code is definitely working and functional!

    1. You never set the value of the "inputs." For inputs and other stateful changes it's best to double bind the state (set it and read it). I'm changing the "username" input to reflect this. This also removes the need for a handle change callback, since it's all handled in state anyways. If you prefer the full form data obj then you should have a helper function like updateFormData
    2. I renamed "handleChange" to "updateFormData" for the sake of readability. Good practice to always name things in a more descriptive way
    3. Just for the sake of teaching you about destructuring, I destructured "e.target" in "updateFormData"
    4. What's the "form-control" class? That needs a much better name. Wrap the whole form area in a class called "formCont" and you can style easily from there

    Important note - you should be using a library to handle authentication. I'm pretty sure react-router has some of that functionality, but there are other great resources for this.
    
*/

const Register2 = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [username, setUsername] = useState("");

  const updateFormData = (e) => {
    //destructuring
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    //D - Use error handling. On a very basic level check if username === ""
    // you did that in the other file

    axios
      .post("/api/register/", formData)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
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
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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
            onChange={updateFormData}
          />
        </label>
      </div>
      <div className="form-control">
        <label>
          Password:
          <input type="password" name="password" onChange={updateFormData} />
        </label>
      </div>
      <input type="submit" value="Register" className="btn btn-block" />
    </form>
  );
};

export default Register2;
