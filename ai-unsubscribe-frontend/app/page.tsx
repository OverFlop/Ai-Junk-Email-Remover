"use client";
import { signIn } from "next-auth/react";

export default function Home() {
    return (
        <main className="flex min-h-screen items-center justify-center bg-zinc-50">
            <div className="w-full max-w-md rounded-xl bg-white p-8 shadow">
                <h1 className="mb-4 text-2xl font-semibold">AI Email Unsubscribe</h1>
                <p className="mb-6 text-zinc-600">
                    Scan your inbox and unsubscribe from unwanted newsletters.
                </p>
                <button
                    onClick={() => signIn("google")}
                    className="w-full rounded-lg bg-black py-3 text-white"
                >
                    Sign in with Google
                </button>
            </div>
        </main>
    );
}
