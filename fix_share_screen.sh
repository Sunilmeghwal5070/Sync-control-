#!/bin/bash
sed -i '/Text("OR", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)/,/onValueChange = { if (it.length <= 6) enteredCode = it.uppercase() },/c\
        if (role == "parent") {\
            Text("OR", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)\
            Spacer(modifier = Modifier.height(16.dp))\
            Text("Enter code of Child'"'"'s Device", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)\
            Spacer(modifier = Modifier.height(16.dp))\
            OutlinedTextField(\
                value = enteredCode,\
                onValueChange = { if (it.length <= 6) enteredCode = it.uppercase() },' app/src/main/java/com/example/ui/screens/MainScreens.kt
sed -i '/unfocusedTextColor = MaterialTheme.colorScheme.onBackground,/!b;n;c\
            )\
        }' app/src/main/java/com/example/ui/screens/MainScreens.kt
