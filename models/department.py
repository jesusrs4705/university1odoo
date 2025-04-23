from odoo import models, fields

class Department(models.Model):
    _name = 'university.department'
    _description = 'Department'

    name = fields.Char(string="Name", required=True)
    university_id = fields.Many2one('university.university', string="University")
    head_id = fields.Many2one('university.teacher', string="Head of Department")
    teacher_ids = fields.One2many('university.teacher', 'department_id', string="Teachers")
