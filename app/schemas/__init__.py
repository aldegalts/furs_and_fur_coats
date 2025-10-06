from .auth_schema import (
    TokenPairResponse,
    AccessTokenResponse,
    LoginRequest,
    RefreshRequest
)

from .user_schema import (
    UserBase,
    UserCreate,
    UserResponse,
    UserDetailResponse
)

from .category_schema import (
    CategoryBase,
    CategoryResponse,
    CategoryWithProductsResponse
)

from .product_attribute_schema import (
    ProductAttributeBase,
    ProductAttributeResponse
)

from .product_schema import (
    ProductBase,
    ProductFilterRequest,
    ProductResponse
)

from .cart_item_schema import (
    CartItemBase,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartItemWithProductResponse
)

from .cart_schema import (
    CartBase,
    CartCreate,
    CartResponse
)

from .order_item_schema import (
    OrderItemBase,
    OrderItemResponse,
    OrderItemWithProductResponse
)

from .order_schema import (
    OrderBase,
    OrderCreate,
    OrderResponse,
    OrderWithItemsResponse
)


CategoryResponse.model_rebuild()
ProductAttributeResponse.model_rebuild()

ProductResponse.model_rebuild()
CartItemResponse.model_rebuild()
OrderItemResponse.model_rebuild()

CategoryWithProductsResponse.model_rebuild()
CartItemWithProductResponse.model_rebuild()
OrderItemWithProductResponse.model_rebuild()
CartResponse.model_rebuild()
OrderWithItemsResponse.model_rebuild()
UserDetailResponse.model_rebuild()