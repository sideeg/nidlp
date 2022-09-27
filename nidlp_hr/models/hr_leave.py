from datetime import datetime, time

from dateutil import rrule
from pytz import timezone

from odoo import api, fields, models, tools

from odoo.addons.resource.models.resource import Intervals


class HolidaysRequestType(models.Model):
    _inherit = "hr.leave.type"
    is_calender_days = fields.Boolean()


class HolidaysRequest(models.Model):
    _inherit = "hr.leave"
    is_calender_days = fields.Boolean(related="holiday_status_id.is_calender_days")

    def _get_number_of_days(self, date_from, date_to, employee_id):
        self = self.with_context(is_calender_days=self.is_calender_days)
        return super()._get_number_of_days(date_from, date_to, employee_id)

    def _compute_number_of_hours_display(self):
        for holiday in self:
            super(
                HolidaysRequest, holiday.with_context(is_calender_days=holiday.is_calender_days)
            )._compute_number_of_hours_display()


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    def _exist_interval_in_date(self, intervals, date):
        return any(interval[0].date() == date for interval in intervals)

    def _calender_days_intervals_batch(self, start_dt, end_dt, intervals, resources):
        for resource in resources or []:  # since resources can be None.
            interval_resource = intervals[resource.id]
            tz = timezone(resource.tz)
            attendances = []
            if len(interval_resource._items) > 0:
                attendances = interval_resource._items
            for day in rrule.rrule(rrule.DAILY, dtstart=start_dt, until=end_dt):
                exist_interval = self._exist_interval_in_date(attendances, day.date())
                if not exist_interval:  # add days if they dont exist.
                    attendances.append(
                        (
                            datetime.combine(day.date(), time.min).replace(tzinfo=tz),
                            datetime.combine(day.date(), time.max).replace(tzinfo=tz),
                            self.env["resource.calendar.attendance"],
                        )
                    )
            intervals[resource.id] = Intervals(attendances)
        return intervals

    def _attendance_intervals_batch(
        self, start_dt, end_dt, resources=None, domain=None, tz=None, is_calender_days=False
    ):
        res = super()._attendance_intervals_batch(
            start_dt=start_dt, end_dt=end_dt, resources=resources, domain=domain, tz=tz
        )
        if self.env.context.get("is_calender_days"):
            return self._calender_days_intervals_batch(start_dt, end_dt, res, resources)
        return res

    def _leave_intervals_batch(self, start_dt, end_dt, resources=None, domain=None, tz=None):
        if self.env.context.get("is_calender_days"):
            resources_list = list(resources) + [self.env["resource.resource"]]
            return {r.id: Intervals([]) for r in resources_list}
        return super()._leave_intervals_batch(start_dt, end_dt, resources, domain, tz)
