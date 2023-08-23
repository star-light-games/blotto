import { Card, CardContent, Typography, Box } from '@mui/material';

function TcgCard({ card }) {
    console.log(card);
    console.log(card.creatureTypes)
    // console.log(card.creatureTypes.join(', '))
    return (
        <Card 
        variant="outlined" 
        style={{ 
            width: 250, 
            height: 300, 
            position: 'relative', 
            backgroundColor: '#eee',
            overflow: 'hidden'
        }}
        >
        <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="flex-start">
            <Typography variant="h6">{card.name}</Typography>
            <Typography variant="h6">{card.cost}</Typography>
            </Box>

            <Box mt={2}>
            <Typography variant="body2" color="textSecondary">
                {card.creatureTypes.join(', ')}
            </Typography>
            <Typography>
                Abilities: 
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
            <Typography variant="h6" style={{ marginRight: 5 }}>{card.attack}</Typography>
            <Typography variant="h6">{card.health}</Typography>
            </Box>
        </CardContent>
        </Card>
    );
    }
  
export default TcgCard;