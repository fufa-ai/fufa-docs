---
title: Connect Telegram
description: Create a Telegram bot with BotFather and paste its token into Fufa, so messages customers send your bot arrive in your inbox.
sidebar:
  order: 5
---

Your Telegram bot is connected to a Fufa inbox. Customers who message the bot appear in the inbox, and replies from you or your AI agent are sent as the bot.

## Before you start

- You need the **Owner** or **Admin** role in the workspace.
- A Telegram account, on your phone or on the web.

## Create a bot

1. In Telegram, open [@BotFather](https://t.me/BotFather). Fufa's connect dialog also has an **Open BotFather** button.
2. Send `/newbot`.
3. Choose a display name, then a username that ends in `bot`, for example `yourstore_bot`.
4. BotFather replies with the bot's token, which looks like `123456789:AAH…`. Copy it.

Anyone with the token controls the bot, so keep it private.

## Connect it to Fufa

1. Go to **Settings → Inboxes** and open an inbox.
2. Under **Channels**, select **Add channel**, then **Telegram**.
3. Paste the token under **Paste the bot token** and select **Connect bot**.
4. Fufa shows the bot's chat link and a QR code. Select **Open in Telegram**, or scan the code with your phone, and send your bot a message. It shows up in this inbox.

## Set up the bot's profile

Customers see the bot's photo, a short bio, and the text shown before they tap **Start**. Change these by messaging @BotFather. The **Bot profile** section on the channel page links to it.

Share the bot's **Chat link**, `t.me/` followed by its username, on your website, in your Instagram bio, or in order emails.

## Check it works

The **Connection** card on the channel page shows **Valid** when Fufa can send and receive messages as the bot. Send the bot a message from another Telegram account, and it appears in the inbox.

## Common questions

### The connection shows Revoked. What happened?

Telegram stopped accepting the saved token, usually because it was revoked in BotFather. Get the current token from BotFather, then select **Update token** on the channel page and paste it.

### Can I use an existing bot?

Yes. Paste that bot's token instead of creating a new one. If something else uses the same bot, such as another tool, disconnect it there first, because Telegram delivers a bot's messages to one place.

### Can an AI agent answer on Telegram?

Yes. Open the agent's **Deploy** page and turn on Telegram under **Where Fufa replies**. See [Create an agent](/agents/create-an-agent/).

## Related

- [Reply from the inbox](/inbox/reply/)
- [Connect WhatsApp](/channels/whatsapp/)
- [Create an agent](/agents/create-an-agent/)
