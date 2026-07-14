from .base import BaseBackend


class DummyBackend(BaseBackend):
    def __init__(self, params):
        super().__init__(params)

        self.urls = []

    def purge(self, url) -> None:
        self.urls.append(url)
