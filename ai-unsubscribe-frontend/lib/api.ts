export async function fetchEmails() {
    const res = await fetch("/api/emails");
    if (!res.ok) throw new Error("Failed to fetch emails");
    return res.json();
}

export async function unsubscribe(emailId: string) {
    return fetch(`/api/unsubscribe/${emailId}`, { method: "POST" });
}
