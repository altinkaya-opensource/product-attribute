# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class Product(models.Model):
    _inherit = "product.product"

    product_length = fields.Float("length")
    product_height = fields.Float("height")
    product_width = fields.Float("width")
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for length, height, width",
        default=lambda self: self.env.ref("uom.product_uom_cm"),
    )

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]

    @api.onchange(
        "product_length",
        "product_height",
        "product_width",
        "dimensional_uom_id",
        "volume_uom_id",
    )
    def onchange_calculate_volume(self):
        self.volume = self.env["product.template"]._calc_volume(
            self.product_length,
            self.product_height,
            self.product_width,
            self.dimensional_uom_id,
            self.volume_uom_id,
        )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env.ref("uom.product_uom_meter")

        return dimensional_uom._compute_quantity(
            qty=measure, to_unit=uom_meters, round=False,
        )

    @api.model
    def _calc_volume(self, product_length, product_height, product_width, uom_id, volume_uom_id):
        uom_litre = self.env.ref("uom.product_uom_litre")
        volume_litre = (product_length * product_height * product_width * 1000.0) / (uom_id.factor ** 3)
        return uom_litre._compute_quantity(qty=volume_litre, to_unit=volume_uom_id, round=False)

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for length, height, width",
        readonly=False,
    )
    product_length = fields.Float(
        related="product_variant_ids.product_length", readonly=False
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False
    )

    @api.onchange(
        "product_length",
        "product_height",
        "product_width",
        "dimensional_uom_id",
        "volume_uom_id",
    )
    def onchange_calculate_volume(self):
        self.volume = self._calc_volume(
            self.product_length,
            self.product_height,
            self.product_width,
            self.dimensional_uom_id,
            self.volume_uom_id,
        )
