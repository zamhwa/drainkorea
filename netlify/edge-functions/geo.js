// Netlify Edge Function: 서버단 정확 위치(geo) JSON 제공
export default (request, context) => {
  const g = (context && context.geo) || {};
  const body = JSON.stringify({
    city: g.city || '',
    region: (g.subdivision && g.subdivision.name) || '',
    country: (g.country && g.country.code) || ''
  });
  return new Response(body, {
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }
  });
};
export const config = { path: '/__geo' };
