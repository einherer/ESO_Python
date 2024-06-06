from django.contrib import admin
from django_app.models import Server, Account, Character, Equipment, ActiveAbility, ActiveBuff

class CharacterNameFilter(admin.SimpleListFilter):
    title = 'Character Name'  # Custom title for the filter
    parameter_name = 'character__name'

    def lookups(self, request, model_admin):
        return [(char.name, char.name) for char in Character.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(character__name=self.value())
        return queryset
    
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'level', 'class_type')
    search_fields = ('name', 'account__username')
    list_filter = ('class_type', 'level')

class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 1

class ActiveAbilityInline(admin.TabularInline):
    model = ActiveAbility
    extra = 1

class ActiveBuffInline(admin.TabularInline):
    model = ActiveBuff
    extra = 1

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_name', 'level', 'class_name')

    def account_name(self, obj):
        return obj.account.name
    account_name.short_description = 'Account'

    search_fields = ('name', 'account')
    list_filter = ('class_name', 'level')
    inlines = [EquipmentInline, ActiveAbilityInline, ActiveBuffInline]  # Inline related models

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'character_name', 'slot', 'quality')

    def character_name(self, obj):
        return obj.character.name
    character_name.short_description = 'Character Name'

    search_fields = ('name', CharacterNameFilter)
    list_filter = ('slot', 'quality', CharacterNameFilter)

class ActiveAbilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'character_name', 'description')

    def character_name(self, obj):
        return obj.character.name
    character_name.short_description = 'Character Name'

    search_fields = ('name', CharacterNameFilter)
    list_filter = ('name', 'description', CharacterNameFilter)

class ActiveBuffAdmin(admin.ModelAdmin):
    list_display = ('name', 'character_name', 'description')

    def character_name(self, obj):
        return obj.character.name
    character_name.short_description = 'Character Name'

    search_fields = ('name', CharacterNameFilter)
    list_filter = ('name', 'description', CharacterNameFilter)

admin.site.register(Server)
admin.site.register(Account)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(ActiveAbility, ActiveAbilityAdmin)
admin.site.register(ActiveBuff, ActiveBuffAdmin)
