#!/bin/bash
cat << 'INNER_EOF' > app/src/main/java/com/example/ui/screens/AppHiderDialogs.kt
package com.example.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import com.example.data.AppInfo
import com.example.data.DeviceConfig

@Composable
fun AppSelectionDialog(
    title: String,
    apps: List<AppInfo>,
    isHiding: Boolean,
    onToggle: (AppInfo, Boolean) -> Unit,
    onDismiss: () -> Unit
) {
    Dialog(onDismissRequest = onDismiss) {
        Card(modifier = Modifier.fillMaxWidth().fillMaxHeight(0.8f)) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(title, style = MaterialTheme.typography.titleLarge)
                Spacer(modifier = Modifier.height(16.dp))
                if (apps.isEmpty()) {
                    Text("No apps found on the child device. Please ensure the child app is running.")
                } else {
                    LazyColumn(modifier = Modifier.weight(1f)) {
                        items(apps) { app ->
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(app.appName, modifier = Modifier.weight(1f))
                                Switch(
                                    checked = if (isHiding) app.isHidden else app.isLocked,
                                    onCheckedChange = { onToggle(app, it) }
                                )
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = onDismiss, modifier = Modifier.fillMaxWidth()) {
                    Text("Close")
                }
            }
        }
    }
}
INNER_EOF
