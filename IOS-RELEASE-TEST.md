# iOS release test, run before every App Store submission

Run on a real iPhone and a real iPad (or the iPad Air 11-inch simulator) from
the TestFlight build, never only from Xcode. App Review used iPad Air 11-inch
(M3) on iPadOS 26.6 and iPhone 17 Pro Max.

Start each run from a clean install: delete the app, then install from TestFlight.

## 1. First launch and sign in
- [ ] Welcome screens show, Continue and Skip both work.
- [ ] Final welcome screen: white Sign in with Apple button with the Apple logo, above the Google button, same size.
- [ ] Sign in with Apple completes and returns to the app signed in.
- [ ] Sign out from the menu. Sign in with Google completes and returns signed in.
- [ ] Signed out, check every sign in point shows the proper Apple button: Home tab card, top menu, sign in bar, You (profile), Notification settings, Delete account.
- [ ] Turn on dark mode in the app and check the Apple button turns white.

## 2. Change photo (the crash App Review hit)
- [ ] You tab, Change photo, Take Photo: permission prompt shows, Allow, take photo, it saves.
- [ ] Repeat with Don't Allow: no crash, you return to the profile.
- [ ] Photo Library: pick a photo, it saves.
- [ ] Choose File: pick an image, it saves.
- [ ] Repeat all four on iPad in portrait and landscape.

## 3. Links from outside the app (WhatsApp, Messages, Mail, Calendar)
Send yourself these in WhatsApp, then tap each with the app closed (swiped away) and again with the app open in the background:
- [ ] A study link, for example https://makor.co.za/genesis/the-seven-days/
- [ ] A Psalm study link (numeric slug), for example one from a Psalms study page
- [ ] The reading plan, https://makor.co.za/plan/
- [ ] A daily verse page, https://makor.co.za/daily/<slug>/
- [ ] The home page, https://makor.co.za/
For each: the app opens on that exact page, not the landing page. Then tap Home, Plan and another study, and confirm you can move freely and are not pulled back to the linked page.
- [ ] A link to a study published after this build: it opens in the browser instead of stranding you.
- [ ] If WhatsApp opens its own browser instead of the app, long press the link and choose Open in Makor. iOS remembers this choice per app.

## 4. Reading and audio
- [ ] Open a study, open the study drawer, tap a Hebrew or Greek word.
- [ ] Take the quiz before and after, results save when signed in.
- [ ] Play audio, lock the phone, audio keeps playing; next movement moves to the next study, not the landing page.

## 5. Notifications and account
- [ ] Open a notification from the bell: it lands on the right page inside the app.
- [ ] Delete account flow reaches the confirmation step (do not complete it on your real account).

## 6. General
- [ ] Rotate the iPad through all orientations on Home, a study and You.
- [ ] Airplane mode: open a study already in the app, it reads; sign in fails gracefully.
