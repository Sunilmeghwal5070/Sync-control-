import re
with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

target = '<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />'
replacement = """<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.WRITE_SETTINGS" tools:ignore="ProtectedPermissions" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />"""
content = content.replace(target, replacement)

with open('app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
