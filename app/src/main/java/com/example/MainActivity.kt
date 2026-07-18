package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.data.AppDatabase
import com.example.data.AppRepository
import com.example.navigation.AppNavigation
import com.example.ui.theme.MyApplicationTheme
import com.example.viewmodel.AppViewModel
import com.example.viewmodel.AppViewModelFactory

class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    enableEdgeToEdge()
    
    val database = AppDatabase.getDatabase(this)
    val repository = AppRepository(database.appDao())
    val firebaseRepository: com.example.data.FirebaseRepository? = try {
        com.example.data.FirebaseRepository()
    } catch (e: Exception) {
        android.util.Log.e("MainActivity", "Firebase init failed", e)
        android.widget.Toast.makeText(this, "Firebase Init Failed: ${e.message}", android.widget.Toast.LENGTH_LONG).show()
        null
    }
    
    val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
    if (auth?.currentUser == null) {
        auth?.signInAnonymously()?.addOnCompleteListener { task ->
            if (!task.isSuccessful) {
                android.util.Log.e("MainActivity", "Anonymous auth failed", task.exception)
            }
        }
    }
    
    setContent {
      MyApplicationTheme {
        Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
          androidx.compose.foundation.layout.Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            val viewModel: AppViewModel = viewModel(
                factory = AppViewModelFactory(repository, firebaseRepository ?: com.example.data.FirebaseRepository())
            )
            AppNavigation(viewModel)
          }
        }
      }
    }
  }
}