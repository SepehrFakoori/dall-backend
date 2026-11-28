import json
from contextlib import contextmanager
from datetime import date
from typing import Annotated

from django.db import close_old_connections, transaction
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from rest_framework.exceptions import ValidationError

from apps.tenants.models import Tenant

from .models import CheckDirection
from .serializers import CheckSerializer, CheckStatusSerializer, CheckTypeSerializer


class CheckInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    purpose: str
    sayad_id: str
    type: Annotated[StrictInt, Field(description="Check type ID.")]
    status: Annotated[StrictInt, Field(description="Check status ID.")]
    due_date: date
    amount: StrictInt
    description: str = ""
    drawer: Annotated[str | None, Field(description="For received checks only.")] = None
    payee: Annotated[str | None, Field(description="For issued checks only.")] = None


CREATE_ANNOTATIONS = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": False,
    "openWorldHint": False,
}


@contextmanager
def _write_transaction():
    # FastMCP's ASGI app runs outside Django's request lifecycle.
    close_old_connections()
    try:
        with transaction.atomic():
            yield
    except ValidationError as exc:
        raise ToolError(json.dumps(exc.detail, ensure_ascii=False)) from exc
    finally:
        close_old_connections()


def _create_classification(serializer_class, tenant_id, name, direction) -> dict:
    serializer = serializer_class(
        data={"tenant": tenant_id, "name": name, "type": direction.value}
    )
    with _write_transaction():
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


def create_server() -> FastMCP:
    """Build the finance tools for the Dall MCP server."""
    server = FastMCP("Finance", mask_error_details=True)

    @server.tool(annotations=CREATE_ANNOTATIONS)
    def create_check_type(
        tenant_id: StrictInt, name: str, type: CheckDirection
    ) -> dict:
        """Create a received or issued check type for an existing tenant."""
        return _create_classification(CheckTypeSerializer, tenant_id, name, type)

    @server.tool(annotations=CREATE_ANNOTATIONS)
    def create_check_status(
        tenant_id: StrictInt, name: str, type: CheckDirection
    ) -> dict:
        """Create a received or issued check status for an existing tenant."""
        return _create_classification(CheckStatusSerializer, tenant_id, name, type)

    @server.tool(annotations=CREATE_ANNOTATIONS)
    def create_checks(
        tenant_id: StrictInt,
        checks: CheckInput | Annotated[list[CheckInput], Field(min_length=1)],
    ) -> dict:
        """Create one check or a nonempty list of checks for an existing tenant.

        Supply check type and status IDs from that tenant. All checks in a batch
        are saved together, and the result lists them in input order.
        """
        items = checks if isinstance(checks, list) else [checks]
        data = [check.model_dump(mode="json", exclude_unset=True) for check in items]
        with _write_transaction():
            try:
                tenant = Tenant.objects.get(pk=tenant_id)
            except Tenant.DoesNotExist as exc:
                raise ValidationError({"tenant_id": "Tenant does not exist."}) from exc

            serializer = CheckSerializer(
                data=data,
                many=True,
                allow_empty=False,
                context={"tenant": tenant},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(tenant=tenant)
            return {"checks": list(serializer.data)}

    return server
