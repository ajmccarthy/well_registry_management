"""
Tests for admin.monitoring_location module
"""
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.http import HttpRequest
from django.test import Client, TestCase

from ...admin.monitoring_location import MonitoringLocationAdmin
from ...models import MonitoringLocation, AgencyLookup


class TestMonitoringLocationAdmin(TestCase):
    fixtures = ['test_groups.json', 'test_user.json', 'test_agencies.json', 'test_monitoring_location.json']

    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser('my_superuser')
        self.adwr_group = Group.objects.get(name='adwr')
        self.usgs_group = Group.objects.get(name='usgs')

        self.add_permission = Permission.objects.get(codename='add_monitoringlocation')
        self.view_permission = Permission.objects.get(codename='view_monitoringlocation')
        self.change_permission = Permission.objects.get(codename='change_monitoringlocation')
        self.delete_permission = Permission.objects.get(codename='delete_monitoringlocation')

        self.adwr_user = get_user_model().objects.create_user('adwruser')
        self.adwr_user.groups.add(self.adwr_group)
        self.adwr_user.user_permissions.set([
            self.add_permission,
            self.view_permission,
            self.change_permission,
            self.delete_permission
        ])
        self.adwr_user.is_staff = True
        self.adwr_user.save()

        self.usgs_user = get_user_model().objects.create_user('usgsuser')
        self.usgs_user.groups.add(self.usgs_group)
        self.usgs_user.user_permissions.set([
            self.add_permission,
            self.view_permission,
            self.change_permission,
            self.delete_permission
        ])
        self.usgs_user.is_staff = True
        self.usgs_user.save()

        self.site = AdminSite()
        self.admin = MonitoringLocationAdmin(MonitoringLocation, self.site)

    def test_site_id(self):
        reg_entry = MonitoringLocation.objects.get(site_no='44445555',
                                                   agency='ADWR')
        site_id = MonitoringLocationAdmin.site_id(reg_entry)

        self.assertEqual(site_id, "ADWR:44445555")

    def test_save_model_new_monitoring_location_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user
        monitoring_location = MonitoringLocation.objects.create(site_no='11111111',
                                                                agency=AgencyLookup.objects.get(agency_cd='ADWR'))
        self.admin.save_model(request, monitoring_location, None, None)

        saved_monitoring_location = MonitoringLocation.objects.get(site_no='11111111')
        self.assertEqual(saved_monitoring_location.insert_user, self.adwr_user)
        self.assertEqual(saved_monitoring_location.update_user, self.adwr_user)
        self.assertEqual(saved_monitoring_location.agency, AgencyLookup.objects.get(agency_cd='ADWR'))

    def test_save_model_new_monitoring_location_with_super_user(self):
        request = HttpRequest()
        request.user = self.superuser
        monitoring_location = MonitoringLocation.objects.create(site_no='11111111',
                                                                agency=AgencyLookup.objects.get(agency_cd='ADWR'))
        self.admin.save_model(request, monitoring_location, None, None)

        saved_monitoring_location = MonitoringLocation.objects.get(site_no='11111111')
        self.assertEqual(saved_monitoring_location.insert_user, self.superuser)
        self.assertEqual(saved_monitoring_location.update_user, self.superuser)
        self.assertEqual(saved_monitoring_location.agency, AgencyLookup.objects.get(agency_cd='ADWR'))

    def test_save_model_existing_monitoring_location_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.superuser
        monitoring_location = MonitoringLocation.objects.create(site_no='11111111',
                                                                agency=AgencyLookup.objects.get(agency_cd='ADWR'))
        self.admin.save_model(request, monitoring_location, None, None)

        saved_monitoring_location = MonitoringLocation.objects.get(site_no='11111111')
        saved_monitoring_location.site_name = 'A site'
        request.user = self.adwr_user
        self.admin.save_model(request, saved_monitoring_location, None, None)
        saved_monitoring_location = MonitoringLocation.objects.get(site_no='11111111')

        self.assertEqual(saved_monitoring_location.insert_user, self.superuser)
        self.assertEqual(saved_monitoring_location.update_user, self.adwr_user)
        self.assertEqual(saved_monitoring_location.agency, AgencyLookup.objects.get(agency_cd='ADWR'))

    def test_get_queryset_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser
        qs = self.admin.get_queryset(request)

        self.assertEqual(qs.count(), 3)

    def test_get_queryset_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user
        qs = self.admin.get_queryset(request)

        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.filter(agency='ADWR').count(), 1)

    def test_has_view_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_view_permission(request))
        self.assertTrue(self.admin.has_view_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_view_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_view_permission(request))
        self.assertTrue(self.admin.has_view_permission(request, MonitoringLocation.objects.get(site_no='44445555')))
        self.assertFalse(self.admin.has_view_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_add_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_add_permission(request))

    def test_has_add_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_add_permission(request))

    def test_has_change_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_change_permission(request))
        self.assertTrue(self.admin.has_change_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_change_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_change_permission(request))
        self.assertTrue(self.admin.has_change_permission(request, MonitoringLocation.objects.get(site_no='44445555')))
        self.assertFalse(self.admin.has_change_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_delete_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_delete_permission(request))
        self.assertTrue(self.admin.has_delete_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_delete_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_delete_permission(request))
        self.assertTrue(self.admin.has_delete_permission(request, MonitoringLocation.objects.get(site_no='44445555')))
        self.assertFalse(self.admin.has_delete_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_changelist_view_with_usgs_user(self):
        client = Client()
        client.force_login(self.usgs_user)
        resp = client.get('/registry/admin/registry/monitoringlocation/')
        self.assertTrue(resp.context['show_fetch_from_nwis_view'])

    def test_changelist_view_with_adwr_user(self):
        client = Client()
        client.force_login(self.adwr_user)
        resp = client.get('/registry/admin/registry/monitoringlocation/')
        self.assertFalse(resp.context['show_fetch_from_nwis_view'])
