import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// Deletes the calling user's account and all of their data. The caller must
// send their session JWT in the Authorization header. The platform verifies
// the JWT, and we derive the user id from it, so a user can only ever delete
// their own account. Deployed to the makor Supabase project as the
// delete-account Edge Function (verify_jwt on).

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

function json(body: unknown, status: number) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json' } });
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });

  try {
    const url = Deno.env.get('SUPABASE_URL')!;
    const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const token = (req.headers.get('Authorization') || '').replace('Bearer ', '').trim();
    if (!token) return json({ error: 'Not authenticated' }, 401);

    const admin = createClient(url, serviceKey, { auth: { persistSession: false, autoRefreshToken: false } });
    const { data: userData, error: userErr } = await admin.auth.getUser(token);
    if (userErr || !userData || !userData.user) return json({ error: 'Invalid session' }, 401);
    const uid = userData.user.id;

    // Groups this user leads (with their invites/members), and any group the
    // user was invited to or joined.
    const { data: myGroups } = await admin.from('groups').select('id').eq('leader', uid);
    const groupIds = (myGroups || []).map((g: { id: number }) => g.id);
    if (groupIds.length) await admin.from('group_members').delete().in('group_id', groupIds);
    await admin.from('group_members').delete().eq('user_id', uid);
    if (groupIds.length) await admin.from('groups').delete().eq('leader', uid);

    // User owned rows across the app.
    const tables = ['attempts', 'daily_activity', 'devices', 'notifications', 'study_progress', 'user_prefs', 'user_badges'];
    for (const t of tables) await admin.from(t).delete().eq('user_id', uid);
    await admin.from('friendships').delete().or('requester.eq.' + uid + ',addressee.eq.' + uid);
    await admin.from('events').delete().eq('user_id', uid);
    await admin.from('profiles').delete().eq('id', uid);

    // Finally, remove the auth user itself.
    const { error: delErr } = await admin.auth.admin.deleteUser(uid);
    if (delErr) return json({ error: 'Could not delete account: ' + delErr.message }, 500);

    return json({ success: true }, 200);
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
