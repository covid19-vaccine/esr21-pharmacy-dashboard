from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..model_wrappers import DrugDisposalModelWrapper, \
    DrugDisposalUploadModelWrapper, ChainOfCustodyUploadModelWrapper, \
    IncidentReportUploadModelWrapper, DailyTempLogUploadModelWrapper


class DashboardView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):
    navbar_name = 'esr21_pharmacy_dashboard'
    navbar_selected_item = 'esr21_pharmacy'
    template_name = 'esr21_pharmacy/dashboard/home.html'
    drug_disposal_model_wrapper_cls = DrugDisposalModelWrapper
    drug_disposal_upload_model_wrapper_cls = DrugDisposalUploadModelWrapper
    chain_of_custody_upload_model_wrapper_cls = ChainOfCustodyUploadModelWrapper
    incident_report_upload_model_wrapper_cls = IncidentReportUploadModelWrapper
    daily_temp_log_upload_model_wrapper_cls = DailyTempLogUploadModelWrapper

    drug_accountability_model = 'esr21_pharmacy.drugaccountabilitylog'
    drug_disposal_upload_model = 'esr21_pharmacy.drugdisposalupload'
    chain_of_custody_upload_model = 'esr21_pharmacy.chainofcustodyupload'
    incident_report_upload_model = 'esr21_pharmacy.incidentreportupload'
    daily_temp_log_upload_model = 'esr21_pharmacy.dailytemplogupload'
    vac_details_model = 'esr21_subject.vaccinationdetails'

    @property
    def drug_accountability_cls(self):
        return django_apps.get_model(self.drug_accountability_model)

    @property
    def drug_disposal_upload_cls(self):
        return django_apps.get_model(self.drug_disposal_upload_model)

    @property
    def chain_of_custody_upload_cls(self):
        return django_apps.get_model(self.chain_of_custody_upload_model)

    @property
    def incident_report_upload_cls(self):
        return django_apps.get_model(self.incident_report_upload_model)

    @property
    def daily_temp_log_upload_cls(self):
        return django_apps.get_model(self.daily_temp_log_upload_model)

    @property
    def vac_details_cls(self):
        return django_apps.get_model(self.vac_details_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        incident_report_upload_obj = self.incident_report_upload_cls()
        drug_disposal_upload_obj = self.drug_disposal_upload_cls()
        chain_of_custody_upload_obj = self.chain_of_custody_upload_cls()
        daily_temp_log_upload_obj = self.daily_temp_log_upload_cls()

        incident_report_upload = self.incident_report_upload_model_wrapper_cls(
            model_obj=incident_report_upload_obj)
        drug_disposal_upload = self.drug_disposal_upload_model_wrapper_cls(
            model_obj=drug_disposal_upload_obj)
        chain_of_custody_upload = self.chain_of_custody_upload_model_wrapper_cls(
            model_obj=chain_of_custody_upload_obj)
        daily_temp_log_upload = self.daily_temp_log_upload_model_wrapper_cls(
            model_obj=daily_temp_log_upload_obj)

        context.update(
            add_incident_report_upload_url=incident_report_upload.href,
            add_drug_disposal_upload_url=drug_disposal_upload.href,
            add_chain_of_custody_upload_url=chain_of_custody_upload.href,
            add_daily_temp_log_upload_url=daily_temp_log_upload.href,
            inventory=self.inventory,
            cms_inventory=self.cms_inventory,
            all_sites_active_stats=self.all_sites_active_stats,
        )

        return context

    @property
    def all_sites_active_stats(self):
        all_sites_active_stats = []
        for site_name in self.sites_names:
            all_sites_active_stats.append(self.active_at_site(site_name))
        return all_sites_active_stats

    @property
    def all_sites_stats(self):
        all_sites_stats = []
        for site_name in self.sites_names:
            all_sites_stats.append(self.issued_per_site(site_name))
        return all_sites_stats

    @property
    def cms_inventory(self):
        return self.cms_inventory_update - self.inventory

    @property
    def inventory(self):
        total = 0
        for site in self.all_sites_stats:
            if site.get('total'):
                total = total + site.get('total')
        return total

    @property
    def cms_inventory_update(self):
        return sum(
            self.drug_accountability_cls.objects.filter(
                injection_site='CMS', status='active').exclude(
                quantity_received=None).values_list('quantity_received', flat=True))

    def active_at_site(self, site_name):
        try:
            active_on_site = self.drug_accountability_cls.objects.get(
                injection_site=site_name, status='active')

        except self.drug_accountability_cls.DoesNotExist:
            return {'site_name': site_name, 'total': 0, 'lot_number': None}
        else:
            if active_on_site.balance:
                return {'site_name': site_name, 'total': int(active_on_site.balance),
                        'lot_number': active_on_site.lot_number}
            else:
                return {'site_name': site_name, 'total': 0,
                        'lot_number': active_on_site.lot_number}

    def issued_per_site(self, site_name):
        """
        Return a dict of site name and the total drugs that were dispatched to 
        a site
        """
        on_site = self.drug_accountability_cls.objects.filter(
            injection_site=site_name).exclude(status='Disposed')
        count = 0
        for batch in on_site:
            count = count + batch.issued
        return {'site_name': site_name, 'total': count}

    @property
    def last_cms_update(self):
        return self.drug_accountability_cls.objects.order_by(
            '-date').first()

    def latest_site_drug_update(self, site):
        return self.drug_accountability_cls.objects.filter(
            injection_site=f'{site}').order_by('-date').first()

    @property
    def sites_names(self):
        site_lists = []
        sites = Site.objects.all()
        for site in sites:
            name = site.name.split('-')[1]
            site_lists.append(name)
        return site_lists
