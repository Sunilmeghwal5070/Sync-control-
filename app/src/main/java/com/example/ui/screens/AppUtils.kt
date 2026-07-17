package com.example.ui.screens

import android.content.Context
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import com.example.data.AppInfo

fun getInstalledApps(context: Context): List<AppInfo> {
    val pm = context.packageManager
    val packages = pm.getInstalledApplications(PackageManager.GET_META_DATA)
    val apps = mutableListOf<AppInfo>()
    for (packageInfo in packages) {
        if ((packageInfo.flags and ApplicationInfo.FLAG_SYSTEM) == 0) {
            val appName = pm.getApplicationLabel(packageInfo).toString()
            val packageName = packageInfo.packageName
            apps.add(AppInfo(packageName = packageName, appName = appName, isLocked = false, isHidden = false))
        }
    }
    return apps
}
