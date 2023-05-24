import React, { useState } from 'react';
import { on } from 'ws';
// Moved from /frontend/ 
// Register2 is better.


// I need to add validation to the form and error handling, not sure how to do that yet. Also password needs to be hashed and salted but this should be done on the backend.
// The form should also POST to the backend and create a new user in the database. I'll try and figure that out.
// Under accounts/views.py there is a register view that should be able to handle the POST request from the form.

const RegisterForm = ({ onAdd }) => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [email, setEmail] = useState("")
    const onSubmit = (e) => {
        e.preventDefault()

        if(!username) {
            alert('Please add a username')
            return
        }
        if(!password) {
            alert('Please add a password')
            return
        }
        if(!email) {
            alert('Please add an email')
            return
        }
        onAdd({ username, password, email })

        setUsername("")
        setPassword("")
        setEmail("")
    }
// E - Need to hide the password, MUI maybe for style?
// E - I don't know how to do the POST request to the backend and handle the response. I think I need to use axios but I'm not sure.

    return(
        <form className='add-form' onSubmit={onSubmit}>
            <div className='form-control'>
                <label>Username</label>
                <input type='text' placeholder='Create a Username' value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
            <div className="form-control">
            <label>Password</label>
            <input type="text" 
            placeholder="Set a password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}/>
        </div>
        <div className="form-control">
            <label>Email</label>
            <input type="text"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}/>
        </div>

        <input type="submit" value="Create account" className="btn btn-block"/>
    </form>

  )
}

export default RegisterForm







