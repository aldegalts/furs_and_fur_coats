from decimal import Decimal
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from infrastructure.database.models.order_entity import OrderEntity
from infrastructure.smtp.email_client import EmailClient


class EmailService:
    def __init__(self):
        self.email_client = EmailClient()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(BASE_DIR, "../../infrastructure/smtp/templates")
        template_dir = os.path.normpath(template_dir)
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def send_order_confirmation(self, order: OrderEntity, user_email: str) -> bool:
        total_amount = self._calculate_order_total(order)

        template_data = {
            "order_id": order.id,
            "order_date": order.created_at.strftime("%d.%m.%Y %H:%M"),
            "items": [
                {
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                    "total_price": float(item.unit_price * item.quantity)
                }
                for item in order.items
            ],
            "total_amount": float(total_amount)
        }

        template = self.jinja_env.get_template("order_confirmation.html")
        html_content = template.render(**template_data)

        text_content = self._generate_text_version(order, total_amount)

        subject = f"Заказ #{order.id} оформлен!"
        return self.email_client.send_email(
            to=user_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def _calculate_order_total(self, order: OrderEntity) -> Decimal:
        total = Decimal(0)
        for item in order.items:
            total += item.unit_price * item.quantity
        return total

    def _generate_text_version(self, order: OrderEntity, total_amount: Decimal) -> str:
        lines = [
            f"Ваш заказ #{order.id} успешно оформлен!",
            f"Дата заказа: {order.created_at.strftime('%d.%m.%Y %H:%M')}",
            "",
            "Состав заказа:",
        ]

        for item in order.items:
            lines.append(
                f"- {item.product.name}: {item.quantity} шт. x {item.unit_price} руб. = "
                f"{item.unit_price * item.quantity} руб."
            )

        lines.extend([
            "",
            f"Итого: {total_amount} руб.",
            "",
            "Спасибо за заказ!",
            "",
            "С уважением,",
            "Интернет-магазин \"Меха и шубы\""
        ])

        return "\n".join(lines)