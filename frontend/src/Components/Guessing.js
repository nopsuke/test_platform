import React, { useState } from 'react'
import axios from 'axios'

const Guessing = () => {

    const [guess, setGuess] = useState('');

    const token = localStorage.getItem("token");

    
    const url = "http://localhost:8000/api/game/"
    const handleGuess = async (direction) => {
      try {
        console.log(`Attempting to post: ${url}`);
        const response = await axios({
            method: "post",
            url: url,
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Token " + token,
            },
            data: {
                guess: direction,
            },
          })
        console.log(response.data);
        
      } catch (error) {
        console.error('Error:', error);
      }
    };
    return (
        <div>
          <h1>Up or Down Game</h1>
          <button onClick={() => handleGuess("bulls")}>UP</button>
          <button onClick={() => handleGuess("bears")}>DOWN</button>
        </div>
      );
    };
    

export default Guessing