import React, { useEffect, useRef } from 'react'
import { Chart } from './ChartComponent'
import BuyOrder from './BuyOrder'
import SellOrder from './SellOrder'
import { Link } from 'react-router-dom'


// This will hold the main "TradeBoard" page/tab. Will hold "TradeChart", "TradeHistory", "BuySellForm", and some other components which are tbd.
// Will require authentication to view.

const TradeBoard = () => {
  const data = [
    { time: '2018-12-22', value: 32.51 },
    { time: '2018-12-23', value: 31.11 },
    { time: '2018-12-24', value: 27.02 },
    { time: '2018-12-25', value: 27.32 },
    { time: '2018-12-26', value: 27.32 },
  ]

  
  return (
    <div>
    
    <nav style={{ textAlign: "center", marginTop: "20px" }}>
        <Link to="/profile" style={{ padding: "10px" }}>
          Profile
        </Link>
        <Link to="/tradeboard" style={{ padding: "10px" }}>
          Tradeboard
        </Link>
      </nav>
      <h1 style={{ textAlign: "center", color: "purple" }}>TradeBoard</h1>

    <Chart data={data}/>

    <BuyOrder /><SellOrder />
    

    </div>
 
    

  )


}

export default TradeBoard