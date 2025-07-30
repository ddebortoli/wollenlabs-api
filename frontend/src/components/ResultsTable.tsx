import React from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Chip
} from '@mui/material';
import { UrlCheck } from '../types';

interface ResultsTableProps {
    results: UrlCheck[];
}

export const ResultsTable: React.FC<ResultsTableProps> = ({ results }) => {
    if (results.length === 0) return null;

    return (
        <TableContainer component={Paper} sx={{ mt: 4 }}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>URL</TableCell>
                        <TableCell align="center">Status</TableCell>
                        <TableCell align="right">Response Time</TableCell>
                        <TableCell>Error</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {results.map((result) => (
                        <TableRow key={result.id}>
                            <TableCell component="th" scope="row">
                                {result.url}
                            </TableCell>
                            <TableCell align="center">
                                <Chip
                                    label={result.status_code || 'N/A'}
                                    color={result.is_reachable ? 'success' : 'error'}
                                    variant="outlined"
                                />
                            </TableCell>
                            <TableCell align="right">
                                {result.response_time 
                                    ? `${(result.response_time * 1000).toFixed(0)}ms`
                                    : 'N/A'}
                            </TableCell>
                            <TableCell>
                                {result.error_message || '-'}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};