from fastmcp.server.middleware import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        print(f"Processing {context.method} from {context.source}")
        
        try:
            result = await call_next(context)
            print(f"Completed {context.method}")
            return result
        except Exception as e:
            print(f"Failed {context.method}: {e}")
            raise