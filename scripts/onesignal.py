from jnius import autoclass

Context = autoclass('android.content.Context')

# Register device for push notifications
OneSignal = autoclass('com.onesignal.OneSignal')
OneSignal.startInit(Context.getContext())
OneSignal.setInFocusDisplaying(OneSignal.OSInFocusDisplayOption.Notification)
OneSignal.init()

# Retrieve the player ID
player_id = OneSignal.getPermissionSubscriptionState().getSubscriptionStatus().getUserId()

