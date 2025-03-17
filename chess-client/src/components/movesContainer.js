import './css/movesContainer.css';

export function MovesContainer ({moves=[], pieces=[]}) {

    // const moves = [{move: 'e4', time: '2:41'}];
    // const taken_pieces =[{queen: 2}, {rook: 1}, {bishop: 1}, {knight: 1}, {pawn: 6}];
    const pieceImages = {
            pawn: "pieces/pawn.png",
            knight: "pieces/knight.png",
            bishop: "pieces/bishop.png",
            rook: "pieces/rook.png",
            queen: "pieces/queen.png",
            king: "pieces/king.png",
            };

    const mergedPieces = pieces.reduce((acc, piece) => {
            const key = Object.keys(piece)[0]; // Get the piece name
            acc[key] = piece[key]; // Assign the count
            return acc;
            }, {});

    return(
        <div className="moves-container">
        <div className='moves-taken-pieces'>
            {
                Object.entries(mergedPieces).map(([key, count], index) => (
                    [...Array(count)].map((_, index) => (
                                <img 
                    className="moves-taken-piece-img"
                    src={pieceImages[key]}
                    />
                    ))
                ))
            }
        </div>
        <div className="moves-scroll">
            <ol>
            {
                moves.map((move, _) => (
                    <li className='moves-list-item'>
                        <span className='moves-text'>{move.move}</span>
                        <span className='moves-time'>{move.time}</span>
                    </li>
                ))
            }
            </ol>
        </div>
    </div>
    );
}