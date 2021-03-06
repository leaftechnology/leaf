import frappe

def update_employee_leave(doc, method):
    leave_type = frappe.db.sql(""" SELECT * FROM `tabLeave Type` WHERE name=%s""", doc.leave_type,as_dict=1)
    if leave_type[0].enable_percentages:
        frappe.db.sql(""" UPDATE tabEmployee SET leave_balance=%s WHERE name=%s """,(doc.total_leaves_allocated,doc.employee))
        frappe.db.commit()


def cancel_employee_leave(doc, method):
    leave_type = frappe.db.sql(""" SELECT * FROM `tabLeave Type` WHERE name=%s""", doc.leave_type,as_dict=1)
    if leave_type[0].enable_percentages:
        employee = frappe.db.sql(""" SELECT * FROM `tabEmployee` WHERE name=%s """,(doc.employee),as_dict=1)
        new_leave = employee[0].leave_balance
        if int(employee[0].leave_balance) > 0:
            new_leave = int(employee[0].leave_balance) - int(doc.total_leaves_allocated) if int(employee[0].leave_balance) - int(doc.total_leaves_allocated) > 0 else 0
        frappe.db.sql(""" UPDATE tabEmployee SET leave_balance=%s WHERE name=%s """,(str(new_leave),doc.employee))
        frappe.db.commit()