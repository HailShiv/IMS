# Task: Add Password Reset Functionality to Login

## Steps:

- [x] Create TODO_reset.md
- [x] Update coreinventory/settings.py: Add email backend
- [x] Update accounts/urls.py: Add auth.urls include + reset paths
- [x] Update accounts/templates/home/login.html: Add forgot password link
- [x] Create accounts/templates/home/password_reset_form.html: Reset request form (custom styled)
- [x] Create accounts/templates/home/password_reset_done.html: Done message
- [x] Create accounts/templates/home/password_reset_confirm.html: Confirm form
- [x] Create accounts/templates/home/password_reset_complete.html: Complete message
- [x] Create email templates
- [x] Test full flow (ready)
      [x] Complete - FieldError fixed by adding is_active/is_staff fields to User model + custom get_users. Migrations applied.
- [ ] Complete
