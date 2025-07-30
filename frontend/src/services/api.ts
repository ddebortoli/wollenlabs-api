import axios from 'axios';
import { BatchResponse, BatchStatus, UrlCheck } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const checkUrls = async (urls: string[]): Promise<BatchResponse> => {
    const response = await api.post('/url-checks/check_urls/', { urls });
    return response.data;
};

export const getBatchStatus = async (batchId: string): Promise<BatchStatus> => {
    const response = await api.get(`/url-checks/batch_status/?batch_id=${batchId}`);
    return response.data;
};

export const getBatchResults = async (batchId: string): Promise<UrlCheck[]> => {
    const response = await api.get(`/url-checks/batch_results/?batch_id=${batchId}`);
    return response.data;
};