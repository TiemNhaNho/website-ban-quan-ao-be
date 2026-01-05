
from typing import Any
from fastapi import Depends

from app.middleware.authenticate import authenticate
from app.models.customer_model import Customer


class AuthorizationMiddleware:
    def __init__(self, allowed_roles: list[Customer.Role]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, customer: Customer = Depends(authenticate)) -> Any:
        if customer.role not in self.allowed_roles:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
        return customer
    
require_admin = AuthorizationMiddleware([Customer.Role.ADMIN])
require_any_user = AuthorizationMiddleware([Customer.Role.ADMIN, Customer.Role.CUSTOMER])