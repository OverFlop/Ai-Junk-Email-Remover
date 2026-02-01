import EmailList from "@/components/EmailList";
import { mockEmails } from "@/lib/mockEmails";

export default function DashboardPage() {
    return (
        <main className="p-6 max-w-3xl mx-auto">
            <h1 className="text-2xl font-semibold mb-4">Your Emails</h1>
            <EmailList emails={mockEmails} />
        </main>
    );
}
