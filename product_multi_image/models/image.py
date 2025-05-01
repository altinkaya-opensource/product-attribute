# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).

from odoo import api, fields, models


class Image(models.Model):
    _inherit = "base_multi_image.image"

    is_published = fields.Boolean(
        string="Published",
        default=True,
        help="If you uncheck this field, this image will not be shown in "
        "the website.",
    )

    product_variant_ids = fields.Many2many(
        comodel_name="product.product",
        string="Visible in these variants",
        help="If you leave it empty, all variants will show this image. "
        "Selecting one or several of the available variants, you "
        "restrict the availability of the image to those variants.",
    )
    product_variant_count = fields.Integer(compute="_compute_product_variant_count")

    def _compute_product_variant_count(self):
        for image in self:
            image.product_variant_count = len(image.product_variant_ids)

    @api.depends("owner_id", "owner_model")
    def _show_technical(self):
        """Hide technical fields for product images"""
        res = super(Image, self)
        for img in self:
            ctx = self.env.context
            if "params" in ctx and ctx.get("model") in (
                "product.template",
                "product.product",
            ):
                img.show_technical = False
        return res
