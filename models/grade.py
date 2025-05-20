from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Grade(models.Model):
    _name = 'university.grade'
    _description = 'Grade'
    _rec_name = 'name'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    student_id = fields.Many2one('university.student', string="Student")
    enrollment_id = fields.Many2one('university.enrollment', string="Enrollment")
    date = fields.Date(string='Grade Date', default=fields.Date.today, required=True)
    teacher_id = fields.Many2one('university.teacher', string='Grading Teacher', required=True, related='enrollment_id.teacher_id', store=True)
    value = fields.Float(string="Grade", digits=(3,2))

    @api.depends('student_id', 'enrollment_id')
    def _compute_name(self):
        for record in self:
            if record.student_id and record.enrollment_id and record.enrollment_id.subject_id:
                # Obtener iniciales del estudiante
                student_initials = ''.join(word[0].upper() for word in record.student_id.name.split() if word)
                # Obtener las tres primeras letras de la asignatura en mayúsculas
                subject_code = record.enrollment_id.subject_id.name[:3].upper()
                
                # Obtener número secuencial
                grades = self.search([
                    ('student_id', '=', record.student_id.id),
                    ('enrollment_id.subject_id', '=', record.enrollment_id.subject_id.id)
                ])
                sequence = 1
                for grade in grades:
                    if grade.id == record.id or (not record.id and grade.create_date > (record.create_date or fields.Datetime.now())):
                        break
                    sequence += 1
                
                record.name = f'{student_initials}-{subject_code}{sequence}'
            else:
                record.name = 'New Grade'

    @api.constrains('value')
    def _check_value(self):
        for record in self:
            if record.value < 0 or record.value > 10:
                raise ValidationError('La nota debe estar entre 0 y 10.')

    def init(self):
        """
        Método que se ejecuta al actualizar el módulo para recalcular todos los nombres
        """
        super(Grade, self).init()
        # Forzar el recálculo de los nombres para todos los registros existentes
        for record in self.search([]):
            record._compute_name()