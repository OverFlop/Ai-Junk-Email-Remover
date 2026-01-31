"use client";
import { signIn } from "next-auth/react";
import Button from "@mui/material/Button";
import GoogleIcon from "@mui/icons-material/Google";


export default function Home() {
    return (
        <main className="flex min-h-screen items-center justify-center bg-zinc-50">
            <div className="w-full max-w-md rounded-xl bg-white p-8 shadow">
                <h1 className="mb-4 text-2xl font-semibold">AI Email Unsubscribe</h1>
                <p className="mb-6 text-zinc-600">
                    Scan your inbox and unsubscribe from unwanted newsletters.
                </p>
                    <Button
                        fullWidth
                        variant="contained"
                        startIcon={<GoogleIcon />}
                        onClick={() => signIn("google")}
                        sx={{
                            py: 1.5,
                            backgroundColor: "black",
                            "&:hover": {
                                backgroundColor: "#222",
                            },
                            textTransform: "none",
                            fontSize: "1rem",
                        }}
                    >
                        Sign in with Google
                    </Button>

            </div>
        </main>
    );
}
