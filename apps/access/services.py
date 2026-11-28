from collections import defaultdict
from dataclasses import dataclass, field

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q, Model

from .models import Scope, RoleAssignment, RolePermission


@dataclass
class Grant:
    tenant_all: bool = False
    tenant_own: bool = False
    dept_all: set = field(default_factory=set)
    dept_own: set = field(default_factory=set)


class AccessResolver:
    def __init__(self, user, tenant):
        self.user = user
        self.tenant = tenant
        self._grants = None

    @property
    def grants(self) -> dict[str, Grant]:
        if self._grants is None:
            self._grants = self._load()
        return self._grants

    def _load(self) -> dict[str, Grant]:
        grants: dict[str, Grant] = {}
        if not (self.user and self.user.is_authenticated):
            return grants

        # Query 1: this user's assignments in this company
        assignments = list(
            RoleAssignment.objects.filter(
                membership__user=self.user,
                membership__tenant=self.tenant,
                membership__is_active=True,
                role__is_active=True,
            ).values_list("role_id", "department_id")
        )

        if not assignments:
            return grants

        # Query 2: the permissions of those roles
        role_perms = defaultdict(list)
        rows = RolePermission.objects.filter(
            role_id__in={role_id for role_id, _ in assignments},
        ).values_list("role_id", "code", "scope")
        for role_id, code, scope in rows:
            role_perms[role_id].append((code, scope))

        # Combine: grants are addictive (union of everything the user has)
        for role_id, dept_id in assignments:
            for code, scope in role_perms[role_id]:
                g = grants.setdefault(code, Grant())
                if dept_id is None:
                    if scope == Scope.ALL:
                        g.tenant_all = True
                    else:
                        g.tenant_own = True
                else:
                    (g.dept_all if scope == Scope.ALL else g.dept_own).add(dept_id)
        return grants

    def can(
        self,
        code,
        obj=None,
        *,
        owner_field="created_by_id",
        department_field="department_id",
    ) -> bool:
        if self.user.is_superuser:
            return True
        g = self.grants.get(code)
        if g is None:
            return False
        if obj is None:  # view-level check: does the user hold the code at all?
            return True
        if g.tenant_all:
            return True
        dept = getattr(obj, department_field, None)
        if dept is not None and dept in g.dept_all:
            return True
        is_owner = getattr(obj, owner_field, None) == self.user.pk
        return is_owner and (g.tenant_own or (dept is not None and dept in g.dept_own))

    def scope_queryset(
        self, qs, code, *, owner_field="created_by_id", department_field="department_id"
    ):
        if self.user.is_superuser:
            return qs
        g = self.grants.get(code)
        if g is None:
            return qs.none()
        if g.tenant_all:
            return qs
        q = Q()
        if g.dept_all:
            q |= Q(**{f"{department_field}__in": g.dept_all})
        if g.tenant_own:
            q |= Q(**{owner_field: self.user.pk})
        if g.dept_own:
            q |= Q(**{f"{department_field}__in": g.dept_own, owner_field: self.user.pk})
        return qs.filter(q) if q else qs.none()


def get_resolver(request) -> AccessResolver:
    resolver = getattr(request, "_access", None)
    if resolver is None:
        resolver = request._access = AccessResolver(request.user, request.tenant)
    return resolver
