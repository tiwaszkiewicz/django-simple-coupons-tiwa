from django.contrib import admin # type: ignore

from django_simple_coupons.models import (Coupon,
                                          Discount,
                                          Ruleset,
                                          CouponUser,
                                          AllowedUsersRule,
                                          MaxUsesRule,
                                          ValidityRule)

from django_simple_coupons.actions import (reset_coupon_usage, delete_expired_coupons, generate_coupons_action)


# Register your models here.
# ==========================
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.crypto import get_random_string
from .models import Coupon, Discount, Ruleset

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'times_used', 'created')
    change_list_template = "admin/coupon_change_list.html"


    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_url'] = 'generate-coupons'
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
        if request.method == 'POST':
            # Przykładowe parametry
            prefix = request.POST.get('prefix', 'NEW_')
            count = int(request.POST.get('count', 5))

            discount = Discount.objects.first()
            ruleset = Ruleset.objects.first()

            if not discount or not ruleset:
                self.message_user(request, "Error: Missing Discount or Ruleset", level="error")
                return redirect("..")

            for _ in range(count):
                random_part = get_random_string(length=30 - len(prefix))
                code = f"{prefix}{random_part}"
                Coupon.objects.create(code=code, discount=discount, ruleset=ruleset)

            self.message_user(request, f"Successfully created {count} new coupons.")
            return redirect("..")

        return render(request, 'admin/generate_coupons.html', {
            'title': 'Generate New Coupons',
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
    
    



