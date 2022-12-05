import pika
import json
import service_db.database


def sender(payload):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # Connect to CloudAMQP
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue='appeals')  # Declare a queue
    # send a message
    channel.basic_publish(exchange='', routing_key='appeals', body=payload)
    print("[x] Message sent to consumer")
    connection.close()


def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='appeals')

    def callback(ch, method, properties, body):
        msg_dict = json.loads(body)
        service_db.database.write_user(msg_dict['name'],
                                       msg_dict['surname'],
                                       msg_dict['patronymic'],
                                       msg_dict['phone'],
                                       msg_dict['appeal'])

    channel.basic_consume('appeals', callback, auto_ack=True)
    channel.start_consuming()
    connection.close()