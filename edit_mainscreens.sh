#!/bin/bash
sed -i '/var notifGranted by remember { mutableStateOf(false) }/,/var overlayGranted by remember { mutableStateOf(false) }/c\
    var notifGranted by remember { mutableStateOf(false) }\
    var adminGranted by remember { mutableStateOf(false) }\
    var accessGranted by remember { mutableStateOf(false) }\
    var overlayGranted by remember { mutableStateOf(false) }\
    val lifecycleOwner = androidx.lifecycle.compose.LocalLifecycleOwner.current\
    androidx.compose.runtime.DisposableEffect(lifecycleOwner) {\
        val observer = androidx.lifecycle.LifecycleEventObserver { _, event ->\
            if (event == androidx.lifecycle.Lifecycle.Event.ON_RESUME) {\
                val enabledListeners = android.provider.Settings.Secure.getString(context.contentResolver, "enabled_notification_listeners")\
                notifGranted = enabledListeners != null && enabledListeners.contains(context.packageName)\
                val dpm = context.getSystemService(android.content.Context.DEVICE_POLICY_SERVICE) as android.app.admin.DevicePolicyManager\
                val componentName = android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java)\
                adminGranted = dpm.isAdminActive(componentName)\
                val enabledServices = android.provider.Settings.Secure.getString(context.contentResolver, android.provider.Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES)\
                accessGranted = enabledServices != null && enabledServices.contains(context.packageName)\
                overlayGranted = android.provider.Settings.canDrawOverlays(context)\
            }\
        }\
        lifecycleOwner.lifecycle.addObserver(observer)\
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }\
    }' app/src/main/java/com/example/ui/screens/MainScreens.kt
