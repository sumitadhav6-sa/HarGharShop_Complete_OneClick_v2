const API="/api";
export async function api(path,options={}){
  const r=await fetch(API+path,{credentials:"include",headers:{"Content-Type":"application/json",...(options.headers||{})},...options});
  const d=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(d.error||"Something went wrong");
  return d;
}
