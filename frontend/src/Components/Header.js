import React from 'react'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'

const Header = ({ title }) => {

    return (
        <header className="header">
            <h1>{title}</h1>
        </header>

            
    )
}

Header.defaultProps = { // If I don't provide a title when displaying the component, this will be the default title
    title: 'Welcome to XYZ!',
  }


export default Header