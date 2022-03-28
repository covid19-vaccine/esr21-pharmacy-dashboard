from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar

no_url_namespace = True if settings.APP_NAME == 'esr21_pharmacy_dashboard' else False

esr21_pharmacy_dashboard = Navbar(name='esr21_pharmacy_dashboard')

esr21_pharmacy_dashboard.append_item(
    NavbarItem(
        name='esr21_pharmacy',
        title='ESR21 Pharmacy Dashboard',
        label='Pharmacy Dashboard',
        fa_icon='fas fa-shopping-basket',
        url_name='esr21_pharmacy_dashboard:home_url',
        no_url_namespace=no_url_namespace))

site_navbars.register(esr21_pharmacy_dashboard)
