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

    // Group plans created by this user, and everyone's membership of them.
    const { data: myPlans } = await admin.from('group_plans').select('id').eq('creator', uid);
    const planIds = (myPlans || []).map((p: { id: number }) => p.id);
    if (planIds.length) await admin.from('group_plan_members').delete().in('plan_id', planIds);
    await admin.from('group_plan_members').delete().eq('user_id', uid);
    if (planIds.length) await admin.from('group_plans').delete().eq('creator', uid);

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
