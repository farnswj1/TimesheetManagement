from django.core.mail import send_mail

def send_registration_email(email, username, password):
    send_mail(
        "Time Management Account Registered!",
        f"Your account has been resistered! Here are your login credentials:\n\n\tUsername: {username}\n\tPassword: {password}\n\nCheers,\n\tTime Management",
        "sample@timemanagement.com",
        [email],
        fail_silently=False,
    )