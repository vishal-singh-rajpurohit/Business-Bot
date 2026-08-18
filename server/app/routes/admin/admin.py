from fastapi import APIRouter, status
from .super_admin import super_admin_router

admin_router = APIRouter(prefix='/admin', tags=['Admin'])

admin_router.include_router(prefix='super')

"""
    0. Auth Admin

    1. Admin Login

    2. Create Member

    3. Change Access

"""

# 0. Auth Admin
@admin_router.post("/auth", status_code=status.HTTP_200_OK)
def root():
    pass

# 1. Admin Login
@admin_router.post("/login", status_code=status.HTTP_201_CREATED)
def root():
    pass

# 2. Create Member
@admin_router.post("/create-member", status_code=status.HTTP_201_CREATED)
def root():
    pass

# 3. Change Access
@admin_router.post("/change-access", status_code=status.HTTP_201_CREATED)
def root():
    pass

