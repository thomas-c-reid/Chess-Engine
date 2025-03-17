import React, { useState } from 'react';
import Menu from './menu'; 
import Footer from './footer';
import './css/navbar.css';

// This component will be the 

const Navbar = ({setIsFullScreen}) => {

    return (
      <div className ="navbar"
      onMouseEnter={() => setIsFullScreen(false)}>
        
        <div className='menu-switcher'>
          <select className='dropdown-menu'
          id='menu-choice'
          value={'CHESS ARENA'}>
            <option value="Chess Arena">Chess Arena</option>
          </select>
        </div>

        <Menu className='menu'></Menu>
        <Footer className='footer' setIsFullScreen={setIsFullScreen}></Footer>
      </div>
    );
};

export default Navbar;