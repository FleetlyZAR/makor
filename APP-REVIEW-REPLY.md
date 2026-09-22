# Reply to App Review, submission 308349f1-8275-48ba-b104-349bb360ca28

Paste the body below into "Reply to App Review" in App Store Connect, then attach
build 1.0 (10) to the version and resubmit.

---

Both issues are resolved in build 1.0 (10).

## Guideline 4, Design, Sign in with Apple

Every Sign in with Apple control in the app is now a standard Sign in with Apple button, built to the Human Interface Guidelines:

1. It carries the Apple logo and the title "Sign in with Apple".
2. It is a solid black button on light backgrounds and the white style on dark backgrounds.
3. It is 48 points tall, the same size as the Google button beside it, and it is listed first.

It appears in this form on every screen that offers sign in: the welcome screens, the Home tab, the top menu, the sign in bar, the You (profile) screen, notification settings, and delete account. In the top menu, sign in was previously shown as plain menu text. It is now the same button as everywhere else.

## Guideline 2.1(a), Performance, App Completeness

The crash on iPad Air 11-inch (M3) when choosing Camera from Change Photo is fixed. The app did not declare a camera usage description, so iPadOS terminated it the moment the camera was requested. Build 9 declares the camera and photo library purposes, and Makor uses them only when the reader chooses to take or pick a profile photo.

We tested the full Change Photo flow in build 10 on iPad and iPhone, choosing Take Photo, Photo Library and Choose File, with the permission prompt both allowed and denied. The app no longer crashes on any of these paths.
