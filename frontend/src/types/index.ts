export interface UrlCheck {
    id: number;
    url: string;
    status_code: number | null;
    response_time: number | null;
    is_reachable: boolean;
    error_message: string;
    checked_at: string;
    batch_id: string;
}

export interface BatchStatus {
    total: number;
    completed: number;
    pending: number;
    success_rate: number;
}

export interface BatchResponse {
    batch_id: string;
    message: string;
    urls: UrlCheck[];
}