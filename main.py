import os,json,urllib.request as R
U=os.environ["MAKEFUN_ENV_URL"]
def post(p,d):
 return json.loads(R.urlopen(R.Request(U+p,data=json.dumps(d).encode(),headers={"Content-Type":"application/json"})).read())
V=[0,100,320,330,500,900,0]
KN=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
AD=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
DG=[AD[i] for i in(0,2,5,7)]
ST=[AD[i] for i in(1,3,4,6)]
I=10**9
N=[0]
TO=Exception
def parse(f):
 p=f.split();b=[0]*64;r=7;l=0
 for c in p[0]:
  if c=="/":r-=1;l=0
  elif c.isdigit():l+=int(c)
  else:
   v="PNBRQK".index(c.upper())+1
   b[r*8+l]=v if c<"a" else -v;l+=1
 return b,p[1]=="w",sum(1<<"KQkq".index(c) for c in p[2] if c in"KQkq")
def att(b,s,w):
 f,r=s%8,s//8;g=1 if w else -1
 for df in(-1,1):
  ff,rr=f+df,r-g
  if 0<=rr<8 and 0<=ff<8 and b[rr*8+ff]==g:return 1
 for ds,tv in((KN,2),(AD,6)):
  for df,dr in ds:
   ff,rr=f+df,r+dr
   if 0<=ff<8 and 0<=rr<8 and b[rr*8+ff]==tv*g:return 1
 for df,dr in AD:
  ps=(3,5)if df and dr else(4,5)
  ff,rr=f+df,r+dr
  while 0<=ff<8 and 0<=rr<8:
   x=b[rr*8+ff]
   if x:
    if x*g in ps:return 1
    break
   ff+=df;rr+=dr
 return 0
def gen(b,w,cst,caps=0):
 g=1 if w else -1;ms=[]
 for i in range(64):
  p=b[i]
  if p*g<=0:continue
  f,r=i%8,i//8;t=p*g
  if t==1:
   for df in(0,-1,1):
    if df and not 0<=f+df<8:continue
    j=i+8*g+df;x=b[j]
    if df:
     if not x or x*g>0:continue
    elif caps or x:continue
    if j//8 in(0,7):
     for pr in(5,4,3,2):ms.append((i,j,pr))
    else:ms.append((i,j,0))
   if not caps and r==(1 if w else 6) and not b[i+8*g] and not b[i+16*g]:ms.append((i,i+16*g,0))
  else:
   ds,sl=((KN,0),(DG,1),(ST,1),(AD,1),(AD,0))[t-2]
   for df,dr in ds:
    ff,rr=f+df,r+dr
    while 0<=ff<8 and 0<=rr<8:
     x=b[rr*8+ff]
     if x:
      if x*g<0:ms.append((i,rr*8+ff,0))
      break
     if not caps:ms.append((i,rr*8+ff,0))
     if not sl:break
     ff+=df;rr+=dr
  if t==6 and not caps and i==(4 if w else 60):
   if cst&(1 if w else 4) and not b[i+1] and not b[i+2] and b[i+3]==4*g:ms.append((i,i+2,0))
   if cst&(2 if w else 8) and not b[i-1] and not b[i-2] and not b[i-3] and b[i-4]==4*g:ms.append((i,i-2,0))
 return ms
def make(b,w,cst,m):
 f,t,pr=m;nb=b[:];p=nb[f];nb[f]=0
 if pr:p=pr if p>0 else -pr
 nb[t]=p
 if abs(p)==6 and abs(t-f)==2:
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1)
  nb[rt]=nb[rf];nb[rf]=0
 return nb,not w,cst
def legal(s,caps=0):
 b,w,cst=s;o=[]
 for m in gen(b,w,cst,caps):
  if abs(m[1]-m[0])==2 and abs(b[m[0]])==6 and (att(b,m[0],not w) or att(b,(m[0]+m[1])//2,not w)):continue
  ns=make(b,w,cst,m)
  if not att(ns[0],ns[0].index(6 if w else -6),not w):o.append((m,ns))
 return o
def ev(b):
 s=0;mat=0;kc=0
 for i in range(64):
  p=b[i]
  if not p:continue
  g=1 if p>0 else -1;t=p*g;f,r=i%8,i//8
  cen=8-abs(2*f-7)-abs(2*r-7);v=V[t]
  if t==1:v+=(r-1 if g>0 else 6-r)*7
  elif t in(2,3):v+=cen*(6-t)
  elif t==6:kc+=g*cen
  mat+=V[t]
  s+=g*v
 return s+(kc*5 if mat<=2400 else-kc*4)
def srch(s,d,a,be):
 N[0]+=1
 if N[0]>50000:raise TO
 b,w=s[0],s[1]
 chk=att(b,b.index(6 if w else -6),not w)
 if d<=0:
  st=ev(b)if w else-ev(b)
  if not chk:
   if st>=be:return be
   if st>a:a=st
  mv=legal(s,0 if chk else 1)
  if not mv:return -100000 if chk else st
 else:
  mv=legal(s)
  if not mv:return -100000 if chk else 0
 for m,ns in sorted(mv,key=lambda z:-V[abs(b[z[0][1]])]):
  sc=-srch(ns,d-1,-be,-a)
  if sc>=be:return be
  if sc>a:a=sc
 return a
def best(fen):
 s=parse(fen);mv=legal(s)
 if not mv:return None
 bm=mv[0][0];N[0]=0
 for d in range(9):
  try:
   a=-I;cur=bm
   for m,ns in sorted(mv,key=lambda z:-V[abs(s[0][z[0][1]])]):
    sc=-srch(ns,d-1,-I,-a)
    if sc>a:a=sc;cur=m
  except TO:break
  bm=cur
 f,t,pr=bm
 return chr(97+f%8)+str(f//8+1)+chr(97+t%8)+str(t//8+1)+("nbrq"[pr-2] if pr else "")
def main():
 g=post("/game",{})
 while g.get("status")!="done":
  while g.get("status")=="your_move":
   try:m=best(g["fen"])
   except Exception:m=None
   if m not in g["legal_moves"]:m=g["legal_moves"][0]
   g=post("/move",{"game":g["game"],"move":m})
  g=post("/game",{})
if __name__=="__main__":main()
