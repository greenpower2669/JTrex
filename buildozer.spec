[app]
title = June T-Rex
package.name = junetrex
package.domain = com.junedady

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,gif,wav
source.exclude_dirs = .kivy,bin,.buildozer,__pycache__

version = 1.0.1
android.numeric_version = 101
icon.filename = %(source.dir)s/pter/pter0.png

requirements = python3,kivy
orientation = landscape
fullscreen = 1

android.api = 36
android.minapi = 21
android.ndk = 28c
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.debug_artifact = apk
android.release_artifact = aab

p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
