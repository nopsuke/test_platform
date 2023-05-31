import React, { useEffect, useRef } from 'react'
import { Chart } from './ChartComponent'

// This will hold the main "TradeBoard" page/tab. Will hold "TradeChart", "TradeHistory", "BuySellForm", and some other components which are tbd.
// Will require authentication to view.

const TradeBoard = () => {
  const data = [
    { time: '2018-12-22', value: 32.51 },
    { time: '2018-12-23', value: 31.11 },
    { time: '2018-12-24', value: 27.02 },
    { time: '2018-12-25', value: 27.32 },
  ]

  
  return (
    <div>This isn't supposed to be here...
    <Chart data={data}/>
    </div>

  )


}

export default TradeBoard