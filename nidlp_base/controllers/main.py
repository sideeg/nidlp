# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import http
from odoo.http import content_disposition, request

from odoo.addons.web.controllers.main import ReportController


class ReportControllerCustom(ReportController):
    @http.route(
        [
            "/report/<converter>/<reportname>",
            "/report/<converter>/<reportname>/<docids>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def report_routes(self, reportname, docids=None, converter=None, **data):
        report = request.env["ir.actions.report"]._get_report_from_name(reportname)
        context = dict(request.env.context)
        if converter == "xlsx":
            excel = report.with_context(context)._render_excel(docids, data=data)[0]
            pdfhttpheaders = [("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")]
            return request.make_response(excel, headers=pdfhttpheaders)
        return super().report_routes(reportname, docids, converter, **data)

    @http.route(["/report/download"], type="http", auth="user")
    def report_download(self, data, context=None):
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        if type in ["qweb-pdf", "qweb-text"]:
            return super().report_download(data, context)

        extension = converter = "xlsx"
        reportname = url.split("/report/xlsx/")[1].split("?")[0]

        docids = None
        if "/" in reportname:
            reportname, docids = reportname.split("/")

        response = self.report_routes(reportname, docids=docids, converter=converter, context=context)
        report = request.env["ir.actions.report"]._get_report_from_name(reportname)
        filename = "%s.%s" % (report.name, extension)

        response.headers.add("Content-Disposition", content_disposition(filename))
        return response
