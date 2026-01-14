"""
Example FGP Python module demonstrating the interface.

This module can be loaded by an FGP daemon using the PythonModule wrapper.

Usage:
    from fgp_daemon import PythonModule, FgpServer

    module = PythonModule::load("examples/python_module.py", "EchoModule")
    server = FgpServer::new(module, "~/.fgp/services/echo/daemon.sock")
    server.serve()
"""


class EchoModule:
    """A simple echo service for testing Python module integration."""

    # Required: Service name (used in socket path and method routing)
    name = "echo"

    # Required: Service version (semver format)
    version = "1.0.0"

    def __init__(self):
        """Initialize the module. Called once when the module is loaded."""
        self._request_count = 0

    def dispatch(self, method: str, params: dict) -> dict:
        """
        Handle a method call.

        Args:
            method: Fully-qualified method name (e.g., "echo.ping")
            params: Method parameters as a dictionary

        Returns:
            dict: Result to send back to the client

        Raises:
            ValueError: If the method is unknown
            Exception: Any exception is converted to an error response
        """
        self._request_count += 1

        if method == "echo.ping":
            return {"pong": True, "count": self._request_count}

        elif method == "echo.echo":
            return {"echo": params}

        elif method == "echo.reverse":
            text = params.get("text", "")
            return {"reversed": text[::-1]}

        elif method == "echo.add":
            a = params.get("a", 0)
            b = params.get("b", 0)
            return {"result": a + b}

        elif method == "echo.error":
            # Demonstrate error handling
            raise ValueError("This is a test error")

        else:
            raise ValueError(f"Unknown method: {method}")

    def method_list(self) -> list:
        """
        Return list of available methods with documentation.

        Optional: If not implemented, returns empty list.

        Returns:
            list: List of method info dictionaries with keys:
                - name: Method name
                - description: Human-readable description
                - params: List of parameter info dicts (optional)
        """
        return [
            {
                "name": "echo.ping",
                "description": "Simple health check - returns pong",
                "params": []
            },
            {
                "name": "echo.echo",
                "description": "Echo back the input parameters",
                "params": [
                    {"name": "any", "type": "object", "required": False}
                ]
            },
            {
                "name": "echo.reverse",
                "description": "Reverse a text string",
                "params": [
                    {"name": "text", "type": "string", "required": True}
                ]
            },
            {
                "name": "echo.add",
                "description": "Add two numbers",
                "params": [
                    {"name": "a", "type": "number", "required": True},
                    {"name": "b", "type": "number", "required": True}
                ]
            },
            {
                "name": "echo.error",
                "description": "Test error handling",
                "params": []
            }
        ]

    def on_start(self):
        """
        Called when the daemon starts.

        Optional: If not implemented, no action taken.
        Use for initialization (open database connections, etc.)
        """
        print(f"[{self.name}] Module starting...")

    def on_stop(self):
        """
        Called when the daemon is stopping.

        Optional: If not implemented, no action taken.
        Use for cleanup (close connections, flush caches, etc.)
        """
        print(f"[{self.name}] Module stopping... (handled {self._request_count} requests)")

    def health_check(self) -> dict:
        """
        Return health status for dependencies.

        Optional: If not implemented, returns empty dict.

        Returns:
            dict: Mapping of dependency name to status dict with keys:
                - ok: boolean (healthy or not)
                - latency_ms: float (optional)
                - message: string (optional)
        """
        return {
            "python": {
                "ok": True,
                "message": f"Handled {self._request_count} requests"
            }
        }


# You can also define the module class as "Module" for auto-loading
Module = EchoModule
