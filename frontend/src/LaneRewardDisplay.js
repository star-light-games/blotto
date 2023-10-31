import { Typography } from '@mui/material';
import React from 'react';
import { Card, CardContent } from '@mui/material';

export default function LaneRewardDisplay({ laneReward, currentLaneReward, setCurrentLaneReward, notSelectable }) {
    // Determine if the current card should have a border based on the selected reward
    const isSelected = !notSelectable && currentLaneReward && currentLaneReward.name === laneReward.name;

    return (
        <Card 
            onClick={notSelectable ? () => {} : () => setCurrentLaneReward(laneReward)}
            style={{
                ...(notSelectable ? {} : {cursor: 'pointer'}),
                border: isSelected ? '5px solid black' : 'none',  // Apply border if selected
                maxWidth: 500,
            }}
        >
            <CardContent>
                <Typography variant="h4">
                    {laneReward.name}
                </Typography>
                <Typography variant='h6'>
                    {laneReward.threshold ? `${laneReward.threshold}: ${laneReward.reward_description}` : `${laneReward.reward_description}`}
                </Typography>
            </CardContent>
        </Card>
    );
}