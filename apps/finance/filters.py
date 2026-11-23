from django_filters import BaseInFilter, CharFilter, FilterSet, DateFilter

from .models import Check


class CharInFilter(BaseInFilter, CharFilter):
    """many to many filter"""


class CheckFilter(FilterSet):
    type = CharInFilter(field_name="type", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")

    date_from = DateFilter(
        field_name="due_date",
        lookup_expr="gte",
    )
    date_to = DateFilter(
        field_name="due_date",
        lookup_expr="lte",
    )

    class Meta:
        model = Check
        fields = ["type", "status", "date_from", "date_to"]
