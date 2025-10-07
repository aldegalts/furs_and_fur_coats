from typing import List
from pydantic import BaseModel, ConfigDict


class ProductRecommendation(BaseModel):
    product_id: int
    product_name: str
    change_percent: int
    action: str


class AnalyticsPeriod(BaseModel):
    start: str
    end: str
    total_orders: int


class ProductSummary(BaseModel):
    id: int
    product_name: str
    category: str
    total_sold: int
    total_revenue: float


class RawSalesData(BaseModel):
    products: List[ProductSummary]


class AnalyticsResponse(BaseModel):
    analysis: str
    recommendations: List[ProductRecommendation]
    period: AnalyticsPeriod
    raw_data: RawSalesData

    model_config = ConfigDict(from_attributes=True)
