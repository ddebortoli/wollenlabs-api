import { useState, useEffect } from 'react';
import { BatchStatus, UrlCheck } from '../types';
import { getBatchStatus, getBatchResults } from '../services/api';

export const useBatchStatus = (batchId: string | null) => {
    const [status, setStatus] = useState<BatchStatus | null>(null);
    const [results, setResults] = useState<UrlCheck[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let intervalId: NodeJS.Timeout;

        const fetchStatus = async () => {
            if (!batchId) return;

            try {
                setLoading(true);
                const batchStatus = await getBatchStatus(batchId);
                setStatus(batchStatus);

                if (batchStatus.pending === 0) {
                    const batchResults = await getBatchResults(batchId);
                    setResults(batchResults);
                    clearInterval(intervalId);
                }

                setError(null);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred');
            } finally {
                setLoading(false);
            }
        };

        if (batchId) {
            fetchStatus();
            intervalId = setInterval(fetchStatus, 2000);
        }

        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [batchId]);

    return { status, results, loading, error };
};