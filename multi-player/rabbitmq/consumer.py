import json
import sys
import os
import pika
"""
Consumes the messages from the queue, it is redundant if the socket server is ran.
"""


def callback(ch, method, properties, body):
    print(f"Message Received: {json.loads(body)}")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare('games_stats')
    channel.basic_consume(queue='games_stats', auto_ack=True , on_message_callback=callback)

    print("Connection established. Waiting for messages. Press CTRL+C to interrupt.")
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)