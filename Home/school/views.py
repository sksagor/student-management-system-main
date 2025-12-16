from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
# IMPORT YOUR NOTIFICATION MODEL HERE
from .models import Notification 
# from school.models import Notification # If it's in another app
from .models import Notification # Ensure this is imported for the function below
from django.contrib.auth import get_user_model

User = get_user_model()

# --- ADD THIS FUNCTION HERE ---
def create_notification(user, message, notification_type=None):
    """
    Creates a new notification for the specified user.
    """
    if user and message:
        if isinstance(user, int) or isinstance(user, str):
            try:
                user = User.objects.get(pk=user)
            except User.DoesNotExist:
                print(f"Warning: User with ID {user} not found for notification.")
                return

        Notification.objects.create(
            user=user, 
            message=message,
        )
# -----------------------------


def index(request):
    """
    Renders the login page.
    """
    return render(request, "authentication/login.html")


def dashboard(request):
    """
    Renders the dashboard and retrieves notification data.
    """
    # FIX: Use capitalized 'Notification'
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notification.count()
    
    context = {
        'unread_notification_count': unread_notification_count,
        # Pass the QuerySet if your template needs to iterate over them
        # 'unread_notifications': unread_notification 
    }
    return render(request, "students/student-dashboard.html", context)


# --- Notification Views ---

def mark_notification_as_read(request):
    """
    Marks all unread notifications for the user as read.
    NOTE: The logic here is identical to mark_all_notifications_read.
    You should consider removing one or renaming this to handle a SINGLE notification
    if that was your original intent.
    """
    if request.method == 'POST':
        # FIX: Use capitalized 'Notification'
        notifications_to_read = Notification.objects.filter(user=request.user, is_read=False)
        notifications_to_read.update(is_read=True)
        return JsonResponse({'status': 'success'})
    
    return HttpResponseForbidden()


def clear_all_notification(request):
    """
    Deletes all notifications for the current user.
    """
    if request.method == "POST":
        # FIX: Use capitalized 'Notification'
        notifications_to_delete = Notification.objects.filter(user=request.user)
        notifications_to_delete.delete()
        return JsonResponse({'status': 'success'})
        
    # FIX: Call the function (add parentheses)
    return HttpResponseForbidden()


def mark_all_notifications_read(request):
    """
    Marks all unread notifications for the current user as read.
    (This function is redundant if mark_notification_as_read is implemented this way)
    """
    if request.method == 'POST':
        # Find all unread notifications for the logged-in user
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        
        # Update them to read
        unread_notifications.update(is_read=True)
        
        # We'll stick to a redirect for this example, or use JsonResponse based on usage.
        return redirect('dashboard') # Assuming 'dashboard' is a named URL
    
    return HttpResponseForbidden()