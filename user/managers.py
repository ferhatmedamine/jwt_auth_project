from django.db import models

class UserRoleManager(models.Manager):
    def add_user_to_organisation(self, user, organisation, role='student'):
        return self.create(user=user, organisation=organisation, role=role)

    def update_user_role(self, user, organisation, new_role):
        user_role = self.get(user=user, organisation=organisation)
        user_role.role = new_role
        user_role.save()
        return user_role

    def remove_user_from_organisation(self, user, organisation):
        self.filter(user=user, organisation=organisation).delete()