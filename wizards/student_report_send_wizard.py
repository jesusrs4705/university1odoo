from odoo import api, fields, models

class StudentReportSendWizard(models.TransientModel):
    _name = 'student.report.send.wizard'
    _description = 'Send Student Report by Email'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        student_id = self.env.context.get('active_id')
        if student_id:
            student = self.env['university.student'].browse(student_id)
            res.update({
                'student_id': student.id,
                'email_to': student.email,
            })
        return res

    student_id = fields.Many2one('university.student', string='Student', required=True, readonly=True)
    email_to = fields.Char(string='Recipient Email', required=True)
    subject = fields.Char(string='Subject', required=True, 
                         default=lambda self: self.env.ref('university1.email_template_student_report').subject)
    body = fields.Html(string='Message Body', required=True, 
                      default=lambda self: self.env.ref('university1.email_template_student_report').body_html)

    def action_send_report(self):
        self.ensure_one()
        template = self.env.ref('university1.email_template_student_report')
        
        # Update template temporarily with wizard values
        template.write({
            'email_to': self.email_to,
            'subject': self.subject,
            'body_html': self.body,
        })
        
        # Send mail with template
        template.send_mail(
            self.student_id.id,
            force_send=True,
            email_values={'email_to': self.email_to}
        )
        
        # Restore template original values
        template.write({
            'email_to': '{{ object.email }}',
            'subject': 'Academic Report for {{ object.name }} - {{ object.university_id.name }}',
            'body_html': template.body_html,
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Academic report has been sent to {self.email_to}',
                'type': 'success',
                'sticky': False,
            }
        }