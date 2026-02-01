import { Card, CardActionArea, CardContent, Typography } from "@mui/material";
import { memo } from "react";

export interface Email {
  summary: string,
  subject: string
  id: string,
  unsubscribeMethod: string,
  unsubscribeUrl: string,
  unsubscribeAddress: string,
}

export interface Sender {
  address: string,
  isSelected: boolean,
  messages: Email[],
}

const SenderCard = memo(({ sender, index, toggleSelectedCard }: { sender: Sender, index: number, toggleSelectedCard: (index: number) => void }) => {
  return (
    <Card key={sender.address}>
      <CardActionArea
        onClick={() => toggleSelectedCard(index)}
        data-active={sender.isSelected ? '' : undefined}
        sx={{
          height: '100%',
          '&[data-active]': {
            backgroundColor: 'action.selected',
            '&:hover': {
              backgroundColor: 'action.selectedHover',
            },
          },
        }}
      >
        <CardContent sx={{ height: '100%' }}>
          <Typography variant="h5" component="div">
            {sender.address}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {sender.messages.length} messages
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
});

export default SenderCard;