#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from kytos.core import KytosEvent, KytosNApp, log
from kytos.core.helpers import listen_to
from napps.viniciusarcanjo.kyslacker import settings


class Main(KytosNApp):
    """Main class of a KytosNApp"""

    def setup(self):
        """ Init slacker object

        """
        self.has_failed = False
        try:
            from slacker import Slacker
            if not settings.token:
                self.has_failed = True
                log.error("Please, set the token variable in settings.py")
                log.error("kyslacker will shut down")
            else:
                self.slack = Slacker(settings.token)
        except ImportError as e:
            log.error(
                "Package slacker inst't installed. Please, pip install slacker"
            )

    def execute(self):
        "This NApp is event-oriented"

        # Token settings, auto shutdown.
        if self.has_failed:
            self.controller.unload_napp(self.username, self.name)
        pass

    def _parse_str(self, str1, msg):
        """ Check if msg is a string and concatenate to str1

        :str1: base string
        :msg: string to be concatenated
        :returns: str1 + msg

        """
        if isinstance(msg, str):
            return str1 + " " + msg
        # Otherwise just return the base string
        return str1

    @listen_to('viniciusarcanjo/kyslacker.send')
    def send(self, event):
        """Listen to KytosEvent 'kyslacker.send' parse it and send it via slacker

        Here's a simple snippet to send a event and the expected dict keys:

        event = KytosEvent(name='viniciusarcanjo/kyslacker.send')
        d = {
            'channel': 'of_notifications',
            'source': '{0}/{1}'.format(self.username, self.name),
            'tag': 'INFO',
            'payload': 'L2circuit X was provisioned for customer A'
        }
        event.content['message'] = d
        self.controller.buffers.app.put(event)

        # 'channel' is the slack channel, by default it's #general
        # 'source' is the NApp username/name that fired the event
        # 'tag' is a string to prefix the 'payload'
        # 'payload' is a string that will be sent

        :event: KytosEvent

        """

        try:
            # if settings wasn't properly setup in the first place
            if not self.has_failed:
                d = event.content.get('message')
                if d:
                    if not isinstance(d, dict):
                        log.error(
                            "The object in KytosEvent.content.message isn't a dict!"
                        )
                        return
                    slack_msg = ""
                    for k in ['source', 'tag', 'payload']:
                        slack_msg = self._parse_str(slack_msg, d.get(k))
                    # only sends if it's not empty.
                    if slack_msg:
                        # fallback to #general
                        ch = d.get('channel') if d.get(
                            'channel') else '#general'
                        log.info('channel:{0} msg:{1}'.format(ch, slack_msg))
                        self.slack.chat.post_message(ch, slack_msg)
        except requests.exceptions.ConnectionError as e:
            log.error(
                "ConnectionError to Slack API. Make sure you are connected and can reach Slack API."
            )

    def shutdown(self):
        """Too simple to have a shutdown procedure."""
        log.info("kyslacker's gone!")
        pass
