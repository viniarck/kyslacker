kyslacker
=========

Kytos meets Slack, for your notification/automation needs! This NApp sends Slack notifications via slacker. Essentially, kyslacker is just a wrapper around slacker by leveraging Kytos NApp's messaging queues. As a result, kyslacker provides you a simple and common interface for Slack, which becomes even more important when you have several NApps. Also, kyslacker keeps all Slack dependencies in this package (NApp), so you don't have to keep installing dependencies in other NApps.


User Stories
============

- Multiple Kytos NApps want to send a Slack message to a specific Slack channel via KytosEvent.
- Multiple Kytos NApps want to be able add other extra information such as NApp that originated the message, tags, and the content of the Slack message itself.
- User A wants to have access to one Slack bot.


Requirements
============

pip3 install -r requirements.txt


How to use this NApp
====================

First of all, you need kytos SDN platform up and running and then:

1. pip3 install -r requirements.txt
2. kytos napps install viniciusarcanjo/kyslacker
3. kytos napps enable viniciusarcanjo/kyslacker
4. Set your Slack's bot's API token in settings.py. If you don't have a token yet, check this `link <https://my.slack.com/services/new/bot>`_
5. Start coding your NApp that will send messages (KytosEvent) to kyslacker

Coding your client NApp
=======================

The simplest snippet looks like this:

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

If you want to prototype quickly with the above snippet and you don't have a base NApp yet, I recommend you pull this sample client application that I published on kytos napps repos:

.. code-block:: shell

  kytos napps install viniciusarcanjo/kyslacker-client
  kytos napps enable viniciusarcanjo/kyslacker-client

Go to kytos napps dir and start hacking!

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
