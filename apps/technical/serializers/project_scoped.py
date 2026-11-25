from rest_framework import serializers

from apps.projects.models import Project


class ProjectScopedSerializer(serializers.ModelSerializer):
    """Validate nested technical records against the authorized URL project."""

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.unscoped.none(),
        required=False,
        help_text="Optional project ID. If supplied, it must match the project in the URL.",
    )

    def get_fields(self):
        """Accept a submitted project only when it matches the verified parent."""
        fields = super().get_fields()
        project = self.context.get("project")
        fields["project"].queryset = Project.unscoped.filter(
            pk=getattr(project, "pk", None)
        )
        return fields

    def validate(self, attrs):
        """Require the view's verified parent even when the project field is omitted."""
        if self.context.get("project") is None:
            raise serializers.ValidationError(
                {"project": "A verified project is required."}
            )
        return super().validate(attrs)
