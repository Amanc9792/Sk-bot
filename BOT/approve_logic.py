import datetime
import pytz

# Timezone for IST
IST = pytz.timezone('Asia/Kolkata')

# Dictionary to store approved users and their expiration
approved_users = {}

def get_current_ist_time():
    return datetime.datetime.now(IST)

# Approve a user and return the activation and expiration details
def approve_user(tguserid, no_of_days, owner_id):
    current_time = get_current_ist_time()
    expiration_date = current_time + datetime.timedelta(days=no_of_days)
    approved_users[tguserid] = expiration_date

    return {
        'activation_date': current_time.strftime('%Y-%m-%d'),
        'activation_time': current_time.strftime('%H:%M:%S'),
        'expiry_date': expiration_date.strftime('%Y-%m-%d'),
        'expiry_time': expiration_date.strftime('%H:%M:%S'),
    }

# Check if the user is premium and return their details
def get_user_premium_status(tguserid, username):
    current_time = get_current_ist_time()
    if tguserid in approved_users:
        expiration_time = approved_users[tguserid]
        if expiration_time > current_time:
            activation_time = expiration_time - datetime.timedelta(days=30)  # Assuming 30 days premium
            return {
                'activation_date': activation_time.strftime('%Y-%m-%d'),
                'activation_time': activation_time.strftime('%H:%M:%S'),
                'expiry_date': expiration_time.strftime('%Y-%m-%d'),
                'expiry_time': expiration_time.strftime('%H:%M:%S'),
            }
    return None

# Remove expired users from the approved users list
def remove_expired_users():
    current_time = get_current_ist_time()
    expired_users = [user for user, expiry in approved_users.items() if expiry <= current_time]
    for user in expired_users:
        del approved_users[user]
    return expired_users

# Check if the user is approved
def is_user_approved(tguserid):
    current_time = get_current_ist_time()
    if tguserid in approved_users and approved_users[tguserid] > current_time:
        return True
    else:
        if tguserid in approved_users:
            del approved_users[tguserid]
        return False
