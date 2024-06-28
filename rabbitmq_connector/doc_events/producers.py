import frappe
import requests

from rabbitmq_connector.rabbitmq import publisher

def doc_producer(doc, method):
    message = doc.as_dict()

    list_config = frappe.db.get_list("Producers", filters={"doc_type": "Customer", "trigger": method})
    if not list_config:
        return

    producer_config = frappe.get_doc("Producers", list_config[0]["name"])
    if not producer_config:
        return

    payload = {
        "queue": producer_config.doc_type,
        "data": message
    }

    publisher(producer_config, payload)
    frappe.msgprint("Task {} has been updated!".format(doc.name))
