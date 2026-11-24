from .registry import register


class AccessPermission:
    ROLE_MANAGE = register("access.role.manage", "مدیریت نقش ها")
    ASSIGNMENT_MANAGE = register("access.assignment.manage", "مدیریت انتساب نقش ها")
