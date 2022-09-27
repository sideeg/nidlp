import io

import xlsxwriter

from odoo import _, fields, models
from odoo.exceptions import UserError


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    report_type = fields.Selection(selection_add=[("xlsx", "Excel")], ondelete={"xlsx": "cascade"})

    def _render_excel(self, docids, data=None):
        docids = docids.split(",")
        docids = [int(x) for x in docids]
        obj_ids = self.env[self.model].browse(docids)
        return self._render_xlsx(self.report_name, obj_ids), "xlsx"

    def _render_xlsx(self, report_name, obj_ids=None):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(
            output,
            {
                "in_memory": True,
                "strings_to_formulas": False,
            },
        )
        sheet = workbook.add_worksheet(report_name[:31])

        try:
            option, lines = getattr(obj_ids, self.report_name)()
        except (AttributeError, TypeError) as e:
            raise UserError(
                _(
                    "Please define the function %s on the model %s in order to use this report"
                    % (self.report_name, self.model)
                )
            ) from e
        if option.get("col_sizing"):
            for key, size in enumerate(option.get("col_sizing")):
                sheet.set_column(key, key, size)
        else:
            sheet.set_column(0, option.get("col_number") - 1, option.get("col_size", 20))
        sheet.right_to_left()
        y_offset = 0
        # write lines
        for line in lines:
            line_items = line.get("items", [])
            line_style = line.get("style")
            style_highlight = workbook.add_format(line_style)
            line_x_offset = line.get("x_offset", 0)
            line_y_offset = line.get("y_offset", 0)
            if len(line_items) == 1:
                y_range = y_offset + line_y_offset
                sheet.merge_range(
                    y_range,
                    line_x_offset,
                    y_range,
                    line_x_offset + option.get("col_number") - 1,
                    line_items[0],
                    style_highlight,
                )
            else:
                for x_offset, col in enumerate(line_items):
                    sheet.write(y_offset, x_offset + line_x_offset, col, style_highlight)
            y_offset += 1 + line_y_offset

        workbook.close()
        output.seek(0)
        generated_file = output.read()
        output.close()
        return generated_file
