---
title: Use Fufa MCP from other clients
description: Connect Claude Code, Cursor, VS Code or your own code to the Fufa MCP server with an MCP API key, and work in your Fufa workspace from there.
sidebar:
  order: 3
---

Claude Code, Cursor, VS Code or your own code can connect to your Fufa workspace through the Fufa MCP server. Once connected, they can use the same tools as Claude chat: read and update agents, conversations, contacts, campaigns, workflows and reports.

These clients sign in with an MCP API key instead of your Fufa password. Setup takes a few minutes once you have the key.

## Before you start

- A Fufa account. The key acts as you, so the client can do only what your role in the workspace allows.
- An MCP API key. You can't create keys in Fufa yet, so email team@fufa.ai from your registered email address and ask for an MCP API key. Keys start with `fufa_`.
- The Fufa MCP server URL: `https://api.fufa.ai/v1/merchant/mcp`

:::caution
Treat the key like a password. Anyone who has it can work in your workspace as you. Don't commit it to a repository or paste it into a shared chat.
:::

## How the connection works

Every client needs the same two things:

- **URL**: `https://api.fufa.ai/v1/merchant/mcp`, using the Streamable HTTP transport.
- **Header**: `Authorization: Bearer fufa_your_key`, with your own key in place of `fufa_your_key`.

Any MCP client that can send a header with a remote server works. The sections below show the setup for common clients.

## Connect Claude Code

1. In a terminal, run this command with your own key:

   ```bash
   claude mcp add --transport http fufa https://api.fufa.ai/v1/merchant/mcp --header "Authorization: Bearer fufa_your_key"
   ```

2. Start Claude Code and run `/mcp`. **fufa** shows as connected, with its tools listed.

Add `--scope user` to the command to use Fufa in every project, not only the current one.

## Connect Cursor

1. Open `~/.cursor/mcp.json`, or create it, and add Fufa under `mcpServers`:

   ```json
   {
     "mcpServers": {
       "fufa": {
         "url": "https://api.fufa.ai/v1/merchant/mcp",
         "headers": { "Authorization": "Bearer fufa_your_key" }
       }
     }
   }
   ```

2. Open Cursor's settings, go to the MCP section, and check that **fufa** is on and lists its tools.

## Connect VS Code

1. Open `.vscode/mcp.json` in your project, or create it, and add Fufa under `servers`:

   ```json
   {
     "servers": {
       "fufa": {
         "type": "http",
         "url": "https://api.fufa.ai/v1/merchant/mcp",
         "headers": { "Authorization": "Bearer fufa_your_key" }
       }
     }
   }
   ```

2. Click **Start** above the server entry in the file, then open Copilot Chat in agent mode and pick the Fufa tools from the tools list.

If the project is shared, don't put the key in `.vscode/mcp.json`. Use VS Code's input variables so each person is asked for their own key.

## Connect from your own code

Use any MCP client library. With the official TypeScript SDK:

```ts
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';

const transport = new StreamableHTTPClientTransport(
  new URL('https://api.fufa.ai/v1/merchant/mcp'),
  { requestInit: { headers: { Authorization: `Bearer ${process.env.FUFA_MCP_KEY}` } } },
);
const client = new Client({ name: 'my-app', version: '1.0.0' });
await client.connect(transport);

const workspaces = await client.callTool({ name: 'organization_list', arguments: {} });
console.log(workspaces.content);
```

Each tool returns its result as JSON text. A failed call returns `isError: true` with an `error` message. See [What you can do with Fufa MCP](/mcp/tools/) for every tool.

## Check it works

Ask the client "Which Fufa workspaces do I belong to, and which one is active?" It calls `organization_list` and answers with your workspaces. If you belong to more than one, ask it to switch to the one you want before you start.

## Common questions

### How do I get an MCP API key?

Email team@fufa.ai from the email address you use to sign in to Fufa and ask for an MCP API key. You can't create keys in the Fufa app yet.

### Do I need an API key to use Fufa in Claude chat?

No. Claude on claude.ai and the Claude desktop app sign in with your Fufa account instead. See [Connect Fufa to Claude](/mcp/claude-connector/).

### What can a client do with my API key?

Everything your role in the workspace allows, through the tools listed in [What you can do with Fufa MCP](/mcp/tools/). The key acts as you, so its access changes when your role changes.

### Why does the client say "Missing bearer token"?

The client didn't send the `Authorization` header. Check that the header is spelled exactly `Authorization: Bearer fufa_your_key`, with one space after `Bearer`, and restart the client.

### What do I do if my API key leaks?

Email team@fufa.ai from your registered email address straight away and ask for the key to be revoked and replaced.

## Related

- [What you can do with Fufa MCP](/mcp/tools/)
- [Connect Fufa to Claude](/mcp/claude-connector/)
- [Things to ask Fufa MCP](/mcp/examples/)
