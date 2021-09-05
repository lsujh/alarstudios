from typing import List, Optional

from fastapi import Request

from app.enums.roles import Roles


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.email or not len(self.email) > 5:
            self.errors.append("Email should be > 5 chars")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("A valid email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be > 4 chars")
        if not self.errors:
            return True
        return False


class UserUpdateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.role: Optional[Roles] = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.role = form.get("role")

    async def is_valid(self):
        if not self.email or not len(self.email) > 5:
            self.errors.append("Email should be > 5 chars")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("A valid email is required")
        if not self.role in Roles.list():
            self.errors.append("A valid role is required (Admin, Manager)")
        if not self.errors:
            return True
        return False
