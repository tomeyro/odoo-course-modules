# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string='Title', required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)

    taken_seats = fields.Float(compute="_taken_seats", default=0.0)

    instructor_id = fields.Many2one(
        'res.partner',
        string='Instructor',
        domain=[
            '|',
            ('instructor', '=', True),
            ('category_id', 'ilike', 'Teacher'),
        ]
    )
    course_id = fields.Many2one(
        'openacademy.course',
        ondelete='cascade',
        string='Course',
        required=True
    )
    attendee_ids = fields.Many2many('res.partner', string='Attendees')

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if self.seats:
            self.taken_seats = 100 * len(self.attendee_ids) / self.seats
        else:
            self.taken_seats = 0

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not "
                               "be negative",
                }
            }
        if len(self.attendee_ids) > self.seats:
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                }
            }
