from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from apps.projects.urls import router as project_router

from .views import (
    BlockViewSet,
    CityViewSet,
    FloorTypeViewSet,
    FloorViewSet,
    LocationViewSet,
    ProjectProfileViewSet,
    ProvinceViewSet,
    UnitViewSet,
)

router = SimpleRouter()
router.register("provinces", ProvinceViewSet)
router.register("cities", CityViewSet)

projects_router = NestedSimpleRouter(project_router, "projects", lookup="project")
projects_router.register("blocks", BlockViewSet, basename="project-block")
projects_router.register("floor-types", FloorTypeViewSet, basename="project-floor-type")
projects_router.register("floors", FloorViewSet, basename="project-floor")
projects_router.register("units", UnitViewSet, basename="project-unit")
projects_router.register("profiles", ProjectProfileViewSet, basename="project-profile")
projects_router.register("locations", LocationViewSet, basename="project-location")

urlpatterns = router.urls + projects_router.urls
