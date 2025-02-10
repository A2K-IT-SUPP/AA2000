from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'), 
    path('about', views.about, name="about"),
    
    path('systems', views.systems, name="systems"),
    path('systems/fdas', views.systems_fdas, name="systems_fdas"),
    path('systems/afss', views.systems_afss, name="systems_afss"),
    path('systems/cctv', views.systems_cctv, name="systems_cctv"),
    path('systems/access-control', views.systems_access_control, name="systems_access_control"),
    path('systems/burglar-alarm', views.systems_burglar_alarm, name="systems_burglar_alarm"),
    path('systems/intercom-paging', views.systems_paging, name="systems_paging"),
    path('systems/walkthrough-metal-detectors', views.systems_walkthrough_metal_detectors, name="systems_walkthrough_metal_detectors"),
    path('systems/gate-barriers', views.systems_gate_barriers, name="systems_gate_barriers"),
    path('systems/room-alert', views.systems_room_alert, name="systems_room_alert"),
    path('systems/xray-baggage-scanners', views.systems_xray_scanners, name="systems_xray_scanners"),
    path('systems/eas', views.systems_eas, name="systems_eas"),
    path('systems/led', views.systems_led, name="systems_led"),
    path('systems/robots', views.systems_robots, name="systems_robots"),
    path('systems/erp', views.systems_erp, name="systems_erp"),
    
    path('products', views.products, name="products"),
    path('products/<slug:slug>/overview', views.product_overview, name="product_overview"),
    
    path('services', views.services, name="services"),
    path('services/supply', views.services_supply, name="services_supply"),
    path('services/installation', views.services_installation, name="services_installation"),
    path('services/maintenance', views.services_maintenance, name="services_maintenance"),
    path('services/troubleshooting', views.services_troubleshooting, name="services_troubleshooting"),
    path('services/design', views.services_design, name="services_design"),
    path('services/inspection', views.services_inspection, name="services_inspection"),
    path('services/consultation', views.services_consultation, name="services_consultation"),
    path('services/training', views.services_training, name="services_training"),
    path('services/electrical', views.services_electrical, name="services_electrical"),
    path('services/mechanical', views.services_mechanical, name="services_mechanical"),
    path('services/plumbing', views.services_plumbing, name="services_plumbing"),
    path('services/fitout', views.services_fitout, name="services_fitout"),
    path('services/aircon', views.services_aircon, name="services_aircon"),
    path('services/fire-safety', views.services_fire_safety, name="services_fire_safety"),
    path('services/bms', views.services_bms, name="services_bms"),
    path('services/elevator', views.services_elevator, name="services_elevator"),
    path('services/energy', views.services_energy, name="services_energy"),
    path('services/data-cabling', views.services_data_cabling, name="services_data_cabling"),
    
    path('brands', views.brands, name="brands"),
    path('brands/<slug:slug>/overview', views.brands_overview, name="brands_overview"),
    
    path('careers', views.careers, name="careers"),
    path('careers/<slug:slug>/overview', views.careers_overview, name="careers_overview"),
    
    path('articles', views.articles, name="articles"),
    path('articles/all', views.blogs, name="blogs"),
    path('policy', views.policy, name="policy"),
    path('faqs', views.faqs, name="faqs"),
    path('articles/<slug:slug>/view', views.articles_view, name="articles_view"),
    
    path('contact', views.contact, name="contact"),
    path('inquiry/submit', views.submit_inquiry, name="submit_inquiry"),
    path('inquiry/status', views.ticket, name="ticket"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
