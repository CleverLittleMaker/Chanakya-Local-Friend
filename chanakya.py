import nest_asyncio
nest_asyncio.apply()

import asyncio
import os
import threading

# Import from the new modular structure
from chanakya_app.app_setup import app
from chanakya_app.memory_management import create_table
from chanakya_app.tool_loader import load_all_mcp_tools_async
from chanakya_app.routes import background_thread
# This import is necessary to register the routes
from chanakya_app import routes

if __name__ == "__main__":
    create_table()

    app.logger.info("Attempting to load MCP tools at startup (async via asyncio.run)...")
    try:
        asyncio.run(load_all_mcp_tools_async())
    except RuntimeError as e:
        if "cannot run nested Nests" in str(e).lower() or "event loop is already running" in str(e).lower() or "Event loop is closed" in str(e).lower():
            app.logger.warning(f"Asyncio.run for load_all_mcp_tools_async issue ({e}). Nest_asyncio should handle loop management.")
            try:
                loop = asyncio.get_event_loop()
                if not loop.is_running():
                    loop.run_until_complete(load_all_mcp_tools_async())
                else:
                    app.logger.info("Event loop already running; assuming nest_asyncio allows tool loading or it occurred.")
            except Exception as loop_e:
                 app.logger.error(f"Fallback loop execution for tool loading failed: {loop_e}", exc_info=True)
        else:
            app.logger.error(f"Unexpected RuntimeError during startup tool loading: {e}", exc_info=True)
            raise
    except Exception as e:
        app.logger.error(f"Failed to load tools at startup: {e}", exc_info=True)

    activity_thread = threading.Thread(target=background_thread, daemon=True)
    activity_thread.start()

    # --- SSL/HTTPS Configuration ---
    cert_file = 'certs/cert.pem'
    key_file = 'certs/key.pem'
    ssl_context = None
    if os.path.exists(cert_file) and os.path.exists(key_file):
        app.logger.info(f"Found certificate and key. Starting with HTTPS.")
        ssl_context = (cert_file, key_file)
    else:
        app.logger.info(f"Certificate and key not found. Starting with HTTP.")

    app.logger.info("Starting Chanakya Flask app (ReAct Agent, Async Routes, Per-Request LLM/Agent, Merged Tools, nest_asyncio)...")
    app.run(host='0.0.0.0', port=5001, use_reloader=True, ssl_context=ssl_context)