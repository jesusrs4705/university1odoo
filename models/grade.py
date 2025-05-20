from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Grade(models.Model):
    _name = 'university.grade'
    _description = 'Grade'

    student_id = fields.Many2one('university.student', string="Student")
    enrollment_id = fields.Many2one('university.enrollment', string="Enrollment")
    date = fields.Date(string='Grade Date', default=fields.Date.today, required=True)
    teacher_id = fields.Many2one('university.teacher', string='Grading Teacher', required=True, related='enrollment_id.teacher_id', store=True)
    value = fields.Float(string="Grade", digits=(3,2))

    @api.constrains('value')
    def _check_value(self):
        for record in self:
            if record.value < 0 or record.value > 10:
                raise ValidationError('La nota debe estar entre 0 y 10.')