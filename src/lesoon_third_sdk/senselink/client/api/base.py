import typing as t


class SenseLinkBaseAPI:
    API_BASE_URL: t.Optional[str] = None

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, params=None, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, params, **kwargs)

    def _post(self, url, data=None, params=None, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, data, params, **kwargs)
