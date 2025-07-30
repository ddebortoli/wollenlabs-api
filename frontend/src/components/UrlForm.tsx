import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';

interface UrlFormProps {
    onSubmit: (urls: string[]) => void;
    loading: boolean;
}

export const UrlForm: React.FC<UrlFormProps> = ({ onSubmit, loading }) => {
    const [urlInput, setUrlInput] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const urls = urlInput
            .split('\n')
            .map(url => url.trim())
            .filter(url => url !== '');
        
        if (urls.length > 0) {
            onSubmit(urls);
            setUrlInput('');
        }
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%', mt: 2 }}>
            <Typography variant="h6" gutterBottom>
                Enter URLs (one per line)
            </Typography>
            <TextField
                multiline
                rows={4}
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://example.com&#10;https://another-example.com"
                fullWidth
                variant="outlined"
                disabled={loading}
                sx={{ mb: 2 }}
            />
            <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading || !urlInput.trim()}
                fullWidth
            >
                {loading ? 'Processing...' : 'Check URLs'}
            </Button>
        </Box>
    );
};