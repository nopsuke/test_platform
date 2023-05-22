// Dashboard that I used earlier in "accounts", need to figure out what to do with it. Not sure why its expecting TS?

import React, { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [userProfile, setUserProfile] = useState(null);
  const [tradeSize, setTradeSize] = useState("");
  const [price, setPrice] = useState("");
  const [stopLoss, setStopLoss] = useState("");
  const [marginUsed, setMarginUsed] = useState(0);

  useEffect(() => {
    // Fetch user profile data when component mounts
    axios
      .get("/api/user_profile/")
      .then((response) => setUserProfile(response.data))
      .catch((error) => console.error("Error:", error));
  }, []); //the empty array here is the

  const handleBuyOrder = () => {
    // D - currently you do not set the tradeSize, price, or stopLoss. I assume these come from an API?
    axios
      .post("/api/buy_order/", {
        trade_size: tradeSize,
        price: price,
        stop_loss: stopLoss,
      })
      .then((response) => setMarginUsed(response.data.margin_used))
      .catch((error) => console.error("Error:", error));
  };

  return (
    // I dont understand this very well. Need to look into it.
    // D - this is the "HTML" that gets added to the page. We get the information we need from the APIs above and then use it here
    <div>{userProfile.name}</div>
  );
};

export default Dashboard;
