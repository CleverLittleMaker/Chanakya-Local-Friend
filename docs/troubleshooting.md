# Troubleshooting

This page lists common issues you might encounter while setting up or running Chanakya and how to solve them.

## Python and Server Errors

**Error: `NameError: app is not defined`**
- **Cause:** This can happen if `app = Flask(__name__)` is defined after it's being used by other parts of the code at the global scope, like `app.logger`.
- **Solution:** Ensure that `app = Flask(__name__)` is one of the first lines after the imports in `chanakya.py`.

**Error: `Event loop is closed`**
- **Cause:** This is a common issue when using `asyncio` with frameworks like Flask that may not be natively async.
- **Solution:** The `chanakya.py` file should start with `import nest_asyncio; nest_asyncio.apply()`. This patch allows the `asyncio` event loop to be nested, which is required for the way Flask and the async libraries interact. Also, ensure Flask is installed with async support: `pip install "flask[async]"`.

**Error: `httpx.UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol.`**
- **Cause:** One of the URLs in your `.env` file is missing the protocol prefix.
- **Solution:** Double-check your `OLLAMA_ENDPOINT`, `OLLAMA_ENDPOINT_SMALL`, `STT_SERVER_URL`, and `TTS_SERVER_URL` in your `.env` file. They **must** start with `http://` or `https://` and should not have extra quotes around the value.

**Error: `Tool Errors (e.g., "Invalid arguments for tool_name")`**
- **Cause:** The LLM is trying to call a tool with incorrect arguments.
- **Solution:**
  1.  Check the server logs (with `verbose=True` for the agent in `chanakya.py`) to see the exact arguments the LLM tried to use.
  2.  Verify that the tool's description in the system prompt accurately reflects its expected arguments.
  3.  Check the MCP tool server itself to confirm its input schema.

**Error: `ACCUWEATHER_API_KEY environment variable is required` (or similar for other tools)**
- **Cause:** An API key or other required environment variable for an MCP tool is missing.
- **Solution:**
  1.  Open your `mcp_config_file.json`.
  2.  Find the configuration for the tool that's causing the error.
  3.  Ensure the `env` block is correctly defined and contains the required key-value pair (e.g., `"ACCUWEATHER_API_KEY": "YOUR_KEY_HERE"`).

**Error: `500 Internal Server Error` during a query**
- **Cause:** This can be a generic error, but it often happens due to intermittent issues. It could be related to the LLM generating an incorrect tool call that the system can't parse, or a temporary asynchronous processing hiccup.
- **Solution:** In many cases, simply retrying the same query will resolve the issue. If the error persists for a specific query, check the `chanakya.log` file for more detailed error messages.

## Docker and Networking Errors

**Error: Cannot connect to Ollama/STT/TTS from the Chanakya Docker container.**
- **Cause:** The Chanakya container cannot reach the other services on the network.
- **Solution:**
  -   **Use `--network="host"`:** This is the simplest solution. When you run the Chanakya Docker container, use the `--network="host"` flag. This makes the container share the host's network, and you can use `http://localhost:<PORT>` in your `.env` file to refer to services running on the same machine.
  -   **Without `--network="host"`:** If you are not using host networking (e.g., you are on a default bridge network), you may need to use `http://host.docker.internal:<PORT>` (on Docker Desktop for Mac/Windows) or the IP address of the `docker0` bridge on Linux to connect to services running on the host.

## Microphone and Audio Issues (Browser)

**Problem: The microphone is not working.**
- **Cause:** The browser does not have permission to access the microphone, or the connection is not secure.
- **Solution:**
  1.  **Use HTTPS:** Modern browsers require a secure (HTTPS) connection to allow microphone access. See the [Deployment](./deployment.md) guide for instructions on setting up HTTPS.
  2.  **Grant Permissions:** When you first visit the page, your browser should prompt you for microphone permission. Make sure you click "Allow". If you accidentally clicked "Block", you will need to go into your browser's site settings for the Chanakya URL and change the microphone permission to "Allow".
  3.  **Unlock Audio:** Browsers require a user interaction (like a click or keypress) on the page before they will allow audio to be played or recorded. Click anywhere on the page first.
  4.  **Check Browser Console:** Open your browser's developer tools (usually by pressing F12) and check the "Console" tab for any JavaScript errors. These can often provide clues about what's going wrong.
