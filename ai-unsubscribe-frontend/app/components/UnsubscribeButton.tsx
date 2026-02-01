import { Button } from "@mui/material";
import { Email } from "@/app/components/SenderCard";

export default function UnsubscribeButton({ emails, token }: { emails: Email[], token: string }) {
  const handleUnsubscribe = () => {
    fetch("http://127.0.0.1:5001/api/unsubscribe", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(emails.filter(msg => msg.isSelected).map(msg => msg.id)),
    }).then(() => setSuccess(true)).catch((err) => setError(err));
  };

  return (
    <Button
      variant="contained"
      color="primary"
      onClick={handleUnsubscribe}
    >
      Unsubscribe Selected ({senders.filter(sender => sender.messages.some(msg => msg.isSelected)).length})
    </Button>
  );
}