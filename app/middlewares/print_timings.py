from timing_asgi import TimingClient, TimingMiddleware
from timing_asgi.integrations import StarletteScopeToName


class PrintTimings(TimingClient):
    def timing(self, metric_name, timing, tags):
        print(metric_name, timing, tags)


class PrintTimingsMiddleware(object):
    def __init__(self, app):
        app.add_middleware(
            TimingMiddleware,
            client=PrintTimings(),
            metric_namer=StarletteScopeToName(
                prefix="fastpi",
                starlette_app=app
            )
        )
