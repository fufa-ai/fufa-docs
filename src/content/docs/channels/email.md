---
title: Connect email
description: Give a Fufa inbox an email address, either a ready-made Fufa address or your own domain, so customer emails land in the inbox and you or your agent reply from it.
sidebar:
  order: 4
---

Customers email an address you choose, and those emails arrive in a Fufa inbox as conversations. You or your AI agent reply from Fufa, and the reply goes out from the same address.

## Before you start

- You need the **Owner** or **Admin** role in the workspace.
- To use your own domain, such as `support@yourstore.com`, you also need access to your domain's DNS settings to add 3 records, and access to the mailbox's settings to turn on forwarding. Allow about 10 minutes. Fufa saves your progress if you stop halfway.

## Connect an address

1. Go to **Settings → Inboxes** and open an inbox.
2. Under **Channels**, select **Add channel**, then **Email**.
3. Choose how to start:
   - **Use a Fufa address** works instantly, with nothing to configure. You can add your own domain later, and conversations stay in the same inbox.
   - **Use your own domain** lets customers see your brand, and replies are signed for your domain so they land in the inbox rather than spam.
4. Enter the **Email address** and the **Sender name** customers see next to it, then finish the steps on screen.

## Set up your own domain

If you chose your own domain, the channel page walks you through two things.

**DNS records.** Add the records shown on the page at your DNS provider: the **Signing records**, the **Bounce records**, and a **DMARC policy**. Each record shows **Waiting** until Fufa finds it, then **Found**. DNS changes can take a while to show up.

**Mailbox forwarding.** Forward your existing mailbox to the address Fufa gives you, so emails customers send you reach the inbox. Choose your provider for the exact steps: **Gmail / Google Workspace**, **Microsoft 365** or **Other**. Gmail sends a confirmation link before forwarding starts. Open it under **Mailbox forwarding** and select **Confirm**.

## Set your sender details

Under **Sender**, set the **Sender name** and a **Signature**. They're used on every reply, whether you or your agent sends it.

## Check it works

Send an email to the address from another account. It appears in the inbox as a new conversation. Reply from Fufa, and the reply arrives in that account's mailbox from your address.

## Common questions

### Should I start with a Fufa address or my own domain?

Start with a Fufa address if you want to be live in a minute. Switch to your own domain when you're ready. Your own domain looks more trustworthy to customers, and signed replies are less likely to land in spam.

### Where do I put the address?

On your contact page, in your order confirmation emails, and anywhere else customers look for help. Messages sent to it land in the inbox, and replies go out from it.

### Why does the page say Sending is paused?

Fufa paused sending from this address, for example because of bounces. Fix the cause shown on the page, then select **Try sending again**.

### Can an AI agent reply to emails?

Yes. Open the agent's **Deploy** page and turn on email under **Where Fufa replies**. See [Create an agent](/agents/create-an-agent/).

## Related

- [Reply from the inbox](/inbox/reply/)
- [Add live chat to your website](/channels/live-chat/)
- [Create an agent](/agents/create-an-agent/)
