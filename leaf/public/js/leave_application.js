



cur_frm.cscript.get_leave_balances = function () {
    cur_frm.clear_table("leaves_per_quarter")
    cur_frm.refresh_field("leaves_per_quarter")
    frappe.call({
        method: "frappe.client.get_value",
        args:{
            "doctype": "Leave Type",
            "filters": {
                "name": cur_frm.doc.leave_type
            },
            "fieldname": "enable_percentages"
        },
        callback: function (r) {
            if(r.message.enable_percentages){
                get_leaves(cur_frm)
                if (cur_frm.doc.leaves_per_quarter.length > 0) {
                    set_pending_leaves(cur_frm)
                }
            } else {
                frappe.msgprint("Percentages is disabled")
            }
        }
    })
}

function get_leaves(cur_frm) {
    if(cur_frm.doc.employee && cur_frm.doc.leave_type && cur_frm.doc.from_date && cur_frm.doc.to_date){
        var total_balance =  cur_frm.doc.leave_balance
        var count = 0
        var quarters = [
            "Fourth Quarter",
            "Third Quarter",
            "Second Quarter",
            "First Quarter", ]
        while(total_balance >= 30) {
            var row = cur_frm.add_child("leaves_per_quarter")
            row.quarter = quarters[count]
            row.leave_allocated = 30
            row.leave_balance = 30
            total_balance -= 30
            count += 1
            cur_frm.refresh_field("leaves_per_quarter")
        }

        if (total_balance < 30 && total_balance > 0) {
            var row1 = cur_frm.add_child("leaves_per_quarter")
            row1.quarter = quarters[count]
            row1.leave_allocated = 30
            row1.leave_balance = total_balance
            total_balance = 0
            count += 1
            cur_frm.refresh_field("leaves_per_quarter")

        }

        while (total_balance === 0 && count < 4) {
             var row2 = cur_frm.add_child("leaves_per_quarter")
            row2.quarter = quarters[count]
            row2.leave_allocated = 30
            row2.leave_balance = 0
            count += 1
            cur_frm.refresh_field("leaves_per_quarter")

        }
    }
}

function set_pending_leaves(cur_frm) {
    var number_of_leaves = cur_frm.doc.total_leave_days
    for(var i = cur_frm.doc.leaves_per_quarter.length - 1; i > 0;i -= 1){
        var leave_balance = cur_frm.doc.leaves_per_quarter[i]

        if(leave_balance.leave_balance > 0 && number_of_leaves <= leave_balance.leave_balance){
            leave_balance.leave_balance = leave_balance.leave_balance - number_of_leaves
            leave_balance.no_salary_yet = number_of_leaves
            cur_frm.refresh_field("leaves_per_quarter")
            number_of_leaves -= number_of_leaves
        } else if (leave_balance.leave_balance > 0 && number_of_leaves >= leave_balance.leave_balance) {
            number_of_leaves -= leave_balance.leave_balance
            leave_balance.no_salary_yet = leave_balance.leave_balance
            leave_balance.leave_balance = 0
            cur_frm.refresh_field("leaves_per_quarter")
        }
    }
}