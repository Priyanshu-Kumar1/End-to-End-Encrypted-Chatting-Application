package org.kivy;
import android.app.Application;
import java.io.FileInputStream;
import com.onesignal.OneSignal;
import android.content.Context;
import android.util.AttributeSet;
import android.content.Intent;
import java.lang.Override;
import android.util.Log;
import java.util.concurrent.TimeUnit;



public class ApplicationClass extends Application{

    private static final String ONESIGNAL_APP_ID = "f4a48b57-05da-478f-99af-fed3e8ae98ac";
  
    @Override
    public void onCreate() {
        super.onCreate();
        
        // Enable verbose OneSignal logging to debug issues if needed.
        OneSignal.setLogLevel(OneSignal.LOG_LEVEL.VERBOSE, OneSignal.LOG_LEVEL.NONE);
        
        // OneSignal Initialization
        OneSignal.initWithContext(this);
        OneSignal.setAppId("f4a48b57-05da-478f-99af-fed3e8ae98ac");
      
        // promptForPushNotifications will show the native Android notification permission prompt.
        // We recommend removing the following code and instead using an In-App Message to prompt for notification permission (See step 7)
        OneSignal.promptForPushNotifications();
    }
}


        
    

    

        



  

