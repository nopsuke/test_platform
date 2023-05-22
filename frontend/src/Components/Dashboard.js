// Dashboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
    const [userProfile, setUserProfile] = useState(null);
    const [tradeSize, setTradeSize] = useState('');
    const [price, setPrice] = useState('');
    const [stopLoss, setStopLoss] = useState('');
    const [marginUsed, setMarginUsed] = useState(0);

    useEffect(() => {
        // Fetch user profile data when component mounts
        axios.get('/api/user_profile/')
            .then(response => setUserProfile(response.data))
            .catch(error => console.error('Error:', error));
    }, []);

    const handleBuyOrder = () => {
        axios.post('/api/buy_order/', {trade_size: tradeSize, price: price, stop_loss: stopLoss})
            .then(response => setMarginUsed(response.data.margin_used))
            .catch(error => console.error('Error:', error));
    };

    return (
        // I dont understand this very well. Need to look into it.
    );
}