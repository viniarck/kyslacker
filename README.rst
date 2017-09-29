kyslacker
=========

Kytos meets Slack, for your notification/automation needs! This NApp sends Slack notifications via slacker. Essentially, kyslacker is just a wrapper around slacker.


You have two interfaces to send messages either via:

1. Kytos NApp's native messaging queue
2. REST API, `/api/viniciusarcanjo/kyslacker/send` endpoint

As a result, kyslacker provides you a simple and common interface for Slack, which becomes even more important when you have several NApps and Apps that integrate with your network. Also, kyslacker keeps all Slack dependencies in this package (NApp), so you don't have to keep installing dependencies in other NApps.


User Stories
============

- Multiple Kytos NApps want to send a message to a specific Slack channel via KytosEvent.
- Multiple Kytos NApps want to be able add other extra information such as NApp that originated the message, tags, and the content of the Slack message itself.
- User A wants to have access to one Slack bot.
- Another App wants to send a message to a specific Slack channel via a REST API.


Requirements
============

pip3 install -r requirements.txt


How to use this NApp
====================

First of all, you need kytos SDN platform up and running and then:

1. pip3.6 install -r requirements.txt
2. kytos napps install viniciusarcanjo/kyslacker
3. kytos napps enable viniciusarcanjo/kyslacker
4. Set your Slack's bot's API token in settings.py. If you don't have a token yet, check this `link <https://my.slack.com/services/new/bot>`_

Then, you have two options:

Option 1 - Coding your client Kytos NApp
========================================

The simplest snippet looks like this to send messages via KytosEvent:

.. code-block:: python

  def execute(self):
      "KytosNApp execute"
      event = KytosEvent(name='viniciusarcanjo/kyslacker.send')
      d = {
          'channel': 'of_notifications',
          'source': '{0}/{1}'.format(self.username, self.name),
          'tag': 'INFO',
          'payload': 'L2circuit X was provisioned for customer A'
      }
      event.content['message'] = d
      log.info('sending message to kyslacker...')
      self.controller.buffers.app.put(event)

If you want to prototype quickly with the above snippet and you don't have a base NApp yet, I recommend you pull this sample client `application <https://www.github.com/viniciusarcanjo/kyslacker-client>`_ that I published on kytos napps repos:

.. code-block:: shell

  kytos napps install viniciusarcanjo/kyslacker_client
  kytos napps enable viniciusarcanjo/kyslacker_client

Go to kytos napps dir and start hacking!

Option 2 - REST POST Call
=========================

If for some reason, you have other APPs that integrate with the network either via other controllers or other external interfaces, you won't be able to leverage KytosEvent, which is why this REST POST endpoint `/api/viniciusarcanjo/kyslacker/send` is available. To send a message, just send a json on this endpoint:

.. code-block:: json

  {
    "channel": "of_notifications",
    "source": "api-client",
    "tag": "INFO",
    "payload": "L2circuit Y was provisioned for customer B"
  }

If this json data is written on a `msg.json` file you can test it with curl:

.. code-block:: shell

   curl -X POST -d@msg.json -H "Content-Type: application/json" localhost:8181/api/viniciusarcanjo/kyslacker/send

FAQ
===

1 - How to run kytos SDN platform?

`Kytos SDN Platform <https://www.kytos.io>`_

You can find plenty of information on this link.

2 - How to create your Slack bot?

`Slack bot <https://my.slack.com/services/new/bot>`_

Roadmap
=======

- I am still experimenting with this library.
- I will add more slack bots and tokens, if necessary. But so far, just one bot has been enough for my use cases since one bot can post to multiple channels.
