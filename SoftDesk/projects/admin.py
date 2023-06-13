from django.contrib import admin

from projects.models import Project, Contributor, Issue, Comment


admin.site.site_header = "SoftDesk Admin Panel"

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ["title", "description", "type"]


# class ContributorAdmin(admin.ModelAdmin):
#     list_display = ["project_id", "role"]


# class IssueAdmin(admin.ModelAdmin):
#     list_display = [
#         "title",
#         "desc",
#         "tag",
#         "priority",
#         "status",
#         "created_time",
#     ]

#     # @admin.display(description='Category')
#     # def category(self, obj):
#     #     return obj.product.category


# class CommentAdmin(admin.ModelAdmin):
#     list_display = ["description", "created_time"]


# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Contributor, ContributorAdmin)
# admin.site.register(Issue, IssueAdmin)
# admin.site.register(Comment, CommentAdmin)

admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
