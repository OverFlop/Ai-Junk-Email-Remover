"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams, useRouter, redirect } from "next/navigation";
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { Box, Button, Card, CardActionArea, CardContent, LinearProgress, Stack, Typography } from "@mui/material";
import SenderCard from "../components/SenderCard";
import Link from "next/link";

export interface Email {
    summary: string,
    subject: string
    id: string,
    from: string,
    isSelected: boolean,
    unsubscribeMethod: string,
    unsubscribeUrl: string,
    unsubscribeAddress: string,
}

export interface Sender {
    address: string,
    messages: Email[],
}

export default function EmailsPage() {
    const searchParams = useSearchParams();
    const router = useRouter();

    const [emails, setEmails] = useState<Email[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState<boolean>(false);

    let [token, setToken] = useState("");

    useEffect(() => {
        const code = searchParams.get("code");
        if (!code) {
            redirect("/");
        }

        async function getAccessToken() {
            const res = await fetch("http://127.0.0.1:5001/api/token", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ authCode: code }),
            });
            if (!res.ok) {
                throw new Error("failed to sign in");
            }
            const data = await res.json();
            const accessToken = data["access_token"];
            return accessToken;
        }

        async function getPart(token: string, pageToken?: string) {
            const params = new URLSearchParams();
            if (pageToken) {
                params.set("pageToken", pageToken);
            }
            const res = await fetch("http://127.0.0.1:5001/api/emails?" + params.toString(), {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}`, "Accept": "application/json" }
            });
            return res.json();
        }

        async function getEmails() {
            const token = await getAccessToken();
            let pageToken;
            while (true) {
                const part = await getPart(token, pageToken);
                if (!part.data) {
                    break;
                }
                setEmails(emails.concat(part.data));
                break;
                if (!part.nextPageToken) {
                    break;
                }
                pageToken = part.nextPageToken;
            }
            setToken(token);
        }

        getEmails().catch(err => setError(err)).then(() => setLoading(false));
    }, [searchParams]);

    let sendersMap = new Map<String, Sender>();
    for (let email of emails) {
        if (!sendersMap.has(email.from)) {
            sendersMap.set(email.from, {
                address: email.from,
                messages: []
            });
        }
        let sender = sendersMap.get(email.from)!;
        if (sender.messages.some(msg => msg.isSelected)) {
            email.isSelected = true;
        }
        sender.messages.push(email);
    }

    let senders = sendersMap.values().toArray();

    const toggleSelectedCard = (index: number) => {
        for (let msg of senders[index].messages) {
            msg.isSelected = !msg.isSelected;
        }
        setEmails(senders.flatMap(sender => sender.messages));
    };

    const handleUnsubscribe = () => {
        setLoading(true);
        fetch("http://127.0.0.1:5001/api/unsubscribe", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify(emails.filter(msg => msg.isSelected).map(msg => msg.id)),
        }).then(() => { setSuccess(true); setLoading(false); }).catch((err) => setError(err));
    };

    if (error) {
        redirect("/");
    }
    if (success) {
        return (
            <div className="p-4 flex flex-col">
                <span className="m-2">Done!</span>
                <Button variant="contained" color="primary" onClick={() => redirect("/")} className="m-2">Go Back</Button>
            </div>
        )
    }

    console.log("hi");

    return (
        <>
            <Box sx={{ position: 'relative', width: '100%' }}>
                {loading && <LinearProgress />}
                {!loading &&
                    <Stack
                        direction="row"
                        justifyContent="flex-end"
                        sx={{ padding: 4 }}
                    >
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleUnsubscribe}
                        >
                            Unsubscribe Selected ({senders.filter(sender => sender.messages.some(msg => msg.isSelected)).length})
                        </Button>
                    </Stack>}
                <Box
                    sx={{
                        width: '100%',
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(min(200px, 100%), 1fr))',
                        gap: 2,
                        padding: 4,
                    }}
                >
                    {senders.map((sender, index) => (
                        <SenderCard key={index} sender={sender} index={index} toggleSelectedCard={toggleSelectedCard}></SenderCard>
                    ))}
                </Box>
            </Box >
        </>
    );
}

