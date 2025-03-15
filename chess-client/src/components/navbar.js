import React, { useState } from 'react';
import Menu from './menu'; 
import Footer from './footer';
import './css/navbar.css';

// This component will be the 

const Navbar = ({setConnectionState, setPlayerTurn, setIsFullScreen}) => {

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

        <Menu className='menu' setPlayerTurn={setPlayerTurn} setConnectionState={setConnectionState}></Menu>
        <Footer className='footer' setIsFullScreen={setIsFullScreen}></Footer>
      </div>
    );
};

export default Navbar;