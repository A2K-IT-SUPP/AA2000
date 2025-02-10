from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_custom_email(user, email_type, ticket_id=None, status_link=None, reply_message=None, attachments=None):
    """
    Sends a custom email with support for multiple attachments.
    
    Parameters:
        - user: The recipient user object
        - email_type: Type of email ('inquiry_confirmation' or 'admin_reply')
        - ticket_id: The generated ticket ID (required for inquiry confirmation)
        - status_link: Link to check ticket status (required for inquiry confirmation)
        - reply_message: Message content for admin reply (optional)
        - attachments: List of file attachments (optional, only for admin reply)
    """
    
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    # Configure based on email_type
    if email_type == 'inquiry_confirmation':
        subject = 'Your Support Ticket ID'
        template_name = 'ticket_email.html'
        context = {
            'user': user,
            'ticket_id': ticket_id,
            'status_link': status_link,
        }
    elif email_type == 'admin_reply':
        subject = 'Response to Your Support Ticket'
        template_name = 'reply_email.html'
        context = {
            'user': user,
            'reply_message': reply_message,
            'ticket_id': ticket_id,
        }
    else:
        raise ValueError("Invalid email type specified")

    # Render the HTML content with context variables
    html_content = render_to_string(f'users/{template_name}', context)
    
    # Create email message with HTML content
    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    
    # Attach each file if provided (only applicable to 'admin_reply')
    if email_type == 'admin_reply' and attachments:
        for file in attachments:
            email.attach(file.name, file.read(), file.content_type)

    # Send the email
    email.send()