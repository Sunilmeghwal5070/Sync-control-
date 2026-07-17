package com.example.ui.screens

import androidx.compose.animation.Crossfade
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun OnboardingScreen(onFinishOnboarding: () -> Unit) {
    var currentPage by remember { mutableIntStateOf(1) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(32.dp))
        
        Crossfade(targetState = currentPage) { page ->
            Text(
                text = if (page == 1) "Monitor your child's device effortlessly" else "Choose specific apps or monitor everything.",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary,
                textAlign = TextAlign.Center
            )
        }

        Spacer(modifier = Modifier.weight(1f))
        
        Box(
            modifier = Modifier
                .size(200.dp)
                .background(MaterialTheme.colorScheme.surfaceVariant, CircleShape),
            contentAlignment = Alignment.Center
        ) {
             Crossfade(targetState = currentPage) { page ->
                 Text(if (page == 1) "Safety First" else "Full Control", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
             }
        }

        Spacer(modifier = Modifier.weight(1f))

        Crossfade(targetState = currentPage) { page ->
            Text(
                text = if (page == 1) 
                    "Track notifications, app usage, and secure your child from harmful activities remotely."
                else 
                    "You have the power to lock apps, block websites, and track location in real-time.",
                fontSize = 16.sp,
                color = MaterialTheme.colorScheme.onBackground,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 16.dp)
            )
        }

        Spacer(modifier = Modifier.height(48.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(onClick = onFinishOnboarding) {
                Text("Skip", color = MaterialTheme.colorScheme.primary, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            
            Text("$currentPage/2", color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.6f), fontSize = 16.sp)
            
            IconButton(
                onClick = {
                    if (currentPage == 1) currentPage = 2 else onFinishOnboarding()
                },
                modifier = Modifier
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primary)
            ) {
                Icon(Icons.Default.ChevronRight, contentDescription = "Next", tint = Color.White)
            }
        }
    }
}
