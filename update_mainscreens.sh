#!/bin/bash
sed -i 's/onPaired()/onPaired()\n                if (role == "child") {\n                    val apps = getInstalledApps(context)\n                    viewModel.updateInstalledApps(apps)\n                }/' app/src/main/java/com/example/ui/screens/MainScreens.kt
