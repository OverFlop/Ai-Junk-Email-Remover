"use client";

import { useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function CallbackPage() {
    const searchParams = useSearchParams();
    const router = useRouter();

    useEffect(() => {
        const code = searchParams.get("code");
        if (!code) return;

        async function sendCode() {
            await fetch("http://127.0.0.1:5000/api/emails", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ authCode: code }),
            });

            // optional: redirect to inbox page later
            // router.push("/inbox");
        }

        sendCode();
    }, [searchParams]);

    return (
        <main className="flex min-h-screen items-center justify-center">
            <p className="text-lg">Scanning your inbox…</p>
        </main>
    );
}
