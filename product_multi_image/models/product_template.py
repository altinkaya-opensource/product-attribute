# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = [_name, "base_multi_image.owner"]

    def set_image_1920(self):
        for template in self:
            # If the template has no images, set image_1920 to False
            if not template.image_ids:
                template.image_1920 = False
                continue

            # Get the first image's image_1920 value
            template.image_1920 = template.image_ids[0].image_1920

    def write(self, vals):
        res = super().write(vals)

        if vals.get("image_ids"):
            self.set_image_1920()   

        return res
            
