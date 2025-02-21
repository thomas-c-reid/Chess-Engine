import './css/playerCard.css'

export function PlayerCard({playerData, className=""}) {

    const isRight = className.includes('right');


    return (
        <div className={`player-card ${className}`}>
            {
                isRight ? (
                    <>
                        <div className="player-card-info-area">
                            <label className="player-card-info-nametag">{playerData['name']}</label>
                            <label>{playerData['description']}</label>
                            {/* <button className="player-card-info-button">show more</button> */}
                        </div>

                        <div className='player-card-icon-area'>
                            <div className="player-card-icon"></div>
                        </div>
                    </>
                ) : (
                    <>
                        <div className='player-card-icon-area'>
                            <div className="player-card-icon"></div>
                        </div>

                        <div className="player-card-info-area">
                            <label className="player-card-info-nametag">{playerData['name']}</label>
                            <label>{playerData['description']}</label>
                            {/* <button className="player-card-info-button">show more</button> */}
                        </div>
                    </>
                )
            }
        </div>
    );
}