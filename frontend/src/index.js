import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
      <App />
  </React.StrictMode>
);

// Gonna write this here but essentially, components can render other components. React seems to just nest components inside eachother and then render them to the DOM.
// I'm guessing the render method is what renders the component to the DOM. The render method is a method of the ReactDOM object.
// Think about it like this.. components are just pieces of a website that display something. DOM is the "completed" website that is displayed to the user.
// Which component is displayed where is controlled by the render method/ReactDOM. How it is displayed is controlled by the CSS.

// Removed BrowserRouter from here. It was causing an error. I think it's because I already have it in App.js
