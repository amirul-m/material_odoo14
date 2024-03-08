from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductMaterial(models.Model):
    _name = 'product.material'
    _description = 'Material'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    type = fields.Selection(
        [('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')], string='Type', required=True)
    unit_price = fields.Monetary('Buy Price', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, default=lambda self: self.env.company.currency_id.id)
    partner_id = fields.Many2one(
        'res.partner', string='Supplier', required=True)

    _sql_constraints = [
        ('_unique_code', 'unique (code)',
         "Material code must be uniq!"),
    ]

    @api.constrains('unit_price')
    def _check_unit_price(self):
        for rec in self:
            if rec.unit_price < 100:
                raise ValidationError('Buy Price cannot below 100')
