from odoo.tests import common
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged('post_install', '-at_install', 'material')
class TestProductMaterial(common.TransactionCase):

    def test_check_unit_price_below_100(self):
        product_obj = self.env.ref('rest_api_material.material1')
        product = product_obj.write({'unit_price': 50})

        with self.assertRaises(ValidationError):
            product_obj._check_unit_price()

    def test_check_unit_price_above_100(self):
        product_obj = self.env.ref('rest_api_material.material1')
        product = product_obj.write({'unit_price': 100})
        print('Successfully price unit at least 100')

    def test_required_field_empty(self):
        product_obj = self.env['product.material']
        try:
            product = product_obj.create({'code': 'M05'})
        except Exception as e:
            self.fail(e)

    def test_required_field_fill(self):
        product_obj = self.env['product.material']
        product = product_obj.create({
            'code': 'M05',
            'name': 'Material 05',
            'type': 'cotton',
            'unit_price': 105,
            'partner_id': self.env.ref('base.res_partner_12').id,
        })
        print('Successfully create')
