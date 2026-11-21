from django.utils.functional import cached_property
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticated,
)

from apps.projects.models import Project, Use
from .models import (
    Block,
    City,
    Floor,
    FloorType,
    Location,
    ProjectProfile,
    Province,
    Unit,
)
from .serializers import (
    BlockSerializer,
    CitySerializer,
    FloorSerializer,
    FloorTypeSerializer,
    LocationSerializer,
    ProjectProfileSerializer,
    ProvinceSerializer,
    UnitSerializer,
)


class ProjectScopedViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_accessible_projects(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(
            organization__memberships__user=user,
            organization__memberships__is_active=True,
        )

    @cached_property
    def project(self):
        return get_object_or_404(
            self.get_accessible_projects(), pk=self.kwargs["project_pk"]
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):
            return queryset.none()
        return queryset.for_project(self.project.pk)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if kwargs.get("many"):
            return serializer

        project_field = serializer.fields["project"]
        project_field.required = False
        project = self.project if "data" in kwargs else self.__dict__.get("project")
        project_field.queryset = Project.objects.filter(pk=getattr(project, "pk", None))
        if project is not None:
            project_field.default = project
        return serializer


class BlockViewSet(ProjectScopedViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class FloorTypeViewSet(ProjectScopedViewSet):
    queryset = FloorType.objects.all()
    serializer_class = FloorTypeSerializer


class FloorViewSet(ProjectScopedViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if not kwargs.get("many") and not getattr(self, "swagger_fake_view", False):
            projects = self.get_accessible_projects()
            serializer.fields["block"].queryset = Block.objects.filter(
                project__in=projects
            )
            serializer.fields["type"].queryset = FloorType.objects.filter(
                project__in=projects
            )
        return serializer


class UnitViewSet(ProjectScopedViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class ProjectProfileViewSet(ProjectScopedViewSet):
    queryset = ProjectProfile.objects.prefetch_related("uses")
    serializer_class = ProjectProfileSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if not kwargs.get("many") and not getattr(self, "swagger_fake_view", False):
            user = self.request.user
            if not user.is_superuser:
                serializer.fields["uses"].child_relation.queryset = Use.objects.filter(
                    organization__memberships__user=user,
                    organization__memberships__is_active=True,
                )
        return serializer


class LocationViewSet(ProjectScopedViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filterset_fields = ("province",)
