import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """    if (hasParentRole) {
        LaunchedEffect(Unit) {
            onNavigateToParentDashboard()
        }
    } else if (pairedDevice != null && pairedDevice.isConnected) {
        ChildDashboard(
            pairCode = pairedDevice.pairCode,
            deviceConfig = deviceConfig,
            onSendMockNotification = { app, msg -> viewModel.sendNotification(app, msg) },
            onUpdateAppStatus = { updatedApps -> viewModel.updateConfig(deviceConfig.copy(installedApps = updatedApps)) },
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
            val user = try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }
            if (user?.email != null) {
                Text(
                    text = "Signed in as: ${user.email}",
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    modifier = Modifier.align(Alignment.End)
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text("Who Uses This Device?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            
            Spacer(modifier = Modifier.height(48.dp))
            
            UseCaseCard(title = "Parent", onClick = { onNavigateToRole("parent") })
            Spacer(modifier = Modifier.height(32.dp))
            UseCaseCard(title = "Child", onClick = { onNavigateToRole("child") })
            
            Spacer(modifier = Modifier.weight(1f))
        }
    }"""

replacement = """    // We show the dashboard if child is paired, BUT the user requested "direct show karo button Parents or child's" 
    // on the home page. So we will always show the selection column.
    // If they already have a role, the button will take them to their dashboard instead of pairing.

    var activeChildView by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }

    if (activeChildView && pairedDevice != null && pairedDevice.isConnected) {
        ChildDashboard(
            pairCode = pairedDevice.pairCode,
            deviceConfig = deviceConfig,
            onSendMockNotification = { app, msg -> viewModel.sendNotification(app, msg) },
            onUpdateAppStatus = { updatedApps -> viewModel.updateConfig(deviceConfig.copy(installedApps = updatedApps)) },
            onDisconnect = {
                activeChildView = false
                onDisconnect()
            }
        )
    } else {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            val user = try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }
            if (user?.email != null) {
                Text(
                    text = "Signed in as: ${user.email}",
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    modifier = Modifier.align(Alignment.End)
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text("Who Uses This Device?", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            
            Spacer(modifier = Modifier.height(48.dp))
            
            if (hasParentRole) {
                UseCaseCard(title = "Parent Dashboard", onClick = { onNavigateToParentDashboard() })
            } else {
                UseCaseCard(title = "Parent", onClick = { onNavigateToRole("parent") })
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            if (pairedDevice != null && pairedDevice.isConnected) {
                UseCaseCard(title = "Child Dashboard", onClick = { activeChildView = true })
            } else {
                UseCaseCard(title = "Child", onClick = { onNavigateToRole("child") })
            }
            
            Spacer(modifier = Modifier.weight(1f))
        }
    }"""
content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
