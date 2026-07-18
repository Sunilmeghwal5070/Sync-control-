import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """fun ShareNotificationScreen(role: String, viewModel: AppViewModel, onPaired: () -> Unit, onBack: () -> Unit) {
    var acceptedTerms by remember { mutableStateOf(false) }
    var pairCode by remember { mutableStateOf(viewModel.generatePairCode()) }
    var enteredCode by remember { mutableStateOf("") }
    val context = androidx.compose.ui.platform.LocalContext.current
    val qrLauncher = rememberLauncherForActivityResult(com.journeyapps.barcodescanner.ScanContract()) { result ->
        if (result.contents != null) {
            enteredCode = result.contents
        }
    }
    // Removed blocking dialog to prevent trapping user.
    // Let system handle back button naturally.
    
    Column("""

replacement = """fun ShareNotificationScreen(role: String, viewModel: AppViewModel, onPaired: () -> Unit, onBack: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val sharedPrefs = remember { context.getSharedPreferences("app_prefs", android.content.Context.MODE_PRIVATE) }
    var acceptedTerms by remember { mutableStateOf(sharedPrefs.getBoolean("accepted_terms", false)) }
    
    var isGenerating by remember { mutableStateOf(false) }
    var cooldownSeconds by remember { mutableStateOf(0) }
    val scope = rememberCoroutineScope()
    
    var pairCode by remember { mutableStateOf(viewModel.generatePairCode()) }
    var enteredCode by remember { mutableStateOf("") }
    
    val qrLauncher = rememberLauncherForActivityResult(com.journeyapps.barcodescanner.ScanContract()) { result ->
        if (result.contents != null) {
            enteredCode = result.contents
        }
    }
    
    LaunchedEffect(cooldownSeconds) {
        if (cooldownSeconds > 0) {
            kotlinx.coroutines.delay(1000)
            cooldownSeconds--
        }
    }
    
    if (!acceptedTerms) {
        androidx.activity.compose.BackHandler { onBack() }
        AlertDialog(
            onDismissRequest = onBack,
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
                    onClick = { 
                        sharedPrefs.edit().putBoolean("accepted_terms", true).apply()
                        acceptedTerms = true 
                    },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text("Accept", color = MaterialTheme.colorScheme.onPrimary)
                }
            },
            dismissButton = {
                TextButton(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
                    Text("Decline", color = MaterialTheme.colorScheme.onSurface)
                }
            },
            containerColor = MaterialTheme.colorScheme.surface
        )
    } else {
        androidx.activity.compose.BackHandler { onBack() }
    }
    
    Column("""

content = content.replace(target, replacement)

target_refresh = """                        Button(
                            onClick = {
                                pairCode = viewModel.refreshPairCode()
                            },
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 8.dp)
                        ) {
                            Icon(Icons.Default.Refresh, contentDescription = "Refresh", modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("Refresh")
                        }"""

replacement_refresh = """                        Button(
                            onClick = {
                                if (cooldownSeconds == 0) {
                                    scope.launch {
                                        isGenerating = true
                                        kotlinx.coroutines.delay(1500) // Loading animation duration
                                        pairCode = viewModel.refreshPairCode()
                                        isGenerating = false
                                        cooldownSeconds = 60
                                    }
                                } else {
                                    android.widget.Toast.makeText(context, "Please wait $cooldownSeconds seconds", android.widget.Toast.LENGTH_SHORT).show()
                                }
                            },
                            enabled = cooldownSeconds == 0 && !isGenerating,
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 8.dp)
                        ) {
                            if (isGenerating) {
                                CircularProgressIndicator(modifier = Modifier.size(18.dp), color = MaterialTheme.colorScheme.onPrimary, strokeWidth = 2.dp)
                            } else {
                                Icon(Icons.Default.Refresh, contentDescription = "Refresh", modifier = Modifier.size(18.dp))
                            }
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(if (cooldownSeconds > 0) "${cooldownSeconds}s" else "Refresh")
                        }"""

content = content.replace(target_refresh, replacement_refresh)

target_qr = """                    val qrBitmap = remember(pairCode) { generateQrBitmap(pairCode) }
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
                    Text("Your Pair Code: $pairCode", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)"""

replacement_qr = """                    val qrBitmap = remember(pairCode) { generateQrBitmap(pairCode) }
                    if (isGenerating) {
                        Box(
                            modifier = Modifier.size(150.dp).background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(16.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Generating...", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                    } else if (qrBitmap != null) {
                        Image(
                            bitmap = qrBitmap.asImageBitmap(),
                            contentDescription = "QR Code",
                            modifier = Modifier.size(150.dp)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Your Pair Code: $pairCode", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                    } else {
                        Box(
                            modifier = Modifier.size(120.dp).background(MaterialTheme.colorScheme.surfaceVariant),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("QR CODE", color = MaterialTheme.colorScheme.onSurface)
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Your Pair Code: $pairCode", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)
                    }"""

content = content.replace(target_qr, replacement_qr)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
