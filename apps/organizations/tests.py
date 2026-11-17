from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from .models import Organization, OrganizationMembership, OrganizationUnit


class OrganizationQuerySetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="member")
        cls.other_user = get_user_model().objects.create_user(username="other")
        cls.company = Organization.objects.create(name="Alpha")
        cls.second = Organization.objects.create(name="Beta")
        cls.deleted = Organization.objects.create(name="Deleted", is_deleted=True)
        cls.member = OrganizationMembership.objects.create(
            organization=cls.company, user=cls.user
        )
        cls.inactive_member = OrganizationMembership.objects.create(
            organization=cls.second, user=cls.user, is_active=False
        )
        OrganizationMembership.objects.create(
            organization=cls.second, user=cls.other_user
        )
        OrganizationMembership.objects.create(organization=cls.deleted, user=cls.user)
        cls.department = OrganizationUnit.objects.create(
            organization=cls.company, name="Engineering"
        )
        cls.line = OrganizationUnit.objects.create(
            organization=cls.company,
            name="Production",
            type=OrganizationUnit.Type.LINE,
            parent=cls.department,
        )
        for company in (cls.second, cls.deleted):
            OrganizationUnit.objects.create(organization=company, name="Other")

    def test_for_user_matches_active_membership_for_that_same_user(self):
        self.assertQuerySetEqual(
            Organization.objects.for_user(self.user), [self.company]
        )

    def test_multiple_companies_are_supported(self):
        self.inactive_member.is_active = True
        self.inactive_member.save(update_fields=["is_active"])
        self.assertQuerySetEqual(
            Organization.objects.for_user(self.user), [self.company, self.second]
        )

    def test_all_companies_and_deleted_companies_can_be_queried_explicitly(self):
        self.assertQuerySetEqual(
            Organization.objects.all(), [self.company, self.second]
        )
        self.assertQuerySetEqual(Organization.all_objects.dead(), [self.deleted])
        self.assertQuerySetEqual(
            Organization.all_objects.for_user(self.user),
            [self.company, self.deleted],
        )

    def test_memberships_can_be_scoped_by_company_and_status(self):
        self.assertQuerySetEqual(
            OrganizationMembership.objects.for_organization(self.company).active(),
            [self.member],
        )
        self.assertQuerySetEqual(
            OrganizationMembership.objects.for_organization(self.second.pk).inactive(),
            [self.inactive_member],
        )
        self.assertEqual(OrganizationMembership.objects.all().count(), 4)

    def test_user_memberships_include_inactive_until_explicitly_filtered(self):
        self.assertEqual(OrganizationMembership.objects.for_user(self.user).count(), 3)
        self.assertQuerySetEqual(
            OrganizationMembership.objects.for_user(self.user).inactive(),
            [self.inactive_member],
        )

    def test_reverse_managers_offer_queryset_methods(self):
        self.assertQuerySetEqual(self.company.memberships.active(), [self.member])
        self.assertQuerySetEqual(
            self.user.organization_memberships.inactive(), [self.inactive_member]
        )
        self.assertQuerySetEqual(self.company.units.departments(), [self.department])

    def test_units_can_be_scoped_by_company_type_or_user(self):
        self.assertQuerySetEqual(
            OrganizationUnit.objects.for_organization(self.company.pk).lines(),
            [self.line],
        )
        self.assertQuerySetEqual(
            OrganizationUnit.objects.for_user(self.user),
            [self.department, self.line],
            ordered=False,
        )
        self.assertEqual(OrganizationUnit.objects.all().count(), 4)

    def test_anonymous_unsaved_and_nonmember_users_get_empty_querysets(self):
        outsider = get_user_model().objects.create_user(username="outsider")
        for user in (AnonymousUser(), get_user_model()(username="unsaved"), outsider):
            for model in (Organization, OrganizationMembership, OrganizationUnit):
                with self.subTest(user=user, model=model):
                    self.assertFalse(model.objects.for_user(user).exists())

    def test_queries_are_lazy_and_chainable(self):
        with self.assertNumQueries(0):
            organizations = Organization.objects.filter(name="Alpha").for_user(
                self.user
            )
            members = self.company.memberships.active().select_related("user")
        self.assertEqual(organizations.get(), self.company)
        with self.assertNumQueries(1):
            self.assertEqual(members.get().user, self.user)

    def test_scoped_delete_preserves_soft_deletion(self):
        Organization.objects.for_user(self.user).delete()
        self.assertFalse(Organization.objects.filter(pk=self.company.pk).exists())
        self.assertTrue(Organization.all_objects.get(pk=self.company.pk).is_deleted)
        self.assertTrue(
            OrganizationMembership.objects.filter(pk=self.member.pk).exists()
        )
