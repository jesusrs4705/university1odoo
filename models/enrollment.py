from odoo import models, fields, api
from datetime import datetime

class Enrollment(models.Model):
    _name = 'university.enrollment'
    _description = 'Enrollment'

    name = fields.Char(string="Enrollment Name", readonly=True, copy=False)
    student_id = fields.Many2one('university.student', string="Student")
    university_id = fields.Many2one('university.university', string="University")
    teacher_id = fields.Many2one('university.teacher', string="Teacher")
    subject_id = fields.Many2one('university.subject', string="Subject")
    grade_ids = fields.One2many('university.grade', 'enrollment_id', string="Grades")

    @api.model
    def create(self, vals):
        if vals.get('subject_id'):
            # Get the subject object
            subject = self.env['university.subject'].browse(vals['subject_id'])
            
            # Get the first three letters of the subject in uppercase
            subject_code = subject.name[:3].upper()
            
            # Get the current year
            current_year = str(datetime.now().year)
            
            # Search for existing enrollments with the same subject code and year
            existing_enrollments = self.search_count([
                ('name', 'like', f'{subject_code}/{current_year}/%')
            ])
            
            # Create the sequential number
            sequence = str(existing_enrollments + 1).zfill(4)
            
            # Generate the enrollment name
            vals['name'] = f"{subject_code}/{current_year}/{sequence}"
        
        return super(Enrollment, self).create(vals)