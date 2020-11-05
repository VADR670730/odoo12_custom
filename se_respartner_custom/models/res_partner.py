# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models,fields
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.user.has_group('base.group_system'):
            return super(ResPartner, self).search(args, offset, limit, order, count=count)
        else:
            args += ['|', ('create_uid', '=', self.env.user.id), '|', ('user_id', '=', self.env.user.id),
                 ('id', '=', self.env.user.partner_id.id)]
        return super(ResPartner, self).search(args, offset, limit, order, count=count)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self.env.user.has_group('base.group_system'):
            return super(ResPartner, self).name_search(name, args, operator, limit)
        else:
            args += ['|', ('create_uid', '=', self.env.user.id), '|', ('user_id', '=', self.env.user.id),
                 ('id', '=', self.env.user.id)]
        return super(ResPartner, self).name_search(name, args, operator, limit)


class ResUsers(models.Model):
    _inherit = 'res.users'


    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self.env.user.has_group('base.group_system'):
            return super(ResUsers, self).name_search(name, args, operator, limit)
        else:
            args += ['|', ('create_uid', '=', self.env.user.id), '|', ('partner_id.user_id', '=', self.env.user.id),
                 ('id', '=', self.env.user.id)]
        return super(ResUsers, self).name_search(name, args, operator, limit)