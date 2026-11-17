# Reply to App Review, submission 308349f1-8275-48ba-b104-349bb360ca28

Paste the body below into "Reply to App Review" in App Store Connect, then attach
build 1.0 (15) to the version and resubmit.

---

The issue from your review of 16 October 2026 is resolved in build 1.0 (15).

## Guideline 2.1(a), Performance, App Completeness

Tapping Sign in with Apple or Sign in with Google on iPad opened a window with no content. The app was presenting the sign in page in a popover, which on iPad appeared as a small empty floating window. On iPhone the same code presented a full screen page, which is why we did not catch it.

Build 15 presents the sign in page full screen on every device. Tapping Sign in with Apple now opens the Apple Account sign in page, and tapping Sign in with Google opens the Google sign in page, each filling the screen with the address shown at the top and a close button.

We tested both buttons in build 15 on iPad Air 11-inch running iPadOS 27, the same device class and OS version as your review, from a fresh install, and on iPhone.
