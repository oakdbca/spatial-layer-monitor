"""DBCA Django Project Middleware."""


# Third-Party
from django import http

# Typing
from typing import Callable


# Type Shortcuts
GetResponseFunction = Callable[[http.HttpRequest], http.HttpResponse]


class CacheControl:
    """DBCA Cache Control Middleware."""

    def __init__(self, get_response: GetResponseFunction) -> None:
        """Instantiates the CacheControl middleware.

        Args:
            get_response (GetResponseFunction): The 'get_response' function
                injected by Django at middleware load-time.
        """
        # Set the `get_response` method.
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest) -> http.HttpResponse:
        """Handles the functionality of the middleware.

        Args:
            request (http.HttpRequest): HTTP request to handle.

        Returns:
            http.HttpResponse: The handled response.
        """
        # Retrieve the response to the request
        response = self.get_response(request)

        # Check the request path
        if request.path[:5] == "/api/":
            # Do not cache /api/ calls
            response["Cache-Control"] = "private, no-store"

        elif request.path[:8] == "/static/":
            # Cache all /static/ calls for 1 day  <-- lowered to 60 seconds for development purposes
            response["Cache-Control"] = "public, max-age=60"

        elif request.path[:7] == "/media/":
            # Cache all /media/ calls for 1 day  <-- lowered to 60 seconds for development purposes.
            response["Cache-Control"] = "public, max-age=60"

        else:
            # Ignore other paths
            pass

        # Return handled response
        return response
