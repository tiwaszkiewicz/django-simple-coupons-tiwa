from django.contrib import admin

from django_simple_coupons.models import (Coupon,
                                          Discount,
                                          Ruleset,
                                          CouponUser,
                                          AllowedUsersRule,
                                          MaxUsesRule,
                                          ValidityRule)

from django_simple_coupons.actions import (reset_coupon_usage, delete_expired_coupons)
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Coupon

from django.shortcuts import render, redirect
from django.urls import path
from django.utils.crypto import get_random_string


# Register your models here.
# ==========================
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.urls import path

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'ruleset', 'times_used', 'created', )
    actions = [delete_expired_coupons]
    change_list_template = "admin/coupon_change_list.html"

    def changelist_view(self, request, extra_context=None):
        """
        Przekazanie URL-a do widoku generowania kuponów.
        """
        extra_context = extra_context or {}
        extra_context['generate_coupons_url'] = reverse('admin:generate-coupons')
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-coupons/', self.admin_site.admin_view(self.generate_coupons_view), name='generate-coupons'),
        ]
        return custom_urls + urls

    def generate_coupons_view(self, request):
        """
        Widok do generowania nowych kuponów.
        """
        discounts = Discount.objects.all()  # Pobierz wszystkie zniżki
        rulesets = Ruleset.objects.all()    # Pobierz wszystkie zestawy zasad


        if request.method == 'POST':
            prefix = request.POST.get('prefix', 'NEW_')
            count = int(request.POST.get('count', 5))

            discount_id = request.POST.get('discount')
            length = int(request.POST.get('length'))     
            ruleset_id = request.POST.get('ruleset')
            discount = Discount.objects.filter(id=discount_id).first()
            ruleset = Ruleset.objects.filter(id=ruleset_id).first()

            
            

            if not discount or not ruleset:
                self.message_user(request, "Error: Missing Discount or Ruleset.", level="error")
                return redirect("..")

            for _ in range(count):
                random_part = get_random_string(length=(length - len(prefix)))
                Coupon.objects.create(code=f"{prefix}{random_part}", discount=discount, ruleset=ruleset)

            self.message_user(request, f"Successfully created {count} coupons.")
            return redirect("..")

        return render(request, 'admin/generate_coupons.html', {
        'title': 'Generate Coupons',
        'discounts': discounts,  # Lista zniżek
        'rulesets': rulesets,    # Lista zestawów zasad
    })




@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(Ruleset)
class RulesetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'allowed_users', 'max_uses', 'validity', )


@admin.register(CouponUser)
class CouponUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'times_used', )
    actions = [reset_coupon_usage]


@admin.register(AllowedUsersRule)
class AllowedUsersRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(MaxUsesRule)
class MaxUsesRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(ValidityRule)
class ValidityRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}