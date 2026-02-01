import { Email } from "@/types/email";

export const mockEmails: Email[] = [
    {
        id: "1",
        from: "IHG One Rewards",
        subject: "Your January eStatement",
        snippet: "Plus, see how far you can go with Silver Elite status",
        isNewsletter: true,
        unsubscribeUrl: "https://example.com/unsub",
        unsubscribeMethod: "GET",
    },
];
