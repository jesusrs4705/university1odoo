from odoo import models, fields, api

class Teacher(models.Model):
    _name = 'university.teacher'
    _description = 'Teacher'

    image = fields.Image(string="Image", max_width=1920, max_height=1920)
    name = fields.Char(string="Name", required=True)
    university_id = fields.Many2one('university.university', string="University")
    department_id = fields.Many2one('university.department', string="Department")
    subject_ids = fields.Many2many('university.subject', string="Subjects")
    enrollment_ids = fields.One2many('university.enrollment', 'teacher_id', string="Enrollments")

    # Count field and function 
    enrollments_count = fields.Integer(compute='_compute_enrollments_count', string='Enrollments Count')

    def _compute_enrollments_count(self):
        for teacher in self:
            teacher.enrollments_count = self.env['university.enrollment'].search_count([('teacher_id', '=', teacher.id)])

    
    def action_view_enrollments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teacher Enrollments',
            'res_model': 'university.enrollment',
            'view_mode': 'list,form',
            'domain': [('teacher_id', '=', self.id)],
            'context': {'default_teacher_id': self.id}
        }