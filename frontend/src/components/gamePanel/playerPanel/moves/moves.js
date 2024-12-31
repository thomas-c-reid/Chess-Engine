import "./moves.css";
import React from 'react';

const Moves = ({ moves = []}) => {
    return (
        <div className="moves-container">
            <ul style={{ listStyleType: "none" }}>
                {moves.map((move, index) => (
                    <li key={index}>
                        {move}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Moves;
