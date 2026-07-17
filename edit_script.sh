#!/bin/bash
sed -i '/fun ShareNotificationScreen/,/MyNotificationsScreen(viewModel/c\
@Composable\
fun ShareNotificationScreen(role: String, viewModel: AppViewModel, onPaired: () -> Unit) {\
    var acceptedTerms by remember { mutableStateOf(false) }\
    val pairCode = remember { viewModel.generatePairCode() }\
    var enteredCode by remember { mutableStateOf("") }\
    val context = androidx.compose.ui.platform.LocalContext.current\
    val qrLauncher = rememberLauncherForActivityResult(com.journeyapps.barcodescanner.ScanContract()) { result ->\
        if (result.contents != null) {\
            enteredCode = result.contents\
        }\
    }\
    if (!acceptedTerms) {\
        AlertDialog(\
            onDismissRequest = { },\
            title = { Text("Read Carefully", textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth(), fontWeight = FontWeight.Bold) },\
            text = {\
                Column {\
                    Text("1. This app uses third party(Firebase) services to share Notifications. End-to-end encryption ensures only you can read and nobody in between.")\
                    Spacer(modifier = Modifier.height(8.dp))\
                    Text("2. You are responsible for your Child notifications.")\
                }\
            },\
            confirmButton = {\
                Button(\
                    onClick = { acceptedTerms = true },\
                    modifier = Modifier.fillMaxWidth(),\
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)\
                ) {\
                    Text("Accept", color = MaterialTheme.colorScheme.onPrimary)\
                }\
            },\
            containerColor = MaterialTheme.colorScheme.surface\
        )\
    }\
    Column(\
        modifier = Modifier\
            .fillMaxSize()\
            .background(MaterialTheme.colorScheme.background)\
            .padding(16.dp),\
        horizontalAlignment = Alignment.CenterHorizontally\
    ) {\
        Spacer(modifier = Modifier.height(16.dp))\
        Text(if (role == "child") "Get Child'\''s Notification" else "Share Notification", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)\
        Spacer(modifier = Modifier.height(24.dp))\
        Card(\
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),\
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),\
            shape = RoundedCornerShape(16.dp)\
        ) {\
            Column(\
                modifier = Modifier.padding(24.dp).fillMaxWidth(),\
                horizontalAlignment = Alignment.CenterHorizontally\
            ) {\
                if (role == "child") {\
                    val qrBitmap = remember(pairCode) { generateQrBitmap(pairCode) }\
                    if (qrBitmap != null) {\
                        Image(\
                            bitmap = qrBitmap.asImageBitmap(),\
                            contentDescription = "QR Code",\
                            modifier = Modifier.size(150.dp)\
                        )\
                    } else {\
                        Box(\
                            modifier = Modifier.size(120.dp).background(MaterialTheme.colorScheme.surfaceVariant),\
                            contentAlignment = Alignment.Center\
                        ) {\
                            Text("QR CODE", color = MaterialTheme.colorScheme.onSurface)\
                        }\
                    }\
                    Spacer(modifier = Modifier.height(16.dp))\
                    Text("Your Pair Code: $pairCode", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp)\
                    Text("Code expires in 10 mins", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f))\
                } else {\
                    Button(onClick = {\
                        val options = com.journeyapps.barcodescanner.ScanOptions()\
                        options.setDesiredBarcodeFormats(com.journeyapps.barcodescanner.ScanOptions.QR_CODE)\
                        options.setPrompt("Scan Child'\''s QR Code")\
                        options.setBeepEnabled(true)\
                        options.setOrientationLocked(false)\
                        qrLauncher.launch(options)\
                    }, modifier = Modifier.fillMaxWidth().height(60.dp)) {\
                        Text("Scan QR Code", fontSize = 18.sp)\
                    }\
                }\
            }\
        }\
        Spacer(modifier = Modifier.height(16.dp))\
        Text("OR", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)\
        Spacer(modifier = Modifier.height(16.dp))\
        Text("Enter code of Child'\''s Device", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)\
        Spacer(modifier = Modifier.height(16.dp))\
        OutlinedTextField(\
            value = enteredCode,\
            onValueChange = { if (it.length <= 6) enteredCode = it.uppercase() },\
            placeholder = { Text("6-Digit Code", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)) },\
            modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp),\
            singleLine = true,\
            colors = OutlinedTextFieldDefaults.colors(\
                focusedTextColor = MaterialTheme.colorScheme.onBackground,\
                unfocusedTextColor = MaterialTheme.colorScheme.onBackground,\
            )\
        )\
        Spacer(modifier = Modifier.height(24.dp))\
        Button(\
            onClick = {\
                val codeToUse = if (role == "child") pairCode else enteredCode\
                viewModel.pairDevice(role, codeToUse)\
                onPaired()\
            },\
            modifier = Modifier.width(120.dp).height(48.dp),\
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),\
            enabled = role == "child" || enteredCode.length == 6\
        ) {\
            Text("Pair", color = MaterialTheme.colorScheme.onPrimary)\
        }\
    }\
}\
\
@OptIn(ExperimentalMaterial3Api::class)\
@Composable\
fun MyNotificationsScreen(viewModel' app/src/main/java/com/example/ui/screens/MainScreens.kt
