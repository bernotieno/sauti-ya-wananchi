from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'category',
        'county',
        'urgency',
        'ai_processed',
        'is_verified',
        'created_at',
    ]
    list_filter = [
        'category',
        'urgency',
        'county',
        'ai_processed',
        'is_verified',
        'created_at',
    ]
    search_fields = [
        'raw_text',
        'summary',
        'county',
        'officer_name',
        'department_name',
    ]
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('Complaint Details', {
            'fields': ('id', 'raw_text', 'summary')
        }),
        ('Classification', {
            'fields': ('category', 'county', 'urgency', 'sentiment')
        }),
        ('Media', {
            'fields': ('audio_file', 'image_file')
        }),
        ('Identification', {
            'fields': ('officer_name', 'department_name'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ai_processed', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    actions = ['mark_as_verified', 'export_as_csv']

    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} complaints marked as verified.")
    mark_as_verified.short_description = "Mark selected complaints as verified"

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="complaints.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Category', 'County', 'Urgency', 'Summary',
            'Officer', 'Department', 'Created At', 'Verified'
        ])

        for complaint in queryset:
            writer.writerow([
                str(complaint.id),
                complaint.category,
                complaint.county,
                complaint.urgency,
                complaint.summary or complaint.raw_text[:200],
                complaint.officer_name,
                complaint.department_name,
                complaint.created_at.strftime('%Y-%m-%d %H:%M'),
                'Yes' if complaint.is_verified else 'No'
            ])

        return response
    export_as_csv.short_description = "Export selected complaints as CSV"
