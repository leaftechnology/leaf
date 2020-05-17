

cur_frm.cscript.employee = function () {
    set_new_leaves_allocated(cur_frm)
}
cur_frm.cscript.leave_type = function () {
    set_new_leaves_allocated(cur_frm)

}
cur_frm.cscript.to_date = function () {
    set_new_leaves_allocated(cur_frm)

}
cur_frm.cscript.from_date = function () {
    set_new_leaves_allocated(cur_frm)

}

function set_new_leaves_allocated(cur_frm) {
    if (cur_frm.doc.employee && cur_frm.doc.leave_type && cur_frm.doc.to_date){
       frappe.call({
           method: "frappe.client.get_value",
           args: {
               "doctype":"Leave Type",
               "filters": {
                   "name": cur_frm.doc.leave_type
               },
               "fieldname": "*"
           },
           callback: function (r) {
               if (r.message.max_leaves_allowed && r.message.enable_percentages) {
                   cur_frm.doc.new_leaves_allocated = r.message.max_leaves_allowed
                   cur_frm.doc.total_leaves_allocated = r.message.max_leaves_allowed
                   cur_frm.refresh_field("new_leaves_allocated")
                   cur_frm.refresh_field("total_leaves_allocated")
               }
           }
       })
    }
}
