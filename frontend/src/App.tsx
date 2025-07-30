import React, { useState } from 'react';
import { Container, Typography, Box, Alert, CircularProgress } from '@mui/material';
import { UrlForm } from './components/UrlForm';
import { ProgressBar } from './components/ProgressBar';
import { ResultsTable } from './components/ResultsTable';
import { checkUrls, getBatchStatus, getBatchResults } from './services/api';
import { BatchStatus, UrlCheck } from './types';

function App() {
  const [batchId, setBatchId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState<BatchStatus | null>(null);
  const [results, setResults] = useState<UrlCheck[]>([]);
  const MAX_POLLS = 3;
  const POLL_INTERVAL = 1000;

  const handleSubmit = async (urls: string[]) => {
    try {
      setIsSubmitting(true);
      setError(null);
      const response = await checkUrls(urls);
      setBatchId(response.batch_id);
      setResults(response.urls);

      let pollCount = 0;
      const pollInterval = setInterval(async () => {
        try {
          pollCount++;
          if (pollCount >= MAX_POLLS) {
            clearInterval(pollInterval);
            const finalResults = await getBatchResults(response.batch_id);
            setResults(finalResults);
            return;
          }

          const batchStatus = await getBatchStatus(response.batch_id);
          setStatus(batchStatus);

          if (batchStatus.pending === 0) {
            clearInterval(pollInterval);
            const results = await getBatchResults(response.batch_id);
            setResults(results);
          }
        } catch (err) {
          console.error('Error polling status:', err);
          clearInterval(pollInterval);
          setError("Error checking URLs status");
        }
      }, POLL_INTERVAL);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit URLs');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          URL Health Checker
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <UrlForm onSubmit={handleSubmit} loading={isSubmitting} />
        
        {isSubmitting && (
          <Box display="flex" justifyContent="center" my={4}>
            <CircularProgress />
          </Box>
        )}

        {batchId && status && (
          <>
            <ProgressBar status={status} />
            <ResultsTable results={results} />
          </>
        )}
      </Box>
    </Container>
  );
}

export default App;