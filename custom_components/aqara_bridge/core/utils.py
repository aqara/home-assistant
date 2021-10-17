""" the Aqara Bridge utils."""
import logging
import re
import uuid
from datetime import datetime
from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from homeassistant.helpers.typing import HomeAssistantType


TITLE = "Aqara Bridge Debug"
NOTIFY_TEXT = '<a href="%s?r=10" target="_blank">Open Log<a>'
HTML = (f'<!DOCTYPE html><html><head><title>{TITLE}</title>'
        '<meta http-equiv="refresh" content="%s"></head>'
        '<body><pre>%s</pre></body></html>')

# These code are reference to @AlexxIT. It is very useful to help debug.
class AqaraBridgeDebug(logging.Handler, HomeAssistantView):
    # pylint: disable=abstract-method, arguments-differ
    """ debug handler """
    name = "bridge_debug"
    requires_auth = False

    text = ''

    def __init__(self, hass: HomeAssistantType):
        super().__init__()

        # random url because without authorization!!!
        self.url = "/{}".format(uuid.uuid4())

        hass.http.register_view(self)
        hass.components.persistent_notification.async_create(
            NOTIFY_TEXT % self.url, title=TITLE)

    def handle(self, rec: logging.LogRecord) -> None:
        date_time = datetime.fromtimestamp(rec.created).strftime(
            "%Y-%m-%d %H:%M:%S")
        module = 'main' if rec.module == '__init__' else rec.module
        self.text = "{} {}  {}  {}  {}\n".format(
            self.text, date_time, rec.levelname, module, rec.msg)

    async def get(self, request: web.Request):
        """ for shortcut """
        try:
            if 'c' in request.query:
                self.text = ''

            if 'q' in request.query or 't' in request.query:
                lines = self.text.split('\n')

                if 'q' in request.query:
                    reg = re.compile(fr"({request.query['q']})", re.IGNORECASE)
                    lines = [p for p in lines if reg.search(p)]

                if 't' in request.query:
                    tail = int(request.query['t'])
                    lines = lines[-tail:]

                body = '\n'.join(lines)
            else:
                body = self.text

            reload = request.query.get('r', '')
            return web.Response(text=HTML % (reload, body),
                                content_type="text/html")

        except Exception:
            return web.Response(status=500)
