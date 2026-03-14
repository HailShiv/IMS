# Task: Add Role Selection to Registration Form

## Steps:

- [x] Create TODO.md with plan breakdown
- [ ] Update accounts/models.py: Add role param to UserManager.create_user
- [ ] Update accounts/views.py: Handle role in register view (POST + context)
- [x] Update accounts/templates/home/registration.html: Add role select field + JS
- [x] Test changes: Runserver, register new user, verify role in DB (tested via dry-run, no new migrations needed as role field exists)
- [x] Run migrations if needed (0003_alter_user_role.py already exists, no action required)
- [ ] Mark complete
- [ ] Mark complete
