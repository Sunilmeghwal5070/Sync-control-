package com.example.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.ui.screens.*
import com.example.viewmodel.AppViewModel

@Composable
fun AppNavigation(viewModel: AppViewModel) {
    val navController = rememberNavController()
    
    val allPairedDevices by viewModel.allPairedDevices.collectAsStateWithLifecycle()
    val pairedDevice by viewModel.pairedDevice.collectAsStateWithLifecycle()
    
    NavHost(navController = navController, startDestination = "splash") {


        
        composable("splash") {
            SplashScreen(onNavigateToNext = {
                if (allPairedDevices.isNotEmpty()) {
                    navController.navigate("use_case") {
                        popUpTo("splash") { inclusive = true }
                    }
                } else {
                    navController.navigate("onboarding") {
                        popUpTo("splash") { inclusive = true }
                    }
                }
            })
        }
        composable("onboarding") {
            OnboardingScreen(onFinishOnboarding = {
                navController.navigate("loading") {
                    popUpTo("onboarding") { inclusive = true }
                }
            })
        }
        composable("loading") {
            LoadingScreen(onLoadingFinished = {
                navController.navigate("use_case") {
                    popUpTo("loading") { inclusive = true }
                }
            })
        }
        composable("use_case") {
            val hasParentRole = allPairedDevices.any { it.role == "parent" }
            val hasChildRole = allPairedDevices.any { it.role == "child" }
            val currentChildDevice = allPairedDevices.firstOrNull { it.role == "child" }

            UseCaseScreen(
                pairedDevice = currentChildDevice,
                hasParentRole = hasParentRole,
                viewModel = viewModel,
                onNavigateToRoleSelection = {
                    navController.navigate("role_selection")
                },
                onNavigateToParentDashboard = {
                    navController.navigate("parent_dashboard")
                },
                onDisconnect = {
                    viewModel.disconnectDevice()
                }
            )
        }
        composable("parent_dashboard") {
            val selectedPairCode by viewModel.selectedPairCode.collectAsStateWithLifecycle()
            val deviceConfig by viewModel.deviceConfig.collectAsStateWithLifecycle()
            
            ParentDashboardScreen(
                allDevices = allPairedDevices.filter { it.role == "parent" },
                selectedPairCode = selectedPairCode,
                deviceConfig = deviceConfig,
                onSelectDevice = { code -> viewModel.selectDevice(code) },
                onNavigate = { route -> navController.navigate(route) },
                onDisconnect = { code ->
                    viewModel.disconnectDevice(code)
                    if (allPairedDevices.size <= 1) { // If last one deleted
                        navController.navigate("use_case") {
                            popUpTo(0) { inclusive = true }
                        }
                    }
                },
                onAddDevice = {
                    navController.navigate("role_selection")
                }
            )
        }
        composable("device_controls") {
            val config by viewModel.deviceConfig.collectAsStateWithLifecycle()
            DeviceControlsScreen(
                deviceConfig = config,
                onConfigChanged = { viewModel.updateConfig(it) },
                onBack = { navController.popBackStack() }
            )
        }
        composable("location_tracking") {
            val config by viewModel.deviceConfig.collectAsStateWithLifecycle()
            LocationScreen(
                deviceConfig = config,
                onBack = { navController.popBackStack() }
            )
        }
        composable("restrictions") {
            val config by viewModel.deviceConfig.collectAsStateWithLifecycle()
            RestrictionsScreen(
                deviceConfig = config,
                onConfigChanged = { viewModel.updateConfig(it) },
                onBack = { navController.popBackStack() }
            )
        }
        composable("security") {
            val config by viewModel.deviceConfig.collectAsStateWithLifecycle()
            SecurityScreen(
                deviceConfig = config,
                onConfigChanged = { viewModel.updateConfig(it) },
                onBack = { navController.popBackStack() }
            )
        }
        composable("role_selection") {
            RoleSelectionScreen(
                onRoleSelected = { role ->
                    navController.navigate("permissions/$role")
                }
            )
        }
        composable("permissions/{role}") { backStackEntry ->
            val role = backStackEntry.arguments?.getString("role") ?: "child"
            PermissionScreen(role = role, onPermissionsGranted = {
                navController.navigate("share_notification/$role")
            })
        }
        composable("share_notification/{role}") { backStackEntry ->
            val role = backStackEntry.arguments?.getString("role") ?: "child"
            ShareNotificationScreen(
                role = role, 
                viewModel = viewModel,
                onPaired = {
                    navController.navigate("use_case") {
                        popUpTo("role_selection") { inclusive = true }
                    }
                }
            )
        }
        composable("my_notifications") {
            MyNotificationsScreen(
                viewModel = viewModel,
                onBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}

