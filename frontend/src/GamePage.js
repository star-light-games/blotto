import React from 'react';
import { useState, useEffect } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import TcgCard from './TcgCard';
import { URL } from './settings';

function GameInfo({ game, playerNum }) {
    const opponentNum = playerNum === 0 ? 1 : 0;
    const opponentUsername = game.usernames_by_player[opponentNum];
    const opponentHandSize = (game.game_state && game.game_state.hands_by_player) 
                             ? game.game_state.hands_by_player[opponentNum].length 
                             : 0;

    return (
        <div>
            <p>Your username: {game.usernames_by_player[playerNum]}</p>
            <p>Opponent's username: {opponentUsername}</p>
            <p>Opponent's hand size: {opponentHandSize}</p>
        </div>
    );
}

function CharacterDisplay({ character }) {
    return (
        <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            width: '200px', 
            height: '30px',
            border: '1px solid black',
            borderRadius: '5px',
            padding: '5px',
            marginBottom: '5px',
            backgroundColor: '#f5f5f5'
        }}>
            <span>{character.name}</span>
            <span>{character.attack}/{character.health}</span>
        </div>
    );
}

/*       <div 
style={{
    border: isSelected ? '2px solid black' : 'none',
    cursor: 'pointer'
}}
onClick={onCardClick ? () => onCardClick(card) : null}
onMouseEnter={e => e.currentTarget.style.border = '2px solid blue'}
onMouseLeave={e => e.currentTarget.style.border = isSelected ? '2px solid black' : 'none'}
> */

function Lane({ laneData, playerNum, opponentNum, selectedCard }) {    
    return (
      <div style={{ display: 'flex', 
                    flexDirection: 'column', 
                    alignItems: 'center', 
                    margin: '10px' }}>        
        <div 
            style={{ 
                outline: 'none',
                width: '100%',
                padding: '10px'
            }}
            onMouseEnter={e => {
                if (selectedCard) {
                    e.currentTarget.style.outline = '2px solid blue';
                }
            }}
            onMouseLeave={e => {
                e.currentTarget.style.outline = 'none';
            }}>
          <div>
            <h3>Lane {laneData.lane_number + 1}</h3> {/* +1 assuming lane_number starts from 0 */}

            <h4>Opponent's Damage: {laneData.damage_by_player[opponentNum]}</h4>
            {laneData.characters_by_player[opponentNum].map((character, index) => (
              <CharacterDisplay key={index} card={character} />
            ))}
          </div>
          <div>
            <h4>Your Damage: {laneData.damage_by_player[playerNum]}</h4>
            {laneData.characters_by_player[playerNum].map((character, index) => (
              <CharacterDisplay key={index} card={character} />
            ))}
          </div>
        </div>
      </div>
    );
}

function LanesDisplay({ lanes, playerNum, opponentNum, selectedCard }) {
    return (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
        {lanes.map((lane, index) => (
            <Lane key={index} laneData={lane} playerNum={playerNum} opponentNum={opponentNum} selectedCard={selectedCard} />
        ))}
        </div>
    );
}

function HandDisplay({ cards, selectedCard, setSelectedCard }) {
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '20px', flexWrap: 'wrap' }}>
            {cards.map((card, index) => (
                <div key={index} style={{ margin: '5px' }}>
                    <TcgCard card={card.template} isSelected={selectedCard ? selectedCard.id === card.id : false} onCardClick={() => setSelectedCard(card)} />
                </div>
            ))}
        </div>
    );
}

export default function GamePage({}) {
    const { gameId } = useParams();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const playerNum = queryParams.get('playerNum') === "0" ? 0 : 1;
    const opponentNum = playerNum === 0 ? 1 : 0;

    const [game, setGame] = useState({});
    const [loading, setLoading] = useState(true);

    const username = localStorage.getItem('username'); // Retrieving username from localStorage

    const [selectedCard, setSelectedCard] = useState(null);
    console.log(selectedCard);

    useEffect(() => {
        // Fetch the game data from your backend.
        fetch(`${URL}/api/games/${gameId}`)
            .then(res => res.json())
            .then(data => {
                setGame(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("There was an error fetching game data:", error);
            });
    }, [gameId]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!game.game_state) {
        return (
            <div>Waiting for another player to join...</div>
        )
    }

    // console.log(game);
    // console.log(game.game_state)
    console.log(game.game_state.hands_by_player[playerNum])

    return (
        <div>
            <GameInfo game={game} playerNum={playerNum} />
            <LanesDisplay lanes={game.game_state.lanes} playerNum={playerNum} opponentNum={opponentNum} selectedCard={selectedCard}/>
            <HandDisplay cards={game.game_state.hands_by_player[playerNum]} selectedCard={selectedCard} setSelectedCard={setSelectedCard} />
        </div>
    );
}