import React from 'react';
import { Box, LinearProgress, Typography } from '@mui/material';
import { BatchStatus } from '../types';

interface ProgressBarProps {
    status: BatchStatus;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ status }) => {
    const progress = (status.completed / status.total) * 100;
    const successRate = status.success_rate * 100;

    return (
        <Box sx={{ width: '100%', mt: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                    Progress: {status.completed} / {status.total} URLs checked
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    {progress.toFixed(1)}%
                </Typography>
            </Box>
            <LinearProgress 
                variant="determinate" 
                value={progress} 
                sx={{ height: 8, borderRadius: 2 }}
            />
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                <Typography variant="body2" color="text.secondary">
                    Success Rate: {successRate.toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    Pending: {status.pending}
                </Typography>
            </Box>
        </Box>
    );
};