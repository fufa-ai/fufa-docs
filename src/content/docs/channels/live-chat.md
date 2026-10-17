---
title: Add live chat to your website
description: Create a Fufa chat widget, style it to your brand, and paste one script tag on your site, or turn on the Shopify app embed, so visitors can chat with you and your agent.
sidebar:
  order: 2
---

A chat button appears on your website. Visitors open it to message you, and every conversation lands in your Fufa inbox, where you or an AI agent reply.

If you connected Shopify while [creating your workspace](/start/create-a-workspace/), Fufa already made this chat for you. Skip to [Put the chat on your site](#put-the-chat-on-your-site).

## Before you start

- You need the **Owner** or **Admin** role in the workspace.
- Access to your website's code, or to your Shopify theme editor.

## Create the chat

1. Go to **Settings → Inboxes** and open an inbox.
2. Under **Channels**, select **Add channel**, then **Live Chat**.
3. On the **General** tab, enter the **Name** shown in the chat header and add an **Avatar**.
4. Under **Allowed origins**, add every site the chat will run on, with its full address including `https://`, for example `https://shop.example.com`. The chat only loads on these sites.
5. If you sell on Shopify, choose your **Connected store** so the chat knows your products and orders.
6. Select **Create Live Chat Widget**. Fufa shows **Live chat channel created**.

Each inbox can hold one live chat.

## Make it look like your brand

All of these are optional. The **Live preview** shows changes before you select **Save changes**.

- **Appearance**: the **Brand color**, the launcher's color, size, icon and **Placement** on the page.
- **Conversation**: the **Greeting**, **Quick suggestions** that visitors can tap before they type, and **Linked channels** such as your WhatsApp number, offered as other ways to reach you.
- **Proactive messages**: messages that greet visitors before they start a chat, triggered immediately, on scroll, after a delay, or on exit intent.
- **Access & leads**: whether visitors sign in with an email code, a phone code or Google, and whether the chat asks for their name, email or phone. You can also allow file uploads and voice calls.

## Put the chat on your site

**On any website**: open the chat's **General** tab and copy the **Embed snippet**. Paste it just before `</body>` on every page that should show the chat. It looks like this:

```html
<script data-api-url="https://api.fufa.ai/api" src="https://widget.fufa.ai/snippet.js" data-widget-id="YOUR_WIDGET_ID" async></script>
```

**On Shopify**: open your theme editor's **App embeds**, turn on Fufa's **Chat** embed, and save the theme. App embeds are off by default, so the chat stays hidden until you turn it on.

To keep the chat off certain pages, such as checkout, add rules under **Hide widget on pages**.

## Check it works

Open your website in a private browser window. The chat button appears in the corner you chose. Send a message, and it shows up in your Fufa inbox.

## Common questions

### The chat doesn't appear on my site. What should I check?

First, check that your site's address is in **Allowed origins**, written exactly as it appears in the browser, including `https://` and any `www`. Next, check that the snippet is on the page, or that the Shopify **Chat** app embed is on and the theme is saved. Finally, check that no **Hide widget on pages** rule matches the page.

### Can returning visitors see their old chats?

Yes, if they sign in. Turn on a sign-in method under **Access & leads**, such as email code, phone code or Google. Signed-in visitors see their history on any device.

### Can I remove the "Powered by" badge?

There is a **Show "Powered by" badge** option on the **General** tab.

### Can an AI agent answer the chat?

Yes. [Create an agent](/agents/create-an-agent/) and turn on live chat on its **Deploy** page.

## Related

- [Connect WhatsApp](/channels/whatsapp/)
- [Reply from the inbox](/inbox/reply/)
- [Connect Shopify](/commerce/shopify/)
