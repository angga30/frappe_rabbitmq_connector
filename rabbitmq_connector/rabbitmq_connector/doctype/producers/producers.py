# Copyright (c) 2024, Prabunesia Teknodata and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from rabbitmq_connector.utils import update_doc_events


class Producers(Document):

    def on_update(self):
        frappe.msgprint("Task {} has been update iiii!".format(self.name))
        self.update_hooks()

    def on_delete(self):
        frappe.msgprint("Task {} has been delete xxxx!".format(self.name))
        self.update_hooks(delete=True)

    def update_hooks(self, delete=False):
        update_doc_events(self, delete)




