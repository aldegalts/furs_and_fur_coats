from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session

from app.utils.llm import LLMClient
from infrastructure.database.repository import OrderRepository, ProductRepository


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_client = LLMClient()
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)

    def get_production_recommendations(self) -> Dict[str, any]:
        two_weeks_ago = datetime.now() - timedelta(days=14)
        sales_data = self._get_sales_data(two_weeks_ago)

        if not sales_data:
            return {
                "analysis": "За последние 2 недели не было продаж для анализа.",
                "recommendations": [],
                "period": {
                    "start": two_weeks_ago.strftime("%d.%m.%Y"),
                    "end": datetime.now().strftime("%d.%m.%Y")
                }
            }

        sales_summary = self._prepare_sales_summary(sales_data)

        system_prompt = self._create_analytics_prompt()

        llm_response = self.llm_client.chat_with_context(
            data=sales_summary,
            system_prompt=system_prompt
        )

        if not llm_response:
            return {
                "analysis": "Не удалось получить анализ. Попробуйте позже.",
                "recommendations": [],
                "period": {
                    "start": two_weeks_ago.strftime("%d.%m.%Y"),
                    "end": datetime.now().strftime("%d.%m.%Y")
                }
            }

        recommendations = self._extract_recommendations(llm_response)

        return {
            "analysis": llm_response,
            "recommendations": recommendations,
            "period": {
                "start": two_weeks_ago.strftime("%d.%m.%Y"),
                "end": datetime.now().strftime("%d.%m.%Y"),
                "total_orders": len(set(item['order_id'] for item in sales_data))
            },
            "raw_data": self._format_raw_data(sales_data)
        }

    def _get_sales_data(self, start_date: datetime) -> List[Dict]:
        orders = self.order_repo.get_after_date(start_date)

        sales_data = []

        for order in orders:
            for item in order.items:
                sales_data.append({
                    'order_id': order.id,
                    'order_date': order.created_at,
                    'product_id': item.product_id,
                    'product_name': item.product.name,
                    'category': item.product.category.category if item.product.category else 'Без категории',
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price),
                    'total_price': float(item.unit_price * item.quantity)
                })

        return sales_data

    def _prepare_sales_summary(self, sales_data: List[Dict]) -> str:
        product_stats = {}
        category_stats = {}

        for item in sales_data:
            product_id = item['product_id']
            product_name = item['product_name']
            category = item['category']
            quantity = item['quantity']
            total = item['total_price']

            if product_id not in product_stats:
                product_stats[product_id] = {
                    'name': product_name,
                    'category': category,
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'orders_count': 0
                }

            product_stats[product_id]['total_quantity'] += quantity
            product_stats[product_id]['total_revenue'] += total
            product_stats[product_id]['orders_count'] += 1

            if category not in category_stats:
                category_stats[category] = {
                    'total_quantity': 0,
                    'total_revenue': 0
                }

            category_stats[category]['total_quantity'] += quantity
            category_stats[category]['total_revenue'] += total

        summary_lines = [
            "АНАЛИЗ ПРОДАЖ ЗА ПОСЛЕДНИЕ 2 НЕДЕЛИ",
            "=" * 50,
            "",
            f"Всего заказов: {len(set(item['order_id'] for item in sales_data))}",
            f"Всего товаров продано: {sum(item['quantity'] for item in sales_data)} шт.",
            f"Общая выручка: {sum(item['total_price'] for item in sales_data):.2f} руб.",
            "",
            "СТАТИСТИКА ПО КАТЕГОРИЯМ:",
            "-" * 50
        ]

        for category, stats in sorted(category_stats.items(), key=lambda x: x[1]['total_revenue'], reverse=True):
            summary_lines.append(
                f"• {category}: {stats['total_quantity']} шт., "
                f"{stats['total_revenue']:.2f} руб."
            )

        summary_lines.extend([
            "",
            "СТАТИСТИКА ПО ТОВАРАМ:",
            "-" * 50
        ])

        for product_id, stats in sorted(product_stats.items(), key=lambda x: x[1]['total_quantity'], reverse=True):
            summary_lines.append(
                f"{product_id}"
                f"{stats['name']} ({stats['category']}): "
                f"{stats['total_quantity']} шт., "
                f"{stats['orders_count']} заказов, "
                f"{stats['total_revenue']:.2f} руб."
            )

        return "\n".join(summary_lines)

    def _create_analytics_prompt(self) -> str:
        return """Ты — аналитик данных в компании "Меха и шубы", которая производит и продает меховые изделия.

Твоя задача — проанализировать данные о продажах за последние 2 недели и дать КОНКРЕТНЫЕ рекомендации по корректировке объемов производства.

ВАЖНЫЕ ПРАВИЛА:
1. Анализируй тренды и популярность товаров
2. Учитывай как количество проданных единиц, так и выручку
3. Обрати внимание на товары, которые продаются хорошо — их производство нужно увеличить
4. Обрати внимание на товары, которые НЕ продаются — их производство нужно сократить
5. Давай рекомендации в процентах (например: увеличить на 30%, снизить на 50%)
6. В конце ответа ОБЯЗАТЕЛЬНО укажи рекомендации в формате:
   [RECOMMEND: product_id (ПИШИ ID ТОВАРА), изменение в % (+ для увеличения, - для снижения)]
   Например: [RECOMMEND: 5, +30] или [RECOMMEND: 12, -50]

7. Если товар вообще не продавался — рекомендуй снизить производство на 70-100%
8. Если товар очень популярен (больше 5 продаж) — рекомендуй увеличить на 30-50%
9. Учитывай категории товаров — возможно, целая категория популярна или не популярна

ФОРМАТ ОТВЕТА:
1. Общий анализ ситуации
2. Топ-3 популярных товара (что продается лучше всего)
3. Проблемные товары (что не продается)
4. Рекомендации по категориям
5. КОНКРЕТНЫЕ рекомендации по каждому товару в формате [RECOMMEND: ID, процент]

Будь конкретным и давай обоснованные рекомендации!"""

    def _extract_recommendations(self, llm_response: str) -> List[Dict]:
        import re

        recommendations = []

        pattern = r'\[RECOMMEND:\s*(\d+)\s*,\s*([+-]?\d+)\]'
        matches = re.findall(pattern, llm_response)

        for match in matches:
            product_id = int(match[0])
            change_percent = int(match[1])

            product = self.product_repo.get_by_id(product_id)

            if product:
                recommendations.append({
                    'product_id': product_id,
                    'product_name': product.name,
                    'change_percent': change_percent,
                    'action': 'увеличить' if change_percent > 0 else 'снизить'
                })

        return recommendations

    def _format_raw_data(self, sales_data: List[Dict]) -> Dict:
        product_summary = {}

        for item in sales_data:
            product_id = item['product_id']
            if product_id not in product_summary:
                product_summary[product_id] = {
                    'product_name': item['product_name'],
                    'category': item['category'],
                    'total_sold': 0,
                    'total_revenue': 0
                }

            product_summary[product_id]['total_sold'] += item['quantity']
            product_summary[product_id]['total_revenue'] += item['total_price']

        return {
            'products': [
                {
                    'id': pid,
                    **data
                }
                for pid, data in product_summary.items()
            ]
        }