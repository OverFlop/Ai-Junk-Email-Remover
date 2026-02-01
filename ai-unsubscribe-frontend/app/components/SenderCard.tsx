import { Card, CardActionArea, CardContent, Typography } from "@mui/material";
import { memo } from "react";

export interface Email {
  summary: string,
  subject: string
  id: string,
  isSelected: boolean,
  unsubscribeMethod: string,
  unsubscribeUrl: string,
  unsubscribeAddress: string,
}

export interface Sender {
  address: string,
  messages: Email[],
}

const SenderCard = ({ sender, index, toggleSelectedCard }: { sender: Sender, index: number, toggleSelectedCard: (index: number) => void }) => {
  return (
    <Card key={index}>
      <CardActionArea
        onClick={() => toggleSelectedCard(index)}
        data-active={sender.messages.some(msg => msg.isSelected) ? '' : undefined}
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
          <Typography component="div" overflow="scroll">
            {sender.address}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {sender.messages.length} messages
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default SenderCard;