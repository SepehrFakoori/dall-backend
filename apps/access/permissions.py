from .register import register

register(
    app="access",
    prefix="role",
    permissions={
        "role.view": "View roles",
        "role.manage": "Manage roles and assignments",
    },
    unscoped=["role.view", "role.manage"],
)
