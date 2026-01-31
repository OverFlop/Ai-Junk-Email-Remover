import { NextResponse } from "next/server";

export async function GET() {
    return NextResponse.json([
        {
            id: "1",
            from: "Medium",
            subject: "5 articles you might like",
            snippet: "Read the latest stories on tech...",
            isNewsletter: true,
        },
    ]);
}
