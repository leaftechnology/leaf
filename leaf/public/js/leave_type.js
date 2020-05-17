

cur_frm.cscript.enable_percentages = function () {
    var quarters = ['First Quarter','Second Quarter','Third Quarter','Fourth Quarter']
    var percentages = ['100','75','75','0']
    if (cur_frm.doc.enable_percentages && cur_frm.doc.percentage_table.length === 0) {
        for(var quarter=0;quarter<quarters.length;quarter+=1){
        var row = cur_frm.add_child("percentage_table")
         row.type = quarters[quarter]
         row.number_of_days = cur_frm.doc.max_leaves_allowed / 4
         row.percentage = percentages[quarter]
            cur_frm.refresh_field("percentage_table")
        }
    }
}