import { useState, useEffect } from "react";
import HomePage from "./Components/HomePage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; // The Router lives at the root of the project so that all components that you create can be accessed
import RegisterForm from "./Components/RegisterForm";
import Header from "./Components/Header";

const App = () => {
  const [user, setUser] = useState() // E - I want to use this to store the user data upon successfully logging in. I'm not sure if this is the correct approach though.


// E - I think I should be using useEffect to fetch the user related data from the API and then use useState to set the state of the data. I don't know what the logical approach is here.
  useEffect(() => {
    
   
  });


// E - This would fetch the current balance. This should be a constantly evolving number though, so I'm not sure if this is the right approach. 
// E - Also should be able to fetch the balance for a specific user so I'm thinking I need to pass in the user ID as a parameter? Could also create a component for this.
  const fetchBalance = () => {
    const res = fetch("/accounts/api/balance/") // This api link is probably broken. Need to go over and fix things.
    const data = res.json()

    return data
  }

// E - This would fetch the current open positions. But same issue as fetchBalance, this number will be in constant flux potentially so it needs to be updated constantly.
// E - I'm thinking ID as the parameter here as well. Is this even the correct place to to add this function? It's needed in several places or should I create a component for it?
  const fetchOpenPositions = () => {
    const res = fetch("/accounts/api/open_positions/")
    const data = res.json()

    return data
  }

// E - This would register a new user, I hope. Would need to verify the content type etc as well. The return should have a status code of 201 if it works, 400 if it doesn't but I'm not sure
// what part of the app would handle that and how to set it up.
  const registerUser = async (username, password, email) => {
    const res = await fetch("/accounts/api/register/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ username, password, email }),
    })

    const data = await res.json()

    return data // E - I want to provide some kind of feedback to the user if the registration was successful or not. But I'm not sure if Django will handle that through its user.authentication 

  }



  return (
    

    <Router>
      <div className="container">
        <Header title="This is David teaching and Evert trying to learn" />
        

        <RegisterForm />
        

      </div>
    </Router>
  );
}

export default App;


//E - This router structure is a bit confusing. Throwing random errors about not being able to use as a child of another component but I'm sure I'll make do.