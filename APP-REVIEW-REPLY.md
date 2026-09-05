# Reply to App Review, submission 308349f1-8275-48ba-b104-349bb360ca28

Paste the body below into "Reply to App Review" in App Store Connect, then upload
build 1.0 (8) and resubmit.

---

Both issues are addressed in build 1.0 (8).

## Guideline 4.8, Design, Login Services

Makor offers Sign in with Apple as an equivalent login option alongside Google, and it is now present on every screen that offers Google.

In the reviewed build, Sign in with Apple was present in the welcome flow, on the Home tab and in the top menu, but three screens still offered Google alone: the You (profile) screen shown in your screenshot, the notification settings screen, and the delete account screen. That is fixed in build 8. Sign in with Apple now appears everywhere Google appears, and it is listed first in every case.

Sign in with Apple meets all three requirements:

1. It limits data collection to the user's name and email address. Makor requests the name and email scopes only, and nothing else.
2. It allows the user to keep the email address private. We accept Apple's private relay address exactly as issued, and every feature in the app works on a relay address. The user's real address is never requested and never required.
3. It does not collect interactions with the app for advertising. Makor carries no advertising, no advertising SDK, no third party analytics and no tracking SDK, and the app does not request tracking authorisation. Sign-in data is used only to save the user's reading progress across their own devices.

Signing in is optional throughout. Every study, every book and the reading plan are fully readable without an account. Signing in only saves progress.

## Guideline 2.1(b), Information Needed

Makor has no paid content of any kind. There is nothing to buy inside the app, and nothing bought outside the app that unlocks anything inside it. Taking your four questions in order:

**1. Who are the users that will use the paid content in the app?**

There is no paid content, so there are no such users. Every user has full access to all content for free. Makor is a free Bible study app published by Canaan Empire (Pty) Ltd in South Africa, funded by the company as a ministry rather than by users.

**2. Where can users purchase the content that can be accessed in the app?**

Nowhere. None of the content in the app is for sale, in the app, on our website makor.co.za, or anywhere else. The website carries the same studies as the app and is free and open to everyone.

**3. What specific types of previously purchased content can a user access in the app?**

None. There is no previously purchased content, no entitlement, no licence and no account tier. A signed-in reader and a signed-out reader see exactly the same content. Signing in saves reading progress and quiz results, and nothing more.

**4. What paid content, subscriptions, or features are unlocked within the app that do not use In-App Purchase?**

None. There are no in-app purchases, no subscriptions, no donations, no paid tiers and no unlockable features. The app contains no payment flow, no purchase link, no external purchase link and no payment SDK of any kind. The Scripture text is the Berean Standard Bible, which is in the public domain, so it carries no licence fee.

If the screenshot attached to your message points to a screen that reads as paid content, please tell us which screen it is and we will explain it. We have gone through the app and there is nothing that is sold or that requires payment.
