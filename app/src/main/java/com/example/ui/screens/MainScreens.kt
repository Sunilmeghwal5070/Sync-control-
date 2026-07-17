package com.example.ui.screens

import androidx.compose.foundation.Image
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import kotlinx.coroutines.launch
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.PairedDevice
import com.example.viewmodel.AppViewModel
import com.google.zxing.BarcodeFormat
import com.google.zxing.qrcode.QRCodeWriter
import android.graphics.Bitmap
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun UseCaseScreen(
    pairedDevice: PairedDevice?,
    hasParentRole: Boolean,
    viewModel: AppViewModel,
    onNavigateToRoleSelection: () -> Unit,
    onNavigateToParentDashboard: () -> Unit,
    onDisconnect: () -> Unit
) {
    val deviceConfig by viewModel.deviceConfig.collectAsStateWithLifecycle()

    if (hasParentRole) {
        LaunchedEffect(Unit) {
            onNavigateToParentDashboard()
        }
    } else if (pairedDevice != null && pairedDevice.isConnected) {
        ChildDashboard(
            pairCode = pairedDevice.pairCode,
            deviceConfig = deviceConfig,
            onSendMockNotification = { app, msg -> viewModel.sendNotification(app, msg) },
            onDisconnect = onDisconnect
        )
    } else {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            val user = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
            if (user != null) {
                Text(
                    text = "Signed in as: ${user.email}",
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    modifier = Modifier.align(Alignment.End)
                )
            }

            Spacer(modifier = Modifier.height(16.dp))
            Text("What's Your Use Case?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            
            Spacer(modifier = Modifier.height(32.dp))
            
            UseCaseCard(title = "Parent / Child", onClick = onNavigateToRoleSelection)
            Spacer(modifier = Modifier.height(24.dp))
            UseCaseCard(title = "Business / Other", onClick = onNavigateToRoleSelection)
            
            Spacer(modifier = Modifier.weight(1f))
        }
    }
}


