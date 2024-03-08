from odoo import http
from odoo.http import request
import json


class MaterialAPI(http.Controller):

    @http.route('/api/materials', type='http', auth='none', methods=['GET'], csrf=False)
    def get_materials(self, **kw):
        materials = request.env['product.material'].sudo().search_read(
            [], ['id', 'code', 'name', 'type', 'unit_price', 'partner_id'])
        serialized_materials = json.dumps(materials)
        return serialized_materials

    @http.route('/api/material/<int:id>', type='http', auth='none', methods=['GET'], csrf=False)
    def get_material(self, id, **kw):
        material = request.env['product.material'].sudo().search_read(
            [('id', '=', id)], ['id', 'code', 'name', 'type', 'unit_price', 'partner_id'])
        if material:
            serialized_material = json.dumps(material[0])
            return serialized_material
        else:
            return json.dumps({"error": "Material not found"})

    @http.route('/api/materials/<string:material_type>', type='http', auth='none', methods=['GET'], csrf=False)
    def get_materials_by_type(self, material_type, **kw):
        Material = request.env['product.material'].sudo()
        type_exist = dict(Material._fields['type'].selection).get(
            material_type, False)
        if not type_exist:
            return json.dumps({"error": f"Material type {material_type} is not valid"})

        materials = Material.search_read(
            [('type', '=', material_type)], ['id', 'code', 'name', 'type', 'unit_price', 'partner_id'])
        if materials:
            serialized_materials = json.dumps(materials)
            return serialized_materials
        else:
            return json.dumps({"error": f"No Material on this type"})

    @http.route('/api/material/<int:id>', type='json', auth='none', methods=['PUT'], csrf=False)
    def update_material(self, id, **kw):
        Material = request.env['product.material'].sudo()
        material = Material.search([('id', '=', id)])
        try:
            vals = json.loads(request.httprequest.data.decode('utf-8'))
        except json.JSONDecodeError:
            return {"error": "Invalid JSON data in request body"}

        is_valid = set(vals.keys()).issubset(Material._fields.keys())
        if not is_valid:
            return {"error": "All fields must be exist on Material"}

        any_false = any([x for x in vals.values() if not x])
        if any_false:
            return {"error": "Value cannot false because all fields is required"}

        unit_price = vals.get('unit_price', 0)
        if unit_price < 100:
            return {"error": "Buy Price cannot below 100"}

        if material:
            material.write(vals)
            return {"error": "This Material has been updated"}
        else:
            return {"error": "ID Material not found"}

    @http.route('/api/material/<int:id>', type='http', auth='none', methods=['DELETE'], csrf=False)
    def delete_material(self, id, **kw):
        material = request.env['product.material'].sudo().search([
            ('id', '=', id)])
        if material:
            material.unlink()
            return json.dumps({"message": "Material deleted successfully"})
        else:
            return json.dumps({"error": "Material not found"})
