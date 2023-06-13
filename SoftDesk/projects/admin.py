from django.contrib import admin

from projects.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "type"]


class ContributorAdmin(admin.ModelAdmin):
    list_display = ["project_id", "role"]


class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "desc",
        "tag",
        "priority",
        "status",
        "created_time",
    ]

    # @admin.display(description='Category')
    # def category(self, obj):
    #     return obj.product.category


class CommentAdmin(admin.ModelAdmin):
    list_display = ["description", "created_time"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
