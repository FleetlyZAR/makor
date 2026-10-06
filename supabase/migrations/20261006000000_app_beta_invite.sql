-- App beta invite: every subscriber is invited to the iOS (TestFlight) and
-- Android (Play closed testing) builds. Stored as an instant sequence email so
-- comms.deliver handles rendering, unsubscribes and one-send-per-person.
-- Source of the copy: supabase/emails/app-beta.html and app-beta.txt.

insert into comms.sequence_emails (step, key, cadence, subject, preview_text, html, txt, active)
values (-1, 'app-beta', 'instant',
  'Try the Makor app before anyone else',
  'Makor is in testing on iPhone and Android. Here is how to get it.',
  $mk$<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="IE=edge"><title>Try the Makor app</title></head><body style="margin:0;padding:0;background-color:#F1EADB;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F1EADB" style="background-color:#F1EADB;"><tr><td align="center" style="padding:32px 16px;"><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background-color:#FFFDF8;border:1px solid #E6DECD;">
<tr><td align="center" bgcolor="#0E2A2E" style="background-color:#0E2A2E;padding:34px 24px 30px 24px;"><div style="font-family:Georgia,serif;font-size:30px;font-weight:bold;letter-spacing:8px;color:#0F6C6C;">M A K O R</div><div style="font-family:Georgia,serif;font-size:15px;font-style:italic;color:#9BB0AD;padding-top:10px;">In your light we see light.</div></td></tr>
<tr><td style="padding:38px 44px 30px 44px;">
<p style="margin:0 0 22px 0;font-family:Georgia,serif;font-size:17px;line-height:1.65;color:#0E2A2E;">Hi {{first_name}},</p>
<p style="margin:0 0 20px 0;font-family:Georgia,serif;font-size:17px;line-height:1.65;color:#0E2A2E;">Makor is coming to your phone, and we would love you to be one of the first to use it.</p>
<p style="margin:0 0 20px 0;font-family:Georgia,serif;font-size:17px;line-height:1.65;color:#0E2A2E;">The app is in testing on iPhone and Android. Everything you know from the website is there: every study, the audio, your progress and your plans. It is still being polished, so if something looks wrong or gets in your way, reply to this email and tell us. That is the most helpful thing a tester can do.</p>

<p style="margin:30px 0 10px 0;font-family:Georgia,serif;font-size:13px;font-weight:bold;letter-spacing:2px;color:#B8862F;">ON IPHONE OR IPAD</p>
<p style="margin:0 0 14px 0;font-family:Georgia,serif;font-size:17px;line-height:1.65;color:#0E2A2E;">Apple shares test apps through its free TestFlight app.</p>
<ol style="margin:0 0 20px 0;padding-left:22px;font-family:Georgia,serif;font-size:17px;line-height:1.65;color:#0E2A2E;">
<li style="margin-bottom:8px;">Install <a href="https://apps.apple.com/app/testflight/id899247664" style="color:#0F6C6C;">TestFlight from the App Store</a>.</li>
<li style="margin-bottom:8px;">On the same iPhone or iPad, open the Makor invite link below.</li>
<li style="margin-bottom:8px;">Tap <strong>Accept</strong>, then <strong>Install</strong>. Makor appears on your home screen like any other app.</li>
</ol>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 12px 0;"><tr><td bgcolor="#0F6C6C" style="background-color:#0F6C6C;border-radius:3px;"><a href="https://testflight.apple.com/join/tA1weKaq" style="display:inline-block;padding:13px 26px;font-family:Georgia,serif;font-size:16px;color:#FFFDF8;text-decoration:none;">Get Makor for iPhone</a></td></tr></table>
<p style="margin:0 0 20px 0;font-family:Georgia,serif;font-size:14px;line-height:1.6;color:#6A6357;">Updates arrive through TestFlight. Open it now and then, or turn on automatic updates there.</p>

<p style="margin:30px 0 10px 0;font-family:Georgia,serif;font-size:13px;font-weight:bold;letter-spacing:2px;color:#B8862F;">ON ANDROID</p>
<ol style="margin:0 0 20px 0;padding-left:22px;font-family:Georgia,serif;font-size:17px;line-height:1.65;color:#0E2A2E;">
<li style="margin-bottom:8px;">On your Android phone, open the link below while signed in to Google Play with the email address you used for Makor.</li>
<li style="margin-bottom:8px;">Tap <strong>Become a tester</strong>.</li>
<li style="margin-bottom:8px;">Tap <strong>Download it on Google Play</strong> and install Makor as usual.</li>
</ol>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 12px 0;"><tr><td bgcolor="#0F6C6C" style="background-color:#0F6C6C;border-radius:3px;"><a href="https://play.google.com/apps/testing/za.co.makor.app" style="display:inline-block;padding:13px 26px;font-family:Georgia,serif;font-size:16px;color:#FFFDF8;text-decoration:none;">Get Makor for Android</a></td></tr></table>
<p style="margin:0 0 20px 0;font-family:Georgia,serif;font-size:14px;line-height:1.6;color:#6A6357;">If Play says the app is not available, your Play Store is probably signed in with a different Google account. Reply with the Gmail address you use on your phone and we will add it.</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:10px;"><tr><td style="border-left:3px solid #B8862F;padding:4px 0 4px 18px;"><p style="margin:0;font-family:Georgia,serif;font-size:17px;font-style:italic;line-height:1.6;color:#0E2A2E;">Your word is a lamp to my feet and a light to my path.</p><p style="margin:6px 0 0 0;font-family:Georgia,serif;font-size:14px;color:#6A6357;">Psalm 119:105</p></td></tr></table>
<p style="margin:28px 0 0 0;font-family:Georgia,serif;font-size:17px;line-height:1.65;color:#6A6357;">Grace and peace,<br><span style="color:#0F6C6C;">The Makor team</span></p>
</td></tr>
<tr><td bgcolor="#F1EADB" style="background-color:#F1EADB;padding:22px 44px;border-top:1px solid #E6DECD;"><p style="margin:0 0 6px 0;font-family:Georgia,serif;font-size:12px;line-height:1.6;color:#6A6357;">Makor &middot; Johannesburg, South Africa &middot; <a href="https://www.makor.co.za" style="color:#0F6C6C;text-decoration:none;">www.makor.co.za</a></p><p style="margin:0;font-family:Georgia,serif;font-size:12px;line-height:1.6;color:#6A6357;">You are receiving this because you signed up at makor.co.za. <a href="{{unsub_url}}" style="color:#6A6357;">Unsubscribe</a> or <a href="https://makor.co.za/email-preferences/" style="color:#6A6357;">manage your email preferences</a>.</p></td></tr>
</table></td></tr></table></body></html>
$mk$,
  $mk$Hi {{first_name}},

Makor is coming to your phone, and we would love you to be one of the first to use it.

The app is in testing on iPhone and Android. Everything you know from the website is there: every study, the audio, your progress and your plans. It is still being polished, so if something looks wrong or gets in your way, reply to this email and tell us. That is the most helpful thing a tester can do.

ON IPHONE OR IPAD
Apple shares test apps through its free TestFlight app.
1. Install TestFlight from the App Store: https://apps.apple.com/app/testflight/id899247664
2. On the same iPhone or iPad, open the Makor invite link: https://testflight.apple.com/join/tA1weKaq
3. Tap Accept, then Install. Makor appears on your home screen like any other app.
Updates arrive through TestFlight. Open it now and then, or turn on automatic updates there.

ON ANDROID
1. On your Android phone, open this link while signed in to Google Play with the email address you used for Makor: https://play.google.com/apps/testing/za.co.makor.app
2. Tap Become a tester.
3. Tap Download it on Google Play and install Makor as usual.
If Play says the app is not available, your Play Store is probably signed in with a different Google account. Reply with the Gmail address you use on your phone and we will add it.

"Your word is a lamp to my feet and a light to my path." Psalm 119:105

Grace and peace,
The Makor team

Makor, Johannesburg, South Africa, www.makor.co.za
Unsubscribe: {{unsub_url}}
Manage your email preferences: https://makor.co.za/email-preferences/
$mk$,
  true)
