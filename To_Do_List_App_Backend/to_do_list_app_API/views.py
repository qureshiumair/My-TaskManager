from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserTaskManagerSerializer
from django.http import JsonResponse
from rest_framework import status
import json
from .models import user_task_manager_table
from django.core.exceptions import ObjectDoesNotExist
import logging


# logger object to log exception and important operations
logger = logging.getLogger()


class UserTaskManagerView(APIView):
    '''
        This class based APIView contains view for adding new To-Do task and fetching existing tasks 
    '''

    def get(self, request):
        '''
          GET APIView to get the all/or specific task info, If request body contains title key then only task info with that title will be return 
          @params:
            request (object): POST request with new task data in the body 

          @returns:
             ret_dict (dictionary): response dictionary
        '''
        try:
            is_id = request.GET.get('task_id', False)
            data = user_task_manager_table.objects.order_by("-created_at").all() if not is_id else user_task_manager_table\
                .objects.filter(id=is_id).order_by("-created_at").all()

            if is_id and not data:
                raise ValueError("No such task found!!!")

            serializer = UserTaskManagerSerializer(data, many=True)
            ret_dict = {"data": serializer.data}
            status_code = status.HTTP_200_OK

        except ValueError as e:
            logger.critical(f"{e}")
            ret_dict = {"data": f"{e}"}
            status_code = status.HTTP_404_NOT_FOUND

        except BaseException as e:
            logger.critical(f"{e}")
            ret_dict = {
                "data": "Unable to process your request,try after sometime!!!"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(ret_dict, status=status_code)

    def post(self, request):
        '''
            POST APIView to add new task by the user
          @params:
            request (object): POST request with new task data in the body

          @returns:
             ret_dict (dictionary): response dictionary 
        '''
        try:
            request_data = json.loads(request.body)
            serializer = UserTaskManagerSerializer(data=request_data)
            if not serializer.is_valid():
                raise ValueError(serializer.errors)

            serializer.save()
            ret_dict = {"message": "Task added successfully!!!"}
            status_code = status.HTTP_201_CREATED

        except ValueError as e:
            logger.critical(f"{e}")
            ret_dict = {"message": f"{e}"}
            status_code = status.HTTP_400_BAD_REQUEST

        except BaseException as e:
            logger.critical(f"{e}")
            ret_dict = {
                "message": "Unable to process your request,try after sometimes!!!"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(ret_dict, status=status_code)

    def delete(self, request):
        '''
        APIView to delete exsiting task
        @params:
            request (object): DELETE request with title of task which will be delete

        @returns:
             ret_dict (dictionary): response dictionary 
        '''
        try:
            task_id = json.loads(request.body).get('task_id', False)
            user_task_manager_table.objects.get(
                id=task_id).delete()
            ret_dict = {"message": "Task deleted successfully!!!"}
            status_code = status.HTTP_200_OK

        except ObjectDoesNotExist as e:
            logger.critical(f"{e}")
            ret_dict = {
                "message": f'''No such task found!!!'''}
            status_code = status.HTTP_400_BAD_REQUEST

        except BaseException as e:
            logger.critical(f"{e}")
            ret_dict = {
                "message": "Unable to process your request,try after sometimes!!!"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(ret_dict, status=status_code)

    def put(self, request):
        '''
        APIView to update task info 
        @params:
            request (object): UPDATE request object

        @returns:
            ret_dict (dictionary): response dictionary 
        '''
        try:
            request_data = json.loads(request.body)
            task_id = request_data.get("task_id")
            task_obj = user_task_manager_table.objects.filter(
                id=task_id).first()

            if not task_obj:
                raise ValueError(
                    f'''No such task found!!!''')

            serializer = UserTaskManagerSerializer(data=request_data)
            if not serializer.is_valid():
                raise ValueError(serializer.errors)

            serializer.update(task_obj, serializer.data, task_id)
            ret_dict = {"message": "Task Info Updated successfully!!!"}
            status_code = status.HTTP_200_OK

        except ValueError as e:
            logger.critical(f"{e}")
            ret_dict = {"message": f"{e}"}
            status_code = status.HTTP_400_BAD_REQUEST

        except BaseException as e:
            logger.critical(f"{e}")
            ret_dict = {
                "message": "Unable to process your request,try after sometimes!!!"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(ret_dict, status=status_code)