@Composable
fun ChildDashboard(
    pairCode: String,
    deviceConfig: com.example.data.DeviceConfig,
    onSendMockNotification: (String, String) -> Unit,
    onDisconnect: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        val user = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
        if (user != null) {
            Text(
                text = "Signed in as: ${user.email}",
                fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                modifier = Modifier.align(Alignment.End)
            )
        }
        Spacer(modifier = Modifier.height(32.dp))
        Icon(Icons.Default.Notifications, contentDescription = "Active", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(80.dp))
        Spacer(modifier = Modifier.height(16.dp))
        Text("Monitoring Active", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
        Text("Paired with Parent: $pairCode", color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f))
        
        Spacer(modifier = Modifier.height(32.dp))
        Card(
            modifier = Modifier.fillMaxWidth().animateContentSize(),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Current Parent Commands:", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.height(8.dp))
                Text("Wi-Fi: ${if(deviceConfig.wifi) "ON" else "OFF"}", color = MaterialTheme.colorScheme.onSurface)
                Text("Bluetooth: ${if(deviceConfig.bluetooth) "ON" else "OFF"}", color = MaterialTheme.colorScheme.onSurface)
                Text("Flashlight: ${if(deviceConfig.flashlight) "ON" else "OFF"}", color = MaterialTheme.colorScheme.onSurface)
                Text("Hotspot: ${if(deviceConfig.hotspot) "ON" else "OFF"}", color = MaterialTheme.colorScheme.onSurface)
                Text("Aeroplane Mode: ${if(deviceConfig.aeroplaneMode) "ON" else "OFF"}", color = MaterialTheme.colorScheme.onSurface)
                
                val ringerText = when(deviceConfig.ringerMode) {
                    0 -> "SILENT"
                    1 -> "VIBRATE"
                    else -> "NORMAL"
                }
                Text("Ringer Mode: $ringerText", color = MaterialTheme.colorScheme.onSurface)
                Text("Volume: ${deviceConfig.volume}%", color = MaterialTheme.colorScheme.onSurface)
                Text("Brightness: ${deviceConfig.brightness}%", color = MaterialTheme.colorScheme.onSurface)

                Text("Lock Screen: ${if(deviceConfig.lock) "LOCKED" else "UNLOCKED"}", color = if(deviceConfig.lock) Color.Red else MaterialTheme.colorScheme.onSurface)
                if (deviceConfig.screenshotRequested) {
                    Text("Screenshot: PENDING CAPTURE", color = Color(0xFFFFA000))
                }
            }
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text("Simulate Activity", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
        Spacer(modifier = Modifier.height(8.dp))
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
            Button(onClick = { onSendMockNotification("WhatsApp", "New message from friend!") }, modifier = Modifier.weight(1f).padding(end = 4.dp)) {
                Text("WhatsApp")
            }
            Button(onClick = { onSendMockNotification("Instagram", "john_doe liked your post") }, modifier = Modifier.weight(1f).padding(horizontal = 4.dp)) {
                Text("Instagram")
            }
        }
        Row(modifier = Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.SpaceEvenly) {
            Button(onClick = { onSendMockNotification("System", "Missed call from +1 234 567 8900") }, modifier = Modifier.weight(1f).padding(end = 4.dp)) {
                Text("Missed Call")
            }
            Button(onClick = { onSendMockNotification("Chrome", "Blocked access to restricted site") }, modifier = Modifier.weight(1f).padding(horizontal = 4.dp)) {
                Text("Web Blocked")
            }
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        TextButton(onClick = onDisconnect) {
            Text("Stop Monitoring (Disconnect)", color = Color(0xFFFF5252), fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun UseCaseCard(title: String, onClick: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .background(MaterialTheme.colorScheme.surfaceVariant),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(modifier = Modifier
            .height(120.dp)
            .fillMaxWidth(), contentAlignment = Alignment.Center) {
             Text("Illustration", color = MaterialTheme.colorScheme.primary)
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(MaterialTheme.colorScheme.primary)
                .padding(12.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(title, color = MaterialTheme.colorScheme.onPrimary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
        }
    }
}

@Composable
fun RoleSelectionScreen(onRoleSelected: (String) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(16.dp))
        Text("Who Uses This Device?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
        
        Spacer(modifier = Modifier.height(48.dp))
        
        UseCaseCard(title = "Parent", onClick = { onRoleSelected("parent") })
        Spacer(modifier = Modifier.height(32.dp))
        UseCaseCard(title = "Child", onClick = { onRoleSelected("child") })
    }
}

@OptIn(com.google.accompanist.permissions.ExperimentalPermissionsApi::class)
@Composable
fun PermissionScreen(role: String, onPermissionsGranted: () -> Unit) {
    if (role == "parent") {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text("Parent Setup", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(32.dp))
            Button(onClick = onPermissionsGranted, modifier = Modifier.fillMaxWidth().height(50.dp)) {
                Text("Continue to Pairing")
            }
        }
        return
    }

    val context = androidx.compose.ui.platform.LocalContext.current
    var notifGranted by remember { mutableStateOf(androidx.core.app.NotificationManagerCompat.getEnabledListenerPackages(context).contains(context.packageName)) }
    var adminGranted by remember { mutableStateOf(
        (context.getSystemService(android.content.Context.DEVICE_POLICY_SERVICE) as android.app.admin.DevicePolicyManager)
        .isAdminActive(android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java))
    ) }
    var accessGranted by remember { mutableStateOf(
        try {
            android.provider.Settings.Secure.getInt(context.contentResolver, android.provider.Settings.Secure.ACCESSIBILITY_ENABLED) == 1
        } catch (e: Exception) { false }
    ) }
    var overlayGranted by remember { mutableStateOf(android.provider.Settings.canDrawOverlays(context)) }

    androidx.compose.runtime.LaunchedEffect(Unit) {
        while(true) {
            notifGranted = androidx.core.app.NotificationManagerCompat.getEnabledListenerPackages(context).contains(context.packageName)
            adminGranted = (context.getSystemService(android.content.Context.DEVICE_POLICY_SERVICE) as android.app.admin.DevicePolicyManager)
                .isAdminActive(android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java))
            accessGranted = try {
                android.provider.Settings.Secure.getInt(context.contentResolver, android.provider.Settings.Secure.ACCESSIBILITY_ENABLED) == 1
            } catch (e: Exception) { false }
            overlayGranted = android.provider.Settings.canDrawOverlays(context)
            kotlinx.coroutines.delay(1000)
        }
    }

    val locationPermissionState = com.google.accompanist.permissions.rememberMultiplePermissionsState(
        permissions = listOf(
            android.Manifest.permission.ACCESS_FINE_LOCATION,
            android.Manifest.permission.ACCESS_COARSE_LOCATION
        )
    )
    val cameraPermissionState = com.google.accompanist.permissions.rememberMultiplePermissionsState(
        permissions = listOf(
            android.Manifest.permission.CAMERA,
            android.Manifest.permission.RECORD_AUDIO
        )
    )

    val allGranted = notifGranted && adminGranted && accessGranted && locationPermissionState.allPermissionsGranted && cameraPermissionState.allPermissionsGranted && overlayGranted
    var showWarning by remember { mutableStateOf(false) }

    androidx.compose.runtime.LaunchedEffect(allGranted) {
        if (allGranted) {
            onPermissionsGranted()
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Required Permissions",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)
        )
        Text(
            text = "Please allow all permissions for full functionality and security.",
            fontSize = 14.sp,
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f),
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        LazyColumn(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            item {
                PermissionItem(
                    title = "Notification Access",
                    description = "Required to sync notifications to parent.",
                    isGranted = notifGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); notifGranted = true }
                    }
                )
            }
            item {
                PermissionItem(
                    title = "Device Administrator",
                    description = "Required to lock/wipe device remotely.",
                    isGranted = adminGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.app.admin.DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN).apply { putExtra(android.app.admin.DevicePolicyManager.EXTRA_DEVICE_ADMIN, android.content.ComponentName(context, com.example.services.MyAdminReceiver::class.java)) }
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); adminGranted = true }
                    }
                )
            }
            item {
                PermissionItem(
                    title = "Accessibility Service",
                    description = "Required for app limits and web filtering.",
                    isGranted = accessGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_ACCESSIBILITY_SETTINGS)
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); accessGranted = true }
                    }
                )
            }
            item {
                PermissionItem(
                    title = "Location Access",
                    description = "Required for real-time location tracking.",
                    isGranted = locationPermissionState.allPermissionsGranted,
                    onGrant = { locationPermissionState.launchMultiplePermissionRequest() }
                )
            }
            item {
                PermissionItem(
                    title = "Camera & Microphone",
                    description = "Required for remote camera and ambient audio.",
                    isGranted = cameraPermissionState.allPermissionsGranted,
                    onGrant = { cameraPermissionState.launchMultiplePermissionRequest() }
                )
            }
            item {
                PermissionItem(
                    title = "Display over other apps",
                    description = "Required for app lock screen overlays.",
                    isGranted = overlayGranted,
                    onGrant = { 
                        val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION, android.net.Uri.parse("package:" + context.packageName))
                        try { context.startActivity(intent) } catch(e: Exception) { android.widget.Toast.makeText(context, "Not available on this device", android.widget.Toast.LENGTH_SHORT).show(); overlayGranted = true }
                    }
                )
            }
        }

        if (showWarning) {
            Text(
                "You must allow ALL permissions to continue.",
                color = Color.Red,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(vertical = 8.dp)
            )
        }

        Button(
            onClick = {
                if (allGranted) {
                    onPermissionsGranted()
                } else {
                    showWarning = true
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp)
                .height(50.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = if (allGranted) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                contentColor = if (allGranted) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
            )
        ) {
            Text("Continue")
        }
    }
}