on conflict (key) do update
  set subject = excluded.subject, preview_text = excluded.preview_text,
      html = excluded.html, txt = excluded.txt, active = excluded.active;

-- New sign ups: welcome, then the app invite, then tell the admins to add the
-- address to the Play closed testing list (Play has no API for email lists).
create or replace function comms.enroll_and_welcome(p_user_id uuid, p_email text, p_first text, p_last text)
returns void
language plpgsql security definer set search_path to 'comms', 'public'
as $$
declare v_new boolean; v_admin text;
begin
  v_new := not exists (select 1 from comms.subscribers where user_id = p_user_id);
  insert into comms.subscribers (user_id, email, first_name, last_name, enrolled_at)
  values (p_user_id, p_email, p_first, p_last, now())
  on conflict (user_id) do update
    set email = excluded.email, first_name = excluded.first_name, last_name = excluded.last_name;
  perform comms.deliver(p_user_id, 'welcome');
  perform comms.deliver(p_user_id, 'app-beta');
  if v_new and p_email is not null then
    for v_admin in select email from public.admins loop
      perform comms.send_email(
        v_admin,
        'New Makor tester: add ' || p_email || ' to Play closed testing',
        '<p style="font-family:Georgia,serif;font-size:16px;">' || coalesce(nullif(btrim(p_first), ''), 'Someone') ||
          ' just signed up and was sent the app invite.</p><p style="font-family:Georgia,serif;font-size:16px;">Add <strong>' ||
          p_email || '</strong> to the closed testing email list in Play Console (Testing, Closed testing, Testers) so the Android link works for them.</p>',
        coalesce(nullif(btrim(p_first), ''), 'Someone') || ' just signed up and was sent the app invite. Add ' || p_email ||
          ' to the closed testing email list in Play Console (Testing, Closed testing, Testers) so the Android link works for them.');
    end loop;
  end if;
exception when others then
  raise notice 'Makor enroll_and_welcome error: %', sqlerrm;
end;
$$;
