import React, { Component } from "react";
import ReferralsPage from "./Components/ReferralsPage";
import Dashboard from "./Components/Dashboard";
import { 
    BrowserRouter as Router, 
    Switch, 
    Route, 
    Link, 
    Navigate, 
} from "react-router-dom"; // Redirect was replaced by Navigate.

export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <p>This is hopefully the homepage</p>; // I should use the router here, but I'm not getting this paragraph as intended yet.
    }
}