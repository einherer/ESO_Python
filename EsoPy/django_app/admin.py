from django.contrib import admin
from django_app.models import Server, Account, Character, Equipment, ActiveAbility, ActiveBuff

admin.site.register(Server)
admin.site.register(Account)
admin.site.register(Character)
admin.site.register(Equipment)
admin.site.register(ActiveAbility)
admin.site.register(ActiveBuff)