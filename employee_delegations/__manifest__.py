{
    'name': 'Employee Delegations',
    'version': '15',
    'summary': 'delegations all employee approval',
    'description': 'delegations all employee approval/ leave, approval request,purchase request',
    'author': 'Higazi',
    'depends': ['hr', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        # 'data/custom_channels.xml',
        'data/service_cron.xml',
        'views/view.xml',
        'views/hr_leave_form_inherited.xml',

    ],
}
