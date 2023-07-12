import React, { useEffect, useState } from 'react'
import { Chart } from './ChartComponent'
import BuyOrder from './BuyOrder'
import SellOrder from './SellOrder'
import CloseOrder from './CloseOrder'
import { Link } from 'react-router-dom'
import '../Design/Tradeboard.css'
import axios from 'axios'


// This will hold the main "TradeBoard" page/tab. Will hold "TradeChart", "TradeHistory", "BuySellForm", and some other components which are tbd.
// Will require authentication to view.
// Data function to receive data from backend and pass to "TradeChart" component.

const TradeBoard = () => {
  const [tradingProfiles, setTradingProfiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTradingProfile = async () => {
      console.log('Fetching trading profile data...');
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:8000/api/trading_profile/", {
          headers: {
            "Authorization": "Token " + token,
          },
        });
        console.log('Response:', response);
        setTradingProfiles(response.data);
        console.log(tradingProfiles)
        setLoading(false);
      } catch (error) {
        console.log('Error retrieving profile data:', error);
      }
    };

    fetchTradingProfile();
  }, []);

  const data = [
    { time: '2018-12-22', value: 32.51 },
    { time: '2018-12-23', value: 31.11 },
    { time: '2018-12-24', value: 27.02 },
    { time: '2018-12-25', value: 27.32 },
    { time: '2018-12-26', value: 27.32 },
  ]

  
  return (
    <div className="container">
      <nav className="header">
        <Link to="/profile" className="btn">
          Profile
        </Link>
        <Link to="/tradeboard" className="btn">
          Tradeboard
        </Link>
      </nav>
      <h1 className="header">TradeBoard</h1>

      <div className="chart-container">
        <Chart data={data} />
      </div>

      <div className="order-container">
        <div className="order-item">
          <div className="buyorder">
            <BuyOrder tradingProfiles={tradingProfiles} />
          </div>
        </div>
        <div className="order-item">
          <div className="sellorder">
            <SellOrder tradingProfiles={tradingProfiles} />
          </div>
        </div>
        <div className="order-item">
          <div className="closeorder">
            <CloseOrder tradingProfiles={tradingProfiles} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradeBoard;