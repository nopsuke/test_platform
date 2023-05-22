import React from 'react';
import ReactDOM from 'react-dom/client';
import HomePage from "./Components/HomePage";


/* The start is the component and the render is the method that renders the component to the DOM. The render func should render this component in the app div in the site. 
To be confirmed.*/
export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <p>This is Evert trying</p>;
    }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);

// A prop (property) is an argument for a component. It is passed to the component as an attribute. 


//<div>
//<HomePage />; 
//</div>