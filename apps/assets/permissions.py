from apps.access.register import register

register(
    app="assets",
    prefix="assets",
    permissions={
        "assets.view": "Assets",
        "assets.manage": "Manage assets",
    },
    unscoped=["assets.view", "assets.manage"],
)
