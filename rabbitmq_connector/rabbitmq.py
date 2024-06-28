import traceback

import frappe
import pika
from pika.exchange_type import ExchangeType
import json
import frappe
import ssl

def get_rabbitmq_setting():
    return frappe.get_doc("RabbitMQ Setting")



def publisher(doc_event_config, message):
    try:
        settings = get_rabbitmq_setting()
        if settings:
            message = json.dumps(message)
            # Set credentials
            # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            # ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
            url = settings.host
            parameters = pika.URLParameters(url)
            # parameters.ssl_options = pika.SSLOptions(context=ssl_context)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            # Declare exchange
            exchange = ""
            if doc_event_config.exchange:
                exchange = doc_event_config.exchange
                channel.exchange_declare(exchange=exchange, exchange_type=ExchangeType.topic)

            channel.queue_declare(queue=doc_event_config.queue_name, auto_delete=True)

            channel.basic_publish(exchange=exchange, routing_key=doc_event_config.queue_name, body=message)
            # Close connection
            connection.close()

    except Exception as e:
        traceback.print_exc()
        frappe.log_error(title="RabbitMQ Publisher Faild",message=frappe.get_traceback())
        # update_doc = Producer_log()
        # update_doc.update({"error_log":frappe.get_traceback()},p_log_name)
