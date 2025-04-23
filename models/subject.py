from odoo import models, fields, api

class Subject(models.Model):
    _name = 'university.subject'
    _description = 'Subject'

    name = fields.Char(string="Name", required=True)
    university_id = fields.Many2one('university.university', string="University")
    teacher_ids = fields.Many2many('university.teacher', string="Teachers")
    enrollment_ids = fields.One2many('university.enrollment', 'subject_id', string="Enrollments")

    # Counted fileds for the counters and their functions
    enrollments_count = fields.Integer(compute='_compute_enrollments_count', string='Enrollments Count')
    teachers_count = fields.Integer(compute='_compute_teachers_count', string='Teachers Count')

    def _compute_enrollments_count(self):
        for subject in self:
            subject.enrollments_count = self.env['university.enrollment'].search_count([('subject_id', '=', subject.id)])

    def _compute_teachers_count(self):
        for subject in self:
            subject.teachers_count = len(subject.teacher_ids)

    def action_view_enrollments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subject Enrollments',
            'res_model': 'university.enrollment',
            'view_mode': 'list,form',
            'domain': [('subject_id', '=', self.id)],
            'context': {'default_subject_id': self.id}
        }

    def action_view_teachers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subject Teachers',
            'res_model': 'university.teacher',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.teacher_ids.ids)],
            'context': {'default_subject_ids': [(4, self.id)]}
        }