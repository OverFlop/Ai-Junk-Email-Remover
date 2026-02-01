"use client";

import {
    Card,
    CardContent,
    Typography,
    Button,
    Stack,
} from "@mui/material";

export interface Email {
    id: string;
    from: string;
    subject: string;
    snippet: string;
    unsubscribeUrl?: string;
}

interface EmailCardProps {
    email: Email;
    onUnsubscribe?: (emailId: string) => void;
}

export default function EmailCard({
    email,
    onUnsubscribe,
}: EmailCardProps) {
    return (
        <Card variant="outlined">
            <CardContent>
                <Stack spacing={1}>
                    <Typography variant="subtitle2" color="text.secondary">
                        {email.from}
                    </Typography>

                    <Typography variant="h6">
                        {email.subject}
                    </Typography>

                    <Typography variant="body2" color="text.secondary">
                        {email.snippet}
                    </Typography>

                    {email.unsubscribeUrl && (
                        <Button
                            variant="outlined"
                            color="error"
                            onClick={() => onUnsubscribe?.(email.id)}
                            sx={{ alignSelf: "flex-start", mt: 1 }}
                        >
                            Unsubscribe
                        </Button>
                    )}
                </Stack>
            </CardContent>
        </Card>
    );
}
