import React, { useEffect, useState } from 'react';
import { URL } from './settings';
import TcgCard from './TcgCard';
import { Typography } from '@mui/material';
import { Grid } from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

export const getOrganizedCardPool = (data) => {
    // Custom order map for creature types
    const creatureTypeOrder = {
        "Avatar": 1,
        "Earth": 2,
        "Water": 3,
        "Air": 4,
        "Fire": 5
    };

    return Object.values(data.cards).sort((a, b) => {
        const aOrder = creatureTypeOrder[a.creatureTypes?.[0]] || Infinity;
        const bOrder = creatureTypeOrder[b.creatureTypes?.[0]] || Infinity;

        if (aOrder < bOrder) {
            return -1;
        }
        if (aOrder > bOrder) {
            return 1;
        }

        const aCost = a.cost;
        const bCost = b.cost;

        if (aCost < bCost) {
            return -1;
        }
        if (aCost > bCost) {
            return 1;
        }

        // If creatureTypes order is the same, compare the names
        return a.name.localeCompare(b.name);
    });
}


export default function SeventeenLandsPage() {
    const [cardPool, setCardPool] = useState([]);
    const [stats, setStats] = useState([]);

    useEffect(() => {
        fetch(`${URL}/api/seventeen_lands`)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json()
        })
        .then((data) => {
            setStats(data);
        })
    }, [])

    useEffect(() => {
        fetch(`${URL}/api/card_pool`)
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => {
          setCardPool(getOrganizedCardPool(data));
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }, []);

    console.log(stats);

    return (
        <div>
            <Typography variant="h2">17Lands</Typography>
            <Grid container direction="column" spacing={3}>
                {cardPool.map((card) => (
                    <Grid item container direction="row">
                        <Grid item>
                            <TcgCard card={card} displayArt={true} doNotBorderOnHighlight={true} doNotShowPointerCursor={true} />
                        </Grid>
                        <Grid item>
                            <Card>
                                <CardContent>
                                    <Typography variant="h3">Stats</Typography>
                                    <Typography variant="h4">Win Rate: {stats?.[card.name]?.win_rate}</Typography>
                                    <Typography variant="h4">Pick Rate: {stats?.[card.name]?.pick_rate}</Typography>
                                    <Typography variant="h4">Last changed time: {new Date(stats?.[card.name]?.last_changed_time * 1000).toLocaleString()}</Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    </Grid>
                ))}
            </Grid>
        </div>
    )
}