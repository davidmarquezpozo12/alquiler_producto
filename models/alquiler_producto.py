from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'
    _description = 'Alquiler de productos'

    partner_id = fields.Many2one(
        'res.partner',
        string="Cliente",
        required=True
    )

    product_id = fields.Many2one(
        'product.product',
        string="Producto",
        required=True
    )

    fecha_inicio = fields.Date(
        string="Fecha inicio",
        required=True,
        default=fields.Date.today
    )

    fecha_fin = fields.Date(
        string="Fecha fin",
        compute="_compute_fecha_fin",
        store=True
    )

    estado = fields.Selection(
        [
            ('en_alquiler', 'En alquiler'),
            ('entregado', 'Entregado'),
            ('no_entregado', 'No entregado')
        ],
        string="Estado",
        default='en_alquiler'
    )

    observaciones = fields.Text(string="Observaciones")

    # Comprueba la disponibilidad del producto
    @api.onchange('product_id')
    def _onchange_producto(self):
        if self.product_id:
            dominio = [
                ('product_id', '=', self.product_id.id),
                ('estado', '=', 'en_alquiler')
            ]
            if self.id:
                dominio.append(('id', '!=', self.id))

            alquiler_activo = self.env['alquiler.producto'].search(dominio, limit=1)
            if alquiler_activo:
                raise ValidationError("Este producto no está disponible para alquiler.")


    # Suma a la fecha de fin 30 días respecto a la fecha de inicio
    @api.depends('fecha_inicio')
    def _compute_fecha_fin(self):
        for record in self:
            if record.fecha_inicio:
                record.fecha_fin = record.fecha_inicio + timedelta(days=30)

    # Marca los productos no entregados
    def cron_marcar_no_entregados(self):
        hoy = fields.Date.today()
        alquileres = self.search([
            ('estado', '=', 'en_alquiler'),
            ('fecha_fin', '<', hoy)
        ])
        alquileres.write({'estado': 'no_entregado'})