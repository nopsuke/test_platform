import { useState, useEffect } from "react";
import HomePage from "./Components/HomePage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; // The Router lives at the root of the project so that all components that you create can be accessed
import RegisterForm from "./Components/RegisterForm";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <div>This is David teaching and Evert trying to learn</div>

        <RegisterForm />

      </div>
    </Router>
  );
}

export default App;


// This router structure is a bit confusing. Throwing random errors about not being able to use as a child of another component. 