from django.db import models


class user_task_manager_table(models.Model):
    task_status_enum = (("COMPLETED", "completed"), ("DELETED", "deleted"), (
        "ACTIVE", "active"), ("OVER DUE", "over due"))  # ENUM type for task_status field

    title = models.CharField(max_length=200, error_messages={
                             "blank": "Title is required!!!"}, unique=False)
    description = models.TextField(
        error_messages={"blank": "Description is required!!!"}, unique=False)
    due_date = models.DateField(
        error_messages={"blank": "Due Date is required!!!"}, unique=False)
    task_status = models.CharField(
        max_length=10, choices=task_status_enum, default="ACTIVE", unique=False)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False)

    class meta:
        db_table_comment = "This table store users To-Do task info"

    def __str__(self):
        return f"title:{self.title} status:{self.task_status} due_date:{self.due_date}"
