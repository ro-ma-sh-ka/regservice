import pika
import json
import service_db.database


def sender(payload):
    """sender is a method to receive a user message from tornado server and send it to a rabbitmq queue"""
    # connect to rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # crate a channel
    channel = connection.channel()
    # declare a queue
    channel.queue_declare(queue='appeals')
    # send a message to the appeals queue
    channel.basic_publish(exchange='', routing_key='appeals', body=payload)
    # report we have sent the message
    print("[x] Message sent to consumer")
    # close the connection
    connection.close()


def consumer():
    """consumer is a method to listen to the queue appeals"""
    # connect to rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # crate a channel
    channel = connection.channel()
    # declare a queue
    channel.queue_declare(queue='appeals')

    def callback(ch, method, properties, body):
        """callback function convert the user data from json to dictionary
            and upload it to users table by write_user method.
            There is write_appeal method which save appeal to appeals table
        """
        msg_dict = json.loads(body)
        service_db.database.write_user(msg_dict['name'],
                                       msg_dict['surname'],
                                       msg_dict['patronymic'],
                                       msg_dict['phone'],
                                       msg_dict['appeal'])
#        return body
    # define listening to appeals queue. In case of message call callback method
    channel.basic_consume('appeals', callback, auto_ack=True)
    # start listening
    channel.start_consuming()
    # close connection
    connection.close()

#    return callback()


if __name__ == '__main__':
    consumer()
