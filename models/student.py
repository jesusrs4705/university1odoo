from odoo import models, fields, api, _
from markupsafe import escape
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'university.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Image(string="Image", max_width=1920, max_height=1920)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    user_id = fields.Many2one('res.users', string='Related User', readonly=True)
    lang = fields.Selection(
        selection='_get_lang',
        string='Language',
        default=lambda self: self.env.lang
    )
    university_id = fields.Many2one('university.university', string="University")
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    zip = fields.Char(string="Postal Code")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    tutor_id = fields.Many2one('university.teacher', string="Tutor")
    enrollment_ids = fields.One2many('university.enrollment', 'student_id', string="Enrollments")
    grade_ids = fields.One2many('university.grade', 'student_id', string="Grades")

    # Counted fileds for the counters and their functions
    enrollments_count = fields.Integer(compute='_compute_enrollments_count', string='Enrollments Count')
    grades_count = fields.Integer(compute='_compute_grades_count', string='Grades Count')

    _sql_constraints = [
        ('unique_user', 'unique(user_id)', 'A user can only be linked to one student!')
    ]

    @api.model
    def create(self, vals):
        # Create student record
        student = super(Student, self).create(vals)
        
        # Create portal user
        user_vals = {
            'name': vals.get('name'),
            'login': vals.get('email'),
            'email': vals.get('email'),
            'password': 'change_me_123',
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
            'lang': vals.get('lang', self.env.user.lang),
        }
        
        try:
            user = self.env['res.users'].with_context(no_reset_password=True).create(user_vals)
            student.user_id = user.id
        except Exception as e:
            raise ValidationError(f"Error creating user: {str(e)}")
            
        return student

    @api.model
    def _get_lang(self):
        return self.env['res.lang'].get_installed()

    def _compute_enrollments_count(self):
        for student in self:
            student.enrollments_count = self.env['university.enrollment'].search_count([('student_id', '=', student.id)])

    def _compute_grades_count(self):
        for student in self:
            student.grades_count = self.env['university.grade'].search_count([('student_id', '=', student.id)])

    def action_view_enrollments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student Enrollments',
            'res_model': 'university.enrollment',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id}
        }

    def action_view_grades(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student Grades',
            'res_model': 'university.grade',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id}
        }

    def action_send_report(self):
        '''Open mail compose window with student report template'''
        self.ensure_one()
        template = self.env.ref('university1.email_template_student_report')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Academic Report',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'university.student',
                'default_res_ids': [self.id],
                'default_use_template': bool(template),
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
                'force_email': True
            }
        }

    def sendTestEmail(self):
        """Handle the test email sending action triggered from JS"""
        self.ensure_one()
        if not self.email:
            return False
        
        try:
            return self.action_send_report()
        except Exception:
            return False
    
    def action_send_email(self):
        '''Send academic report by email'''
        self.ensure_one()
        template = self.env.ref('university1.email_template_student_report')
        if template:
            template.send_mail(
                self.id,
                force_send=True,
                email_values={
                    'email_to': self.email,
                    'auto_delete': True
                }
            )
            return {
                'toast_message': escape(_("A sample email has been send to %s",self.email)),
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': f'A sample email has been send to {self.email}',
                    'type': 'success',
                    'sticky': False,
                }
                
            }
