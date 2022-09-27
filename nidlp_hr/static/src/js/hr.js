odoo.define("nidlp_hr.payslip.tree", function (require) {
    "use strict";
    var PayslipListController = require("hr_payroll.payslip.tree");
    var core = require("web.core");

    var QWeb = core.qweb;
    var PaylsipExtra = PayslipListController.include({
        renderButtons: function () {
            this._super.apply(this, arguments);
            this.$buttons.append($(QWeb.render("PayslipListView.print_wps_button", this)));
            var self = this;
            this.$buttons.on("click", ".o_button_print_wps", function () {
                if (self.getSelectedIds().length == 0) {
                    return;
                }
                return self
                    ._rpc({
                        model: "hr.payslip",
                        method: "action_print_wps",
                        args: [self.getSelectedIds()],
                    })
                    .then(function (results) {
                        self.do_action(results);
                    });
            });
        },
    });
    return PaylsipExtra;
});