@Composable
fun PermissionItem(title: String, description: String, isGranted: Boolean, onGrant: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f).padding(end = 16.dp)) {
                Text(title, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                Text(description, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f))
            }
            if (isGranted) {
                Icon(Icons.Default.Done, contentDescription = "Granted", tint = Color(0xFF4CAF50))
            } else {
                Button(onClick = onGrant, contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp)) {
                    Text("Allow")
                }
            }
        }
    }
}

@Composable
fun ShareNotificationScreen(role: String, viewModel: AppViewModel, onPaired: () -> Unit) {
    var acceptedTerms by remember { mutableStateOf(false) }
    val pairCode = remember { viewModel.generatePairCode() }
    var enteredCode by remember { mutableStateOf("") }
    val context = androidx.compose.ui.platform.LocalContext.current
    val qrLauncher = rememberLauncherForActivityResult(com.journeyapps.barcodescanner.ScanContract()) { result ->
        if (result.contents != null) {
            enteredCode = result.contents
        }
    }
    if (!acceptedTerms) {
        AlertDialog(
            onDismissRequest = { },
            title = { Text("Read Carefully", textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth(), fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text("1. This app uses third party(Firebase) services to share Notifications. End-to-end encryption ensures only you can read and nobody in between.")
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("2. You are responsible for your Child notifications.")
                }
            },
            confirmButton = {
                Button(
                    onClick = { acceptedTerms = true },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text("Accept", color = MaterialTheme.colorScheme.onPrimary)
                }
            },
            containerColor = MaterialTheme.colorScheme.surface
        )
    }
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(16.dp))
        Text(if (role == "parent") "Get Child's Notification" else "Share Notification", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
        Spacer(modifier = Modifier.height(24.dp))
        Card(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            shape = RoundedCornerShape(16.dp)
        ) {
            Column(
                modifier = Modifier.padding(24.dp).fillMaxWidth(),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                if (role == "child") {
                    val qrBitmap = remember(pairCode) { generateQrBitmap(pairCode) }
                    if (qrBitmap != null) {
                        Image(
                            bitmap = qrBitmap.asImageBitmap(),
                            contentDescription = "QR Code",
                            modifier = Modifier.size(150.dp)
                        )
                    } else {
                        Box(
                            modifier = Modifier.size(120.dp).background(MaterialTheme.colorScheme.surfaceVariant),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("QR CODE", color = MaterialTheme.colorScheme.onSurface)
                        }
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Your Pair Code: $pairCode", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                    Text("Code expires in 10 mins", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f))
                } else {
                    Button(onClick = {
                        val options = com.journeyapps.barcodescanner.ScanOptions()
                        options.setDesiredBarcodeFormats(com.journeyapps.barcodescanner.ScanOptions.QR_CODE)
                        options.setPrompt("Scan Child's QR Code")
                        options.setBeepEnabled(true)
                        options.setOrientationLocked(false)
                        qrLauncher.launch(options)
                    }, modifier = Modifier.fillMaxWidth().height(60.dp)) {
                        Text("Scan QR Code", fontSize = 18.sp)
                    }
                }
            }
        }
        if (role == "parent") {
            Spacer(modifier = Modifier.height(16.dp))
            Text("OR", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Enter code of Child's Device", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = enteredCode,
                onValueChange = { if (it.length <= 10) enteredCode = it.uppercase() },
                placeholder = { Text("10-Digit Code", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)) },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp),
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = MaterialTheme.colorScheme.onBackground,
                    unfocusedTextColor = MaterialTheme.colorScheme.onBackground,
                )
            )
            Spacer(modifier = Modifier.height(24.dp))
        }

        val scope = androidx.compose.runtime.rememberCoroutineScope()
        var isVerifying by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
        var showPairingConfirmDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }

        androidx.compose.runtime.LaunchedEffect(role, pairCode) {
            if (role == "child") {
                val initErr = viewModel.initDeviceConfig(pairCode)
                if (initErr != null) {
                    android.widget.Toast.makeText(context, "Firebase DB Error on Child: $initErr", android.widget.Toast.LENGTH_LONG).show()
                }
                launch {
                    viewModel.requestPairing(pairCode).collect { config ->
                        if (config?.pairingRequested == true && config.pairingAccepted == false) {
                            showPairingConfirmDialog = true
                        }
                    }
                }
            }
        }

        if (showPairingConfirmDialog) {
            AlertDialog(
                onDismissRequest = { },
                title = { Text("Pairing Request") },
                text = { Text("A parent device wants to connect to this device. Allow?") },
                confirmButton = {
                    Button(onClick = {
                        scope.launch {
                            viewModel.setPairingRequest(pairCode, requested = true, accepted = true)
                            viewModel.pairDevice(role, pairCode)
                            onPaired()
                            val apps = getInstalledApps(context)
                            viewModel.updateInstalledApps(apps)
                        }
                        showPairingConfirmDialog = false
                    }) {
                        Text("Accept")
                    }
                },
                dismissButton = {
                    Button(onClick = {
                        scope.launch {
                            viewModel.setPairingRequest(pairCode, requested = false, accepted = false)
                        }
                        showPairingConfirmDialog = false
                    }) {
                        Text("Reject")
                    }
                }
            )
        }

        if (role == "parent") {
            Button(
                onClick = {
                    val codeToUse = enteredCode
                    isVerifying = true
                    scope.launch {
                        val (isValid, errorMsg) = viewModel.verifyPairCode(codeToUse)
                        if (isValid) {
                            try {
                                viewModel.setPairingRequest(codeToUse, requested = true, accepted = false)
                            } catch (e: Exception) {
                                isVerifying = false
                                android.widget.Toast.makeText(context, "Pairing request failed: ${e.message}", android.widget.Toast.LENGTH_LONG).show()
                                return@launch
                            }
                            scope.launch {
                                viewModel.requestPairing(codeToUse).collect { config ->
                                    if (config?.pairingAccepted == true) {
                                        viewModel.pairDevice(role, codeToUse)
                                        onPaired()
                                    } else if (config?.pairingRequested == false) {
                                        isVerifying = false
                                        // Wait until user triggers again
                                    }
                                }
                            }
                        } else {
                            isVerifying = false
                            if (errorMsg != null) {
                                android.widget.Toast.makeText(context, "Firebase Error: $errorMsg", android.widget.Toast.LENGTH_LONG).show()
                            } else {
                                android.widget.Toast.makeText(context, "Invalid Code! Child must open app and show code first.", android.widget.Toast.LENGTH_LONG).show()
                            }
                        }
                    }
                },
                modifier = Modifier.width(200.dp).height(48.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                enabled = !isVerifying && enteredCode.length == 10
            ) {
                Text(if (isVerifying) "Waiting for approval..." else "Pair", color = MaterialTheme.colorScheme.onPrimary)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyNotificationsScreen(viewModel: AppViewModel, onBack: () -> Unit) {
    val notificationLogs by viewModel.notificationLogs.collectAsStateWithLifecycle()
    val dateFormat = SimpleDateFormat("HH:mm - MMM dd", Locale.getDefault())

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("My Notifications", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onSurface)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(padding),
            contentAlignment = Alignment.Center
        ) {
            if (notificationLogs.isEmpty()) {
                Text("Notification Log is Empty", color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f), fontSize = 16.sp)
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(notificationLogs) { log ->
                        Card(
                            modifier = Modifier.fillMaxWidth().animateContentSize(),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Text(log.appName, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                                    Text(dateFormat.format(Date(log.timestamp)), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f))
                                }
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(log.content, color = MaterialTheme.colorScheme.onSurface)
                            }
                        }
                    }
                }
            }
        }
    }
}
