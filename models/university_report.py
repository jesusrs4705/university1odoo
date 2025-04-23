from odoo import models, fields, api
from odoo import tools

class UniversityReport(models.Model):
    _name = 'university.report'
    _description = 'University Report'
    _auto = False

    university_id = fields.Many2one('university.university', string='University')
    professor_id = fields.Many2one('university.teacher', string='Professor')
    department_id = fields.Many2one('university.department', string='Department')
    student_id = fields.Many2one('university.student', string='Student')
    subject_id = fields.Many2one('university.subject', string='Subject')
    average_grade = fields.Float(string='Average Grade', digits=(14,2), group_operator="avg")

    def init(self):
        tools.drop_view_if_exists(self._cr, 'university_report')
        self._cr.execute('''
            CREATE OR REPLACE VIEW university_report AS (
                SELECT
                    ROW_NUMBER() OVER () AS id,
                    e.university_id,
                    e.teacher_id AS professor_id,
                    t.department_id,
                    e.student_id,
                    e.subject_id,
                    AVG(g.value) AS average_grade
                FROM
                    university_enrollment e
                    JOIN university_grade g ON e.id = g.enrollment_id
                    JOIN university_teacher t ON e.teacher_id = t.id
                GROUP BY
                    e.university_id,
                    e.teacher_id,
                    t.department_id,
                    e.student_id,
                    e.subject_id
            )
        ''')