import re

from knox.auth import TokenAuthentication

from rudderstack.helpers.custom_exception_helper import TokenNotFoundException


class BusinessAuthentication(TokenAuthentication):

    def authenticate(self, request):
        try:
            user, auth_token = super(BusinessAuthentication, self).authenticate(request)
        except Exception as e:
            raise TokenNotFoundException()
        path = request.path
        from users.models import UserModel
        if re.search("/api/business/*", path) and user and type(user) == UserModel:
            from business.repository import BusinessRepository
            business = BusinessRepository.get_active_business_for_user(user.id)
            if not business:
                from rudderstack.helpers.custom_exception_helper import UserBusinessNotFoundException
                raise UserBusinessNotFoundException("")
            request.business = business
        return user, auth_token
