# User_Roles_Management

Create a Django application to create a restful API that handles user roles, authentication, and logging:-

User Roles Management Application:
1. Create a new Django app (let’s call it user_roles).
2. Define models for User and Role.
3. Implement views and serializers for adding, updating, and disabling users.
4. Ensure that each role is unique.
5. When a user is assigned a new role, create an entry in a separate table (let’s call it UserRole) with the status (active/disabled).
6. Use Mailtrap.io for sending login credentials to users via email.
7. Verify the user’s status (active/disable) during login.

Logging User Action:
1. Create a separate Model (e.g., UserLog) to store login and logout events, as well as role changes.
2. Implement middleware or signals to capture login/logout events and role changes.
3. Add entries to the log whenever a user logs in, logs out, or has their role modified.

Rules and Guidelines:


1. Create serializers for the User and Role models.
2. Properly validate email addresses.
3. Implement soft delete functionality (mark entries as inactive instead of physically deleting them).
4. Use only MySQL database.
