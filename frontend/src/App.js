import { useState, useEffect } from "react";
import HomePage from "./Components/HomePage";
import { 
  Router,
  Routes, 
  Route,
  useNavigate,
  Link } from "react-router-dom"; // The Router lives at the root of the project so that all components that you create can be accessed
import RegisterForm from "./Components/RegisterForm";
import Header from "./Components/Header";
import LoginForm from "./Components/LoginForm";
import Profile from "./Components/Profile";
import Navbar from "./Components/Navbar";
import TradeBoard from "./Components/TradeBoard";
import PrivateRoute from "./Components/PrivateRoute";
import LogoutButton from "./Components/LogoutButton";
import Guessing from "./Components/Guessing";

const App = () => {
  const [user, setUser] = useState() // E - I want to use this to store the user data upon successfully logging in. I'm not sure if this is the correct approach though.
  const [authenticated, setAuthenticated] = useState(localStorage.getItem("token") ? true : false);


// E - I think I should be using useEffect to fetch the user related data from the API and then use useState to set the state of the data. I don't know what the logical approach is here.
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setAuthenticated(true);
    }
  }, []);
    
   



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

    return data 

  }



  return (
    
    <div>
      <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginForm onLogin={() => setAuthenticated(true)} />} />
          <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
          <Route path="/register" element={<RegisterForm onRegister={registerUser} />} />
          <Route path="/tradeboard" element={<PrivateRoute><TradeBoard /></PrivateRoute>}  />
          <Route path="/logout" element={<PrivateRoute><LogoutButton /></PrivateRoute>} />
          <Route path="/Guessing" element={<PrivateRoute><Guessing /></PrivateRoute>} />
        </Routes>
        

    </div>
  );
}

export default App;

