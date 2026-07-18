package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

@Composable
fun LoginScreen(onLoginSuccess: () -> Unit) {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    var isLoading by remember { mutableStateOf(false) }

    // Check if already logged in
    LaunchedEffect(Unit) {
        val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
        if (auth.currentUser != null) {
            onLoginSuccess()
        } else {
            // Auto login anonymously
            try {
                auth.signInAnonymously().await()
                onLoginSuccess()
            } catch (e: Exception) {
                // If it fails, maybe internet issue or anonymous auth is disabled
            }
        }
    }

    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.padding(32.dp)
        ) {
            Text(
                "Welcome to Sync Control",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(32.dp))
            if (isLoading) {
                CircularProgressIndicator()
            } else {
                Button(
                    onClick = {
                        isLoading = true
                        coroutineScope.launch {
                            try {
                                FirebaseAuth.getInstance().signInAnonymously().await()
                                onLoginSuccess()
                            } catch (e: Exception) {
                                Toast.makeText(context, "Login Failed: ${e.message}. Please enable Anonymous Authentication in Firebase Console.", Toast.LENGTH_LONG).show()
                            } finally {
                                isLoading = false
                            }
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp)
                ) {
                    Text("Continue", fontSize = 16.sp)
                }
            }
        }
    }
}
