#!/bin/bash
sed -i '/OutlinedTextField(/,/        )/c\
            OutlinedTextField(\
                value = enteredCode,\
                onValueChange = { if (it.length <= 6) enteredCode = it.uppercase() },\
                placeholder = { Text("6-Digit Code", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)) },\
                modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp),\
                singleLine = true,\
                colors = OutlinedTextFieldDefaults.colors(\
                    focusedTextColor = MaterialTheme.colorScheme.onBackground,\
                    unfocusedTextColor = MaterialTheme.colorScheme.onBackground\
                )\
            )\
        }' app/src/main/java/com/example/ui/screens/MainScreens.kt
