// import './takenPieces.css';

// function TakenPieces({ takenPieces }) {
//   const pieceImages = {
//     p: '/pawn.png',
//     k: '/knight.png',
//     b: '/bishop.png',
//     r: '/rook.png',
//     q: '/queen.png',
//   };

//   return (
//     <div className="taken-pieces-container">
//       {/* Render the images */}
//       {takenPieces.map((item, index) => (
//         <div key={`piece-${index}`}>
//           <img
//             src={pieceImages[item.piece.toLowerCase()]}
//             alt={item.piece}
//             className="taken-piece-image"
//           />
//         </div>
//       ))}
//       {/* Render the counts */}
//       {takenPieces.map((item, index) => (
//         <div key={`count-${index}`} className="taken-piece-count">
//           {item.count}
//         </div>
//       ))}
//     </div>
//   );
// }

// export default TakenPieces;


import './takenPieces.css';

function TakenPieces({ takenPieces }) {
  const pieceImages = {
    p: '/pawn.png',
    k: '/knight.png',
    b: '/bishop.png',
    r: '/rook.png',
    q: '/queen.png',
  };

  return (
    <div className="taken-pieces-container">
      {takenPieces.map((item, index) => (
        <div key={`wrapper-${index}`} className="taken-piece-wrapper">
          <img
            src={pieceImages[item.piece.toLowerCase()]}
            alt={item.piece}
            className="taken-piece-image"
          />
          <div className="taken-piece-count">{item.count}</div>
        </div>
      ))}
    </div>
  );
}

export default TakenPieces;
