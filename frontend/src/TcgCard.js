import { Card, CardContent, Typography, Box, useTheme } from '@mui/material';
import { snakeCase, getCardBackgroundColor } from './utils';

function TcgCard({ card, isSelected, onCardClick, onMouseEnter, doNotBorderOnHighlight, displayArt , height, width, displayRedX }) {
    const theme = useTheme();
    const isDarkMode = theme.palette.mode === 'dark';

    // Define card background color based on theme mode
    const cardBackgroundColor = getCardBackgroundColor(card, isDarkMode);

    const outlineSize = 2;

    const displayCreatureTypes = card.creatureTypes.includes('Avatar');

    const getRarityColor = (rarity) => {
        switch (rarity) {
          case 'common':
            return 'white';
          case 'rare':
            return 'orange';
          default:
            return 'transparent'; // Default to transparent for other rarities or no rarity
        }
      };

      const ovalStyle = {
        position: 'absolute',
        top: '53%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '20px',
        height: '26px',
        backgroundColor: getRarityColor(card.rarity),
        border: '0px solid black',
        borderRadius: '50%',
        zIndex: 1,
        boxShadow: 'inset 2px 2px 5px rgba(0, 0, 0, 0.3), inset -2px -2px 5px rgba(255, 255, 255, 0.5)', // inner shadow for added depth
        // background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(0, 0, 0, 0.2) 100%)', // subtle gradient for a shiny effect
      };
      

      const aspectRatioBox = {
        position: 'relative',
        width: '100%',
        paddingBottom: '75.7%',  // for 4:3 aspect ratio. Adjust for other ratios.
        overflow: 'hidden'
      };
      
      const imageStyle = {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover'
      };

    return (
      <div 
          style={{
              border: isSelected ? `${outlineSize}px solid black` : 'none',
              boxSizing: 'border-box',
              ...(doNotBorderOnHighlight ? {} : {cursor: 'pointer'}),
              width: width || 250 + (outlineSize * 2),
              height: height || (displayArt ? 400 : 250) + (outlineSize * 2),
          }}
          onClick={onCardClick ? () => onCardClick(card) : null}
          onMouseEnter={e => {
            if (!doNotBorderOnHighlight) {
                e.currentTarget.style.border = `${outlineSize}px solid blue`;
            }
            onMouseEnter && onMouseEnter();
          }}
          onMouseLeave={e => {
            if (isSelected) {
                e.currentTarget.style.border = `${outlineSize}px solid black`;
            } else {
                e.currentTarget.style.border = 'none';
            }
            }}
      >
        <Card 
        variant="outlined" 
        style={{ 
            width: width || 250,
            height: height || (displayArt ? 400 : 250),
            position: 'relative', 
            backgroundColor: cardBackgroundColor,  // Use the defined card background color
            overflow: 'hidden',
            color: theme.palette.text.primary
        }}
        >
        <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="flex-start">
            <Typography variant="h6">{card.name}</Typography>
            <Typography variant="h6">{card.cost}</Typography>
            </Box>

            {displayArt ? 
                <Box display="flex" justifyContent="center" alignItems="center" height="100%" width="100%">
                    <div style={aspectRatioBox}>
                    <img 
                        src={`/images/${snakeCase(card.name)}.png`} 
                        alt={`${snakeCase(card.name)}-character-art`} 
                        style={imageStyle} 
                    />
                    </div>
                {displayRedX && (
                    <img
                        src={'/images/red_x.png'}
                        alt="red-x"
                        style={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            right: 0,
                            bottom: 0,
                            zIndex: 2,
                            maxWidth: '100%',
                            maxHeight: '100%',
                        }}
                    />
            )}
            </Box> : null}
            {card.rarity === 'rare' && <div style={ovalStyle}></div>}
            <Box 
                mt={2} 
                style={{ 
                    maxHeight: '125px', 
                    overflowY: 'auto',
                    paddingRight: '20px'  // Add some padding to the right
                }}
            >
                {displayCreatureTypes && <Typography variant="body2" color="textSecondary">
                    {card.creatureTypes.join(', ')}
                </Typography>}
                <Typography>
                    <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
                        {card.abilities.map((ability, index) => (
                            <li key={index}>{ability.description}</li>
                        ))}
                    </ul>
                </Typography>
                </Box>

            <Box 
                position="absolute" 
                bottom={10} 
                right={10} 
                display="flex" 
                alignItems="center"
            >
            <Typography variant="h6">{card.attack}</Typography>
            <Typography variant="h6">/</Typography>
            <Typography variant="h6">{card.health}</Typography>
            </Box>
        </CardContent>
        </Card>
      </div>
    );
}

export default TcgCard;
