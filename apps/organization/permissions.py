from apps.access.register import register

register(
    app="organization",
    prefix="department",
    permissions={
        "department.view": "View department",
        "department.create": "Create department",
        "department.edit": "Edit department",
        "department.delete": "Delete department",
        "department.approve": "Approve department",
    },
)
