import ctypes
import win32api

# Get a handle to the primary monitor
monitor = win32api.EnumDisplayMonitors()[0][0]

# Get a pointer to a DEVICE_SCALE_FACTOR value
scale_factor = ctypes.c_int()

# Call the GetScaleFactorForMonitor function with the monitor handle and scale factor pointer
ctypes.windll.shcore.GetScaleFactorForMonitor(ctypes.c_int(monitor), ctypes.byref(scale_factor))

# Print the scale factor value
print(scale_factor.value)