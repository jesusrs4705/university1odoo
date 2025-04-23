from odoo import http
from odoo.http import request

class UniversityController(http.Controller):
    @http.route('/universidad', type='http', auth='public', website=True)
    def university_list(self, **kw):
        universities = request.env['university.university'].sudo().search([])
        values = {
            'universities': universities,
            'page_name': 'universities',
        }
        return request.render("university1.university_list_template", values)

    @http.route(['/profesores/<model("university.university"):university>'], type='http', auth='public', website=True)
    def teachers_list(self, university, **kw):
        teachers = request.env['university.teacher'].sudo().search([
            ('university_id', '=', university.id)
        ])
        values = {
            'university': university,
            'teachers': teachers,
            'page_name': 'teachers',
        }
        return request.render("university1.teachers_list_template", values)