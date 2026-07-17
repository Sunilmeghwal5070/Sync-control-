package com.example.ui.screens

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.DeviceConfig

data class DashboardItem(
    val title: String,
    val icon: ImageVector,
    val route: String
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ParentDashboardScreen(
    allDevices: List<com.example.data.PairedDevice>,
    selectedPairCode: String?,
    deviceConfig: com.example.data.DeviceConfig,
    onSelectDevice: (String) -> Unit,
    onNavigate: (String) -> Unit,
    onDisconnect: (String) -> Unit,
    onAddDevice: () -> Unit
) {
    var expanded by remember { androidx.compose.runtime.mutableStateOf(false) }
    val selectedDevice = allDevices.find { it.pairCode == selectedPairCode }

    val items = listOf(
        DashboardItem("Device Controls", Icons.Default.Settings, "device_controls"),
        DashboardItem("Location Tracking", Icons.Default.LocationOn, "location_tracking"),
        DashboardItem("App Hider & Limit", Icons.Default.Lock, "restrictions"),
        DashboardItem("Security & Actions", Icons.Default.Security, "security"),
        DashboardItem("Notification Sync", Icons.Default.Notifications, "my_notifications")
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Box {
                            Column {
                                val user = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
                                if (user != null) {
                                    Text(user.email ?: "", fontSize = 10.sp, color = MaterialTheme.colorScheme.primary)
                                }
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    modifier = Modifier.clickable { expanded = true }
                                ) {
                                    Text(selectedDevice?.deviceName ?: "Select Device", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                                    Icon(Icons.Default.ArrowDropDown, contentDescription = "Select Device", tint = MaterialTheme.colorScheme.onSurface)
                                }
                                if (selectedDevice != null) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(Icons.Default.BatteryFull, contentDescription = "Battery", tint = Color(0xFF4CAF50), modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(4.dp))
                                        Text("${deviceConfig.batteryLevel}%", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f))
                                    }
                                }
                            }
                        DropdownMenu(
                            expanded = expanded,
                            onDismissRequest = { expanded = false }
                        ) {
                            allDevices.forEach { device ->
                                DropdownMenuItem(
                                    text = { Text(device.deviceName) },
                                    onClick = {
                                        onSelectDevice(device.pairCode)
                                        expanded = false
                                    }
                                )
                            }
                            HorizontalDivider()
                            DropdownMenuItem(
                                text = { Text("Add Another Device", color = MaterialTheme.colorScheme.primary) },
                                onClick = {
                                    expanded = false
                                    onAddDevice()
                                }
                            )
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(padding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (selectedDevice != null) {
                Text("Connected to: ${selectedDevice.pairCode}", color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f))
                
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center,
                    modifier = Modifier.padding(bottom = 16.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Settings, // Placeholder for battery icon
                        contentDescription = "Battery",
                        tint = if (deviceConfig.batteryLevel > 20) MaterialTheme.colorScheme.primary else Color.Red,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Battery: ${deviceConfig.batteryLevel}%",
                        color = MaterialTheme.colorScheme.onBackground,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                LazyVerticalGrid(
                    columns = GridCells.Fixed(2),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    items(items) { item ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .aspectRatio(1f)
                                .clip(RoundedCornerShape(16.dp))
                                .clickable { onNavigate(item.route) },
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Column(
                                modifier = Modifier.fillMaxSize(),
                                horizontalAlignment = Alignment.CenterHorizontally,
                                verticalArrangement = Arrangement.Center
                            ) {
                                Icon(item.icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(48.dp))
                                Spacer(modifier = Modifier.height(16.dp))
                                Text(item.title, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp, modifier = Modifier.padding(horizontal = 8.dp), maxLines = 2, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                TextButton(onClick = { onDisconnect(selectedDevice.pairCode) }) {
                    Text("Disconnect ${selectedDevice.deviceName}", color = Color(0xFFFF5252), fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
            } else {
                Text("No device selected.", color = MaterialTheme.colorScheme.onBackground)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DeviceControlsScreen(
    deviceConfig: DeviceConfig,
    onConfigChanged: (DeviceConfig) -> Unit,
    onBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Device Controls") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Wi-Fi", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.wifi, onCheckedChange = { onConfigChanged(deviceConfig.copy(wifi = it)) })
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.surfaceVariant)

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Bluetooth", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.bluetooth, onCheckedChange = { onConfigChanged(deviceConfig.copy(bluetooth = it)) })
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.surfaceVariant)

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Flashlight", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.flashlight, onCheckedChange = { onConfigChanged(deviceConfig.copy(flashlight = it)) })
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.surfaceVariant)

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Hotspot", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.hotspot, onCheckedChange = { onConfigChanged(deviceConfig.copy(hotspot = it)) })
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.surfaceVariant)

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Aeroplane Mode", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.aeroplaneMode, onCheckedChange = { onConfigChanged(deviceConfig.copy(aeroplaneMode = it)) })
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.surfaceVariant)
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Battery Saver", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.batterySaver, onCheckedChange = { onConfigChanged(deviceConfig.copy(batterySaver = it)) })
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.surfaceVariant)
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Do Not Disturb", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.dndMode, onCheckedChange = { onConfigChanged(deviceConfig.copy(dndMode = it)) })
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }

            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Audio Controls", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(bottom = 8.dp))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                            Button(onClick = { onConfigChanged(deviceConfig.copy(ringerMode = 0)) }, colors = ButtonDefaults.buttonColors(containerColor = if (deviceConfig.ringerMode == 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)) { Text("Silent", color = if(deviceConfig.ringerMode == 0) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface) }
                            Button(onClick = { onConfigChanged(deviceConfig.copy(ringerMode = 1)) }, colors = ButtonDefaults.buttonColors(containerColor = if (deviceConfig.ringerMode == 1) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)) { Text("Vibrate", color = if(deviceConfig.ringerMode == 1) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface) }
                            Button(onClick = { onConfigChanged(deviceConfig.copy(ringerMode = 2)) }, colors = ButtonDefaults.buttonColors(containerColor = if (deviceConfig.ringerMode == 2) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)) { Text("Normal", color = if(deviceConfig.ringerMode == 2) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface) }
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Volume: ${deviceConfig.volume}%", color = MaterialTheme.colorScheme.onSurface)
                        Slider(
                            value = deviceConfig.volume.toFloat(),
                            onValueChange = { onConfigChanged(deviceConfig.copy(volume = it.toInt())) },
                            valueRange = 0f..100f
                        )
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
            
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Display Controls", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(bottom = 8.dp))
                        Text("Brightness: ${deviceConfig.brightness}%", color = MaterialTheme.colorScheme.onSurface)
                        Slider(
                            value = deviceConfig.brightness.toFloat(),
                            onValueChange = { onConfigChanged(deviceConfig.copy(brightness = it.toInt())) },
                            valueRange = 0f..100f
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Text("Screen Timeout (Seconds): ${deviceConfig.screenTimeout}", color = MaterialTheme.colorScheme.onSurface)
                        Slider(
                            value = deviceConfig.screenTimeout.toFloat(),
                            onValueChange = { onConfigChanged(deviceConfig.copy(screenTimeout = it.toInt())) },
                            valueRange = 15f..300f
                        )
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LocationScreen(deviceConfig: DeviceConfig, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Location Tracking") },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back") }
                }
            )
        }
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp)) {
            Card(modifier = Modifier.fillMaxWidth().weight(1f), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Default.Map, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(100.dp))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Live Map View", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                        Text("(Map Integration Placeholder)", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f))
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Current Coordinates", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("Latitude: ${deviceConfig.location.lat}", color = MaterialTheme.colorScheme.onSurface)
                    Text("Longitude: ${deviceConfig.location.lng}", color = MaterialTheme.colorScheme.onSurface)
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { /* Refresh */ }, modifier = Modifier.fillMaxWidth()) {
                        Text("Refresh Location")
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RestrictionsScreen(deviceConfig: DeviceConfig, onConfigChanged: (DeviceConfig) -> Unit, onBack: () -> Unit) {
    var showAppLockDialog by remember { mutableStateOf(false) }
    var showAppHideDialog by remember { mutableStateOf(false) }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("App Hider & Restrictions") },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back") }
                }
            )
        }
    ) { padding ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp)) {
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("App Hider & Lock", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                        Text("Select apps to hide or lock on child's device.", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f), fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = { showAppLockDialog = true }, modifier = Modifier.fillMaxWidth()) { Text("Manage App Locks") }
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = { showAppHideDialog = true }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) { Text("Manage Hidden Apps", color = MaterialTheme.colorScheme.onSurface) }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Web Filtering & Blocking", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                        Text("Block websites and domains.", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f), fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = {}, modifier = Modifier.fillMaxWidth()) { Text("Manage Blocked Websites") }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
        
        if (showAppLockDialog) {
            AppSelectionDialog(
                title = "Lock Apps",
                apps = deviceConfig.installedApps,
                isHiding = false,
                onToggle = { app, isLocked ->
                    val newApps = deviceConfig.installedApps.map {
                        if (it.packageName == app.packageName) it.copy(isLocked = isLocked) else it
                    }
                    onConfigChanged(deviceConfig.copy(installedApps = newApps))
                },
                onDismiss = { showAppLockDialog = false }
            )
        }
        if (showAppHideDialog) {
            AppSelectionDialog(
                title = "Hide Apps",
                apps = deviceConfig.installedApps,
                isHiding = true,
                onToggle = { app, isHidden ->
                    val newApps = deviceConfig.installedApps.map {
                        if (it.packageName == app.packageName) it.copy(isHidden = isHidden) else it
                    }
                    onConfigChanged(deviceConfig.copy(installedApps = newApps))
                },
                onDismiss = { showAppHideDialog = false }
            )
        }
    }
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SecurityScreen(deviceConfig: DeviceConfig, onConfigChanged: (DeviceConfig) -> Unit, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Security & Actions") },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back") }
                }
            )
        }
    ) { padding ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp)) {
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Hardware Access", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Camera Access", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.cameraAccess, onCheckedChange = { onConfigChanged(deviceConfig.copy(cameraAccess = it)) })
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.surfaceVariant)

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Microphone Access", color = MaterialTheme.colorScheme.onSurface)
                            Switch(checked = deviceConfig.microphoneAccess, onCheckedChange = { onConfigChanged(deviceConfig.copy(microphoneAccess = it)) })
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
            item {
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Remote Actions", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Button(
                            onClick = { onConfigChanged(deviceConfig.copy(lock = !deviceConfig.lock)) },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = if (deviceConfig.lock) Color.Red else MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Text(if (deviceConfig.lock) "Unlock Device" else "Lock Device", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                        }
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Button(
                            onClick = { onConfigChanged(deviceConfig.copy(screenshotRequested = true)) },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Text("Capture Screenshot", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}
