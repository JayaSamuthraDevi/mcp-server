from fastmcp.server.middleware import Middleware, MiddlewareContext
import json
import logging

logger = logging.getLogger("mcp")

class LoggingMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        # Safe fields ONLY
        safe_log = {
            "event": "request_received",
            "method": context.method,
            "source": context.source,
        }
        logger.info(json.dumps(safe_log))

        try:
            result = await call_next(context)

            logger.info(json.dumps({
                "event": "request_completed",
                "method": context.method
            }))
            return result

        except Exception as e:
            logger.error(json.dumps({
                "event": "request_failed",
                "method": context.method,
                "error": str(e)
            }))
            raise
