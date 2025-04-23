from odoo import models, fields, api

class Grade(models.Model):
    _name = 'university.grade'
    _description = 'Grade'

    student_id = fields.Many2one('university.student', string="Student")
    enrollment_id = fields.Many2one('university.enrollment', string="Enrollment")
    date = fields.Date(string='Grade Date', default=fields.Date.today, required=True)
    teacher_id = fields.Many2one('university.teacher', string='Grading Teacher', required=True, related='enrollment_id.teacher_id', store=True)
    value = fields.Float(string="Grade", digits=(3,2))