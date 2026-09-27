[app]
title = June T-Rex
package.name = junetrex
package.domain = com.junedady

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,gif,wav,mp4
source.exclude_dirs = .kivy,bin,.buildozer,__pycache__

version = 1.0.2
android.numeric_version = 102
icon.filename = %(source.dir)s/assets/icon/JtrexIcon.png

requirements = python3,kivy,ffpyplayer
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
