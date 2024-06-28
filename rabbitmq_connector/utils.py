import frappe

def update_doc_events(doc, delete):
    existing_hooks = frappe.get_hooks("doc_events")
    doc_type = doc.doc_type
    hook = existing_hooks.get(doc_type)

    handler = "rabbitmq_connector.doc_events.producers.doc_producer"
    if doc.custom_function:
        handler = doc.custom_function

    if delete:
        if hook:
            action = hook.get(doc.trigger)
            if action:
                action.pop(handler, None)

            existing_hooks[doc_type][doc.trigger] = action
    else:
        if hook:
            action = hook.get(doc.trigger)
            if action:
                if handler not in action:
                    action.append(handler)

            existing_hooks[doc_type][doc.trigger] = action

        else:
            existing_hooks[doc_type] = {
                doc.trigger: [handler]
            }
    frappe.get_hooks("doc_events").update(existing_hooks)
    frappe.cache().delete_value("app_hooks")


def initial_producers(doc_events):
    producers = frappe.db.get_list('Producers', pluck='name')
    for producer_name in producers:
        doc = frappe.get_doc("Producers", producer_name)
        doc_type = doc.doc_type
        hook = doc_events.get(doc_type)

        handler = "rabbitmq_connector.doc_events.producers.doc_producer"
        if doc.custom_function:
            handler = doc.custom_function

        if hook:
            action = hook.get(doc.trigger)
            if action:
                if handler not in action:
                    action.append(handler)

            doc_events[doc_type][doc.trigger] = action

        else:
            doc_events[doc_type] = {
                doc.trigger: [handler]
            }

        print(f"Update doc event {producer_name}")
