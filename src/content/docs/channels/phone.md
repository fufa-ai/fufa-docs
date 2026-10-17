---
title: Connect a phone number
description: Connect a phone number to a Fufa inbox, from your own carrier's SIP trunk or an existing Retell account, and choose which voice agent answers calls to it.
sidebar:
  order: 6
---

Calls to your phone number are answered by a Fufa voice agent. The number is connected to an inbox, and you choose which agent picks up.

## Before you start

- You need the **Owner** or **Admin** role in the workspace.
- An agent with voice turned on. Open the agent's **Voice** page and turn on **Enable voice**, then choose its voice, language and greeting. See [Create an agent](/agents/create-an-agent/).
- A phone number, either on a SIP trunk from your carrier or already in your Retell account.

## Add the number

1. Go to **Settings → Inboxes** and open an inbox.
2. Under **Channels**, select **Add channel**, then **Phone / Voice**.
3. Choose how to bring the number in:
   - **Import from SIP trunk** brings in a number from your own carrier's trunk. Enter the **Phone number** in international format, such as `+14155551234`. Then enter the trunk's **Termination URI**, such as `your-trunk.pstn.twilio.com`, with its **SIP username** and **SIP password**.
   - **Already in Retell** connects a number that's already in your Retell account. Enter the **Phone number** exactly as it appears there.
4. Pick the **Answering agent**, and add a **Label** such as *Support line* if you like.
5. Select **Connect number**. Fufa shows **Voice number connected** with your number.

One inbox can hold several numbers. Add each one the same way.

## Change who answers

Open the number on the inbox's channel list. Under **Routing**, choose a different **Answering agent** and save.

## Check it works

Call the number from another phone. The agent answers with the greeting you set on its **Voice** page.

## Common questions

### The Answering agent list is empty. Why?

No agent has voice turned on yet. Open an agent, go to **Voice**, turn on **Enable voice**, and save. It then appears in the list.

### Does Fufa handle outgoing calls?

This channel answers incoming calls to your number. The agent picks up every call to it.

### What format should the phone number use?

International (E.164) format: a plus sign, the country code and the number, with no spaces. For example, `+919876543210` or `+14155551234`.

### Calls stopped reaching the agent. What should I check?

Open the number's page and check the **SIP trunk** details and the **Inbound webhook**. If you changed anything at your carrier, select **Rebind webhook** so calls route to Fufa again.

## Related

- [Create an agent](/agents/create-an-agent/)
- [Connect WhatsApp](/channels/whatsapp/)
- [Reply from the inbox](/inbox/reply/)
