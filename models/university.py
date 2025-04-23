from odoo import models, fields, api

class University(models.Model):
    _name = 'university.university'
    _description = 'University'

    image = fields.Image(string="Image", max_width=1920, max_height=1920)
    name = fields.Char(string="Name", required=True)
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    zip = fields.Char(string="Postal Code")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    director_id = fields.Many2one('university.teacher', string="Director")

    department_ids = fields.One2many('university.department', 'university_id', string="Departments")
    teacher_ids = fields.One2many('university.teacher', 'university_id', string="Teachers")
    student_ids = fields.One2many('university.student', 'university_id', string="Students")
    enrollment_ids = fields.One2many('university.enrollment', 'university_id', string="Enrollments")

    # Counted fileds for the counters and their functions
    students_count = fields.Integer(compute='_compute_counts', string='Students Count')
    teachers_count = fields.Integer(compute='_compute_counts', string='Teachers Count')
    enrollments_count = fields.Integer(compute='_compute_counts', string='Enrollments Count')
    departments_count = fields.Integer(compute='_compute_counts', string='Departments Count')

    def _compute_counts(self):
        for university in self:
            university.students_count = self.env['university.student'].search_count([('university_id', '=', university.id)])
            university.teachers_count = self.env['university.teacher'].search_count([('university_id', '=', university.id)])
            university.enrollments_count = self.env['university.enrollment'].search_count([('university_id', '=', university.id)])
            university.departments_count = self.env['university.department'].search_count([('university_id', '=', university.id)])

    def action_view_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'University Students',
            'res_model': 'university.student',
            'view_mode': 'kanban,list,form',
            'domain': [('university_id', '=', self.id)],
            'context': {'default_university_id': self.id}
        }

    def action_view_teachers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'University Teachers',
            'res_model': 'university.teacher',
            'view_mode': 'kanban,list,form',
            'domain': [('university_id', '=', self.id)],
            'context': {'default_university_id': self.id}
        }

    def action_view_enrollments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'University Enrollments',
            'res_model': 'university.enrollment',
            'view_mode': 'list,form',
            'domain': [('university_id', '=', self.id)],
            'context': {'default_university_id': self.id}
        }

    def action_view_departments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'University Departments',
            'res_model': 'university.department',
            'view_mode': 'list,form',
            'domain': [('university_id', '=', self.id)],
            'context': {'default_university_id': self.id}
        }