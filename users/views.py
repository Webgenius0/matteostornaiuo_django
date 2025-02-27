from .models import User, StaffInvitation
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .serializers import (
    StaffSignupSerializer,
    ClientSignupSerializer,
    UserSerializer,
    StaffInvitationSerializer,
    SkillSerializer,
    JobRoleSerializer,
    UniformSerializer
)
from .models import (
    Skill, 
    JobRole,
    Uniform
)
from .email_service import send_staff_signup_email, send_client_signup_email, send_staff_invitation_email_from_client


# Create your views here.
class StaffSignupAPIView(APIView):

    permission_classes = []

    def post(self, request):
        # invited_user = StaffInvitation.objects.all()
        # print("Invited user", invited_user)
        
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if password == confirm_password:
            serializer = StaffSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(is_staff=True)

            staff_member = User.objects.get(email=serializer.data["email"])

            # send_staff_signup_email(staff_member)
            refresh = RefreshToken.for_user(staff_member)
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            data = {
                "user": serializer.data,
                "tokens": tokens,
            }
            # serializer.data

            response = status.HTTP_201_CREATED
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didn not match."}
            )

        return Response(data, status=response)


class ClientSignupAPIView(APIView):

    permission_classes = []

    def post(self, request):
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if password == confirm_password:
            serializer = ClientSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(is_staff=True)
            else:
                response = {
                    # "status": status.HTTP_400_BAD_REQUEST,
                    # "success": False,
                    "errors": serializer.errors,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            staff_member = User.objects.get(email=serializer.data["email"])
            try:
                send_client_signup_email(staff_member)
            except Exception as e:
                pass 
            
            refresh = RefreshToken.for_user(staff_member)
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            data = {
                "user": serializer.data,
                "tokens": tokens,
            }
            response = status.HTTP_201_CREATED
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didn not match."}
            )

        return Response(data, status=response)


# for invite staff from clinets
class StaffInvitationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        staffInvitation = StaffInvitation.objects.filter(user=request.user)
        serializer = StaffInvitationSerializer(staffInvitation, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of staff invitations",
            "data": serializer.data
        }
        return Response(response_data)

    def post(self, request, format=None):
        serializer = StaffInvitationSerializer(data=request.data)
        # print("DFS", request.data['invitations'][0]['staff_email'])
        if serializer.is_valid():
            for invocation in request.data['invitations']:
                staff_email = invocation['staff_email']
                # message = f" {staff_email} {invocation['job_role']} "
                # send_staff_invitation_email_from_client(staff_email, message)

            serializer.save(user=request.user)
            # serializer.save()

            response_data = {
                "message": "Staff invitations sent successfully.",
                "status": 200,
                "success": True,
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# skill api

class SkillList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of skills",
            "data": serializer.data
        }
        return Response(response_data)

class JobRoleList(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        job_roles = JobRole.objects.all()
        serializer = JobRoleSerializer(job_roles, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of job roles",
            "data": serializer.data
        }
        return Response(response_data)

class UniformList(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        uniforms = Uniform.objects.all()
        serializer = UniformSerializer(uniforms, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of uniforms",
            "data": serializer.data
        }
        return Response(response_data)
