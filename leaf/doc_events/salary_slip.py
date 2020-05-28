import frappe
from datetime import *

@frappe.whitelist()
def add_leave_encashment(doc, method):

    from_date = (datetime.strptime(doc.start_date, "%Y-%m-%d")).date()
    to_date = (datetime.strptime(doc.end_date, "%Y-%m-%d")).date()
    salary_structure = frappe.db.sql(""" SELECT * FROM `tabSalary Structure Assignment` WHERE salary_structure=%s and employee=%s""",(doc.salary_structure,doc.employee),as_dict=1)
    amount = 0
    leave = 0
    reg = 0
    while (from_date <= to_date):
        leave_application = get_leave_application(from_date, doc.employee)
        if len(leave_application) > 0:
            leave += 1
        else:
            reg = 0
        from_date = (from_date + timedelta(days=1))


    doc.total_leaves = leave

    remaining_leaves = int(frappe.db.sql(""" SELECT * FROM `tabEmployee` WHERE name=%s """,doc.employee,as_dict=1)[0].leave_balance)
    quarters = [{"quarter":"First Quarter", "days": 90}, {"quarter":"Second Quarter", "days": 60}, {"quarter":"Third Quarter", "days": 30}, {"quarter":"Fourth Quarter", "days": 0}]

    for i in quarters:
        if remaining_leaves > i.get("days") and leave > 0:
            leave_deduction = remaining_leaves - i.get("days") #90 - 60
            if leave_deduction >= leave:
                leave_type = get_leave_type("Sick Leave", i.get("quarter"))
                amount += ((leave_type[0].percentage / 100) * (salary_structure[0].base / 30)) * leave
                remaining_leaves = remaining_leaves - leave
                leave = 0
            else:
                leave_type = get_leave_type("Sick Leave", i.get("quarter"))
                amount += ((leave_type[0].percentage / 100) * (salary_structure[0].base / 30)) * leave_deduction
                remaining_leaves = remaining_leaves - leave
                leave -= leave_deduction
    add = True
    for ii in doc.earnings:
        if ii.__dict__['salary_component'] == "Basic":
            add = False
            ii.__dict__['amount'] = amount + ((salary_structure[0].base / 30) * reg)
    if amount > 0 and add:
        doc.append("earnings", {
            "salary_component": "Basic",
            "amount": amount + ((salary_structure[0].base / 30) * reg)
        })
    doc.remaining_leaves = remaining_leaves - leave


def update_leave_employee(leave,employee):
    frappe.db.sql(""" UPDATE tabEmployee SET leave_balance=%s WHERE name=%s""",(str(leave),employee))
    frappe.db.commit()
def get_leave_application(from_date, employee):
    query = """ SELECT * FROM `tabLeave Application` WHERE '{0}' BETWEEN from_date and to_date and employee='{1}' and status='{2}' """.format(str(from_date), employee, "Approved")
    return frappe.db.sql(query, as_dict=1)

def get_leave_balances(name):
    query = """ SELECT * FROM `tabLeave Balances` WHERE parent='{0}' ORDER BY idx DESC """.format(name)
    return frappe.db.sql(query, as_dict=1)

def get_leave_type(leave_type, quarter):
    return frappe.db.sql(""" SELECT * FROM `tabLeave Type Quarter Percentages` AS LTQP WHERE parent=%s and LTQP.type=%s""", (leave_type,quarter), as_dict=True)

def submit_salary_slip(doc, method):
    update_leave_employee(doc.remaining_leaves, doc.employee)

def cancel_salary_slip(doc, method):
    remaining_leaves = int(frappe.db.sql(""" SELECT * FROM `tabEmployee` WHERE name=%s """, doc.employee, as_dict=1)[0].leave_balance)
    update_leave_employee(remaining_leaves + doc.total_leaves, doc.employee)
