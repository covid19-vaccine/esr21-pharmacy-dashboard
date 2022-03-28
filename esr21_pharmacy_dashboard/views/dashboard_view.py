from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..model_wrappers import DrugDisposalModelWrapper, \
    ChainOfCustodyModelWrapper, IncidentReportModelWrapper, \
    DrugDisposalUploadModelWrapper, ChainOfCustodyUploadModelWrapper, \
    IncidentReportUploadModelWrapper


class DashboardView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):
    navbar_name = 'esr21_pharmacy_dashboard'
    navbar_selected_item = 'esr21_pharmacy'
    template_name = 'esr21_pharmacy/dashboard/home.html'
    drug_disposal_model_wrapper_cls = DrugDisposalModelWrapper
    chain_of_custody_model_wrapper_cls = ChainOfCustodyModelWrapper
    incident_report_model_wrapper_cls = IncidentReportModelWrapper
    drug_disposal_upload_model_wrapper_cls = DrugDisposalUploadModelWrapper
    chain_of_custody_upload_model_wrapper_cls = ChainOfCustodyUploadModelWrapper
    incident_report_upload_model_wrapper_cls = IncidentReportUploadModelWrapper

    drug_accountability_model = 'esr21_pharmacy.drugaccountabilitylog'
    drug_disposal_upload_model = 'esr21_pharmacy.drugdisposalupload'
    drug_disposal_model = 'esr21_pharmacy.drugdisposal'
    chain_of_custody_model = 'esr21_pharmacy.chainofcustody'
    chain_of_custody_upload_model = 'esr21_pharmacy.chainofcustodyupload'
    incident_report_model = 'esr21_pharmacy.incidentreport'
    incident_report_upload_model = 'esr21_pharmacy.incidentreportupload'
    vac_details_model = 'esr21_subject.vaccinationdetails'

    @property
    def drug_accountability_cls(self):
        return django_apps.get_model(self.drug_accountability_model)

    @property
    def drug_disposal_cls(self):
        return django_apps.get_model(self.drug_disposal_model)

    @property
    def chain_of_custody_cls(self):
        return django_apps.get_model(self.chain_of_custody_model)

    @property
    def incident_report_cls(self):
        return django_apps.get_model(self.incident_report_model)

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
    def vac_details_cls(self):
        return django_apps.get_model(self.vac_details_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        incident_report_obj = self.incident_report_cls()
        drug_disposal_obj = self.drug_disposal_cls()
        chain_of_custody_obj = self.chain_of_custody_cls()

        incident_report_upload_obj = self.incident_report_upload_cls()
        drug_disposal_upload_obj = self.drug_disposal_upload_cls()
        chain_of_custody_upload_obj = self.chain_of_custody_upload_cls()

        incident_report = self.incident_report_model_wrapper_cls(
            model_obj=incident_report_obj)
        drug_disposal = self.drug_disposal_model_wrapper_cls(model_obj=drug_disposal_obj)
        chain_of_custody = self.chain_of_custody_model_wrapper_cls(
            model_obj=chain_of_custody_obj)

        incident_report_upload = self.incident_report_upload_model_wrapper_cls(
            model_obj=incident_report_upload_obj)
        drug_disposal_upload = self.drug_disposal_upload_model_wrapper_cls(
            model_obj=drug_disposal_upload_obj)
        chain_of_custody_upload = self.chain_of_custody_upload_model_wrapper_cls(
            model_obj=chain_of_custody_upload_obj)

        remaining_at_site = self.site_live_count

        context.update(
            add_incident_report_url=incident_report.href,
            add_drug_disposal_url=drug_disposal.href,
            add_chain_of_custody_url=chain_of_custody.href,
            add_incident_report_upload_url=incident_report_upload.href,
            add_drug_disposal_upload_url=drug_disposal_upload.href,
            add_chain_of_custody_upload_url=chain_of_custody_upload.href,
            inventory=self.inventory,
            cms_inventory=self.cms_inventory,
            gabz_issued=self.gabz_issued,
            ftown_issued=self.ftown_issued,
            maun_issued=self.maun_issued,
            phikwe_issued=self.phikwe_issued,
            serowe_issued=self.serowe_issued,
            )

        return context

    @property
    def cms_inventory(self):
        cms_inventory = self.cms_inventory_update - self.inventory

        return cms_inventory

    @property
    def inventory(self):
        return self.gabz_issued + self.ftown_issued + self.maun_issued \
               + self.phikwe_issued + self.serowe_issued

    @property
    def cms_inventory_update(self):
        return sum(
            self.drug_accountability_cls.objects.filter(
                injection_site='CMS', status='active').exclude(
                quantity_received=None).values_list('quantity_received', flat=True))

    @property
    def gabz_issued(self):
        active_on_site = self.drug_accountability_cls.objects.filter(
            injection_site='Gaborone', status='active').exclude(
            issued=None, )
        total = 0
        for bach in active_on_site:
            total = total + bach.issued
        return total

    @property
    def ftown_issued(self):
        active_on_site = self.drug_accountability_cls.objects.filter(
            injection_site='Francistown', status='active').exclude(
            issued=None, )
        total = 0
        for bach in active_on_site:
            total = total + bach.issued
        return total

    @property
    def maun_issued(self):
        active_on_site = self.drug_accountability_cls.objects.filter(
            injection_site='Maun', status='active').exclude(
            issued=None, )
        total = 0
        for bach in active_on_site:
            total = total + bach.issued
        return total

    @property
    def phikwe_issued(self):
        active_on_site = self.drug_accountability_cls.objects.filter(
            injection_site='Phikwe', status='active').exclude(
            issued=None, )
        total = 0
        for bach in active_on_site:
            total = total + bach.issued
        return total

    @property
    def serowe_issued(self):
        active_on_site = self.drug_accountability_cls.objects.filter(
            injection_site='Serowe', status='active').exclude(
            issued=None, )
        total = 0
        for bach in active_on_site:
            total = total + bach.issued
        return total

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

    def site_live_count(self):
        vac_per_site = []
        for site in self.sites_names:
            vaccination_at_site = self.vac_details_cls.objects.filter(
                site_id=site, vaccination_date__gt=self.latest_site_drug_update(site).date
                ).count()
            vac_per_site.append([site, vaccination_at_site])

        return vac_per_site
