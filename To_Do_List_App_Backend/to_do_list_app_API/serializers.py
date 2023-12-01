from rest_framework import serializers
from .models import user_task_manager_table
from datetime import datetime


class UserTaskManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_task_manager_table
        fields = '__all__'

    def update(self, instance, validated_data, task_id):
        '''
        We have override an update method becasue we need to implement some of our custom validations before updation in the database
        @params:
            instance (object): old task info object retrived from the database
            validated_data (object): updated task info dictionary sent in the request bt the user
            task_id (integer): ID of the task

        @returns:None

        NOTE: This method will raise ValueError exception if no changes found
        '''
        is_attr_changed = False
        for attr in ("title", "description", "task_status", "due_date"):
            if attr == "due_date" and validated_data.get(attr, False):
                validated_data[attr] = datetime.strptime(
                    validated_data[attr], '%Y-%m-%d').date()

            if getattr(instance, attr) != validated_data.get(attr) and validated_data.get(attr, False):
                is_attr_changed = True
                setattr(instance, attr, validated_data.get(attr))

        if not is_attr_changed:
            raise ValueError("No changes found!!!")

        user_task_manager_table.objects.get(
            id=task_id).delete()
        instance.save()
