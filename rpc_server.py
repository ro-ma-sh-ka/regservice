import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='rpc_queue')

    def on_request(ch, method, props, body):
        # здесь отправляем в фастапи (потребителю, консьюмеру
        print(" [.] %s, ты молодец!?" % body)

    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request, auto_ack=True)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
