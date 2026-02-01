export interface Email {
    id: string;
    from: string;
    subject: string;
    snippet: string;
    isNewsletter: boolean;
    unsubscribeUrl?: string;
    unsubscribeMethod?: "GET" | "POST" | "MAILTO";
}
