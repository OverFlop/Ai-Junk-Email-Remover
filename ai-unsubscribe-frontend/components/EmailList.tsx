"use client";

import { Email } from "@/types/email";
import EmailCard from "./EmailCard";

export default function EmailList({ emails }: { emails: Email[] }) {
    return (
        <div className="space-y-4">
            {emails.map((email) => (
                <EmailCard key={email.id} email={email} />
            ))}
        </div>
    );
}
