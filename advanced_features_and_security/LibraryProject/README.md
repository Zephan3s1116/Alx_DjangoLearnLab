# Bookshelf App - Permissions and Groups Documentation

## Custom Permissions

This application uses custom permissions to control access to book management features.

### Defined Permissions

The Book model includes four custom permissions:

1. can_view - Permission to view books
2. can_create - Permission to create new books
3. can_edit - Permission to edit existing books
4. can_delete - Permission to delete books

## User Groups

Three user groups are configured with different permission levels:

### 1. Viewers
- Permissions: can_view
- Description: Can only view the list of books
- Use Case: General users who need read-only access

### 2. Editors
- Permissions: can_view, can_create, can_edit
- Description: Can view, create, and edit books but cannot delete
- Use Case: Content creators and moderators

### 3. Admins
- Permissions: can_view, can_create, can_edit, can_delete
- Description: Full access to all book management features
- Use Case: Administrators with complete control

## Protected Views

All views in the bookshelf app are protected with the permission_required decorator:

- book_list - Requires bookshelf.can_view
- book_create - Requires bookshelf.can_create
- book_edit - Requires bookshelf.can_edit
- book_delete - Requires bookshelf.can_delete

## Implementation Notes

- Permissions are defined in the Book model Meta class
- Views use Django built-in permission_required decorator
- Groups simplify permission management for multiple users
