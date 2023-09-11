import { Card, CardContent, Typography, Box, useTheme } from '@mui/material';
import { snakeCase } from './utils';

function TcgCard({ card, isSelected, onCardClick, onMouseEnter, doNotBorderOnHighlight, displayArt , height, width, displayRedX }) {
    const theme = useTheme();
    const isDarkMode = theme.palette.mode === 'dark';

    // Define card background color based on theme mode
    const cardBackgroundColor = isDarkMode ? '#555' : '#eee';

    const outlineSize = 2;

    return (
      <div 
          style={{
              border: isSelected ? `${outlineSize}px solid black` : 'none',
              boxSizing: 'border-box',
              cursor: 'pointer',
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

            {displayArt ? <Box 
                display="flex" 
                justifyContent="center" 
                alignItems="center" 
                height="100%" 
                width="100%">
                <img 
                    src={`/images/${snakeCase(card.name)}.png`} 
                    alt={`${snakeCase(card.name)}-character-art`} 
                    style={{maxWidth: '100%', maxHeight: '100%'}} 
                />
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
            <Box mt={2} style={{ maxHeight: '150px', overflowY: 'auto' }}>  {/* Apply max-height and overflow-y */}
                <Typography variant="body2" color="textSecondary">
                    {card.creatureTypes.join(', ')}
                </Typography>
                <Typography>
                    <ul>
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
