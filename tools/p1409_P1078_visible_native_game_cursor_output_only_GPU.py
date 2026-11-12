#!/usr/bin/env python3
"""P1078 visible physical Switch mouse position drawn AFTER persistent HD
canvas and CHILD overlays, BEFORE SDL_RenderPresent. Does NOT paint into
game canvas/CG/video or synthesize cursor/button events.
Source is exact actual user-tested GPL2 P1016 GPU. Keep prior host fixture,
original GPU exports and AArch64 ABI untouched. Standalone host visual
primitive tests optional; no unverified gameplay assumptions.
"""
import json,subprocess
from pathlib import Path
from port_workspace import write_json
from verify_p1123_round204_CLEAN_game_only_native_MPEG_MP2_without_ffmpeg_64Switch_STRICTPIE26 import S,T,SDK,Z,UP,sha,require,check_aarch64
from verify_p838_round128_link_frontier_original_gpl2_vm_core_ARM64 import symbols_in
from p1333_add_bounded_real_Switch_present_vsync_probe_source_only import SRC as OLD,OBJ as OLDOBJ,REPORT as OLDREPORT,HOSTEXE,HOST,WIN,CHILD,INPUT,VP,D,P454,P445,P438,P441
Q=S/'P1409_第278轮_真机P1074存读档看不见光标_只加最终输出高对比准星'
SRC=Q/'p1409_P1078_original_SDL_HD_output_only_visible_mouse_cursor.c'
OBJ=Q/'p1409_P1078_real_original_GPU_AARCH64.o'
HOSTRESULT=Q/'p1409_original_8child_GPU_output_host.exe'
REPORT=T/'P1078A_第278轮仅原GPL2高清输出渲染真正鼠标高对比可见_原8子窗GPU_AARCH64.json'
CURSOR=r'''/* P1490: half-size arrow + rate-limited follow (uniform motion even at low fps). */
#ifndef P902_HOST_TEST
#define P1490_ARROW_W 12
#define P1490_ARROW_H 19
static const char*const P1490_arrow[P1490_ARROW_H]={
"#...........",
"##..........",
"#w#.........",
"#ww#........",
"#www#.......",
"#wwww#......",
"#wwwww#.....",
"#wwwwww#....",
"#wwwwwww#...",
"#wwwwwwww#..",
"#wwwwwwwww#.",
"#wwwwwwwwww#",
"#wwwww#####.",
"#wwww#......",
"#www#.......",
"#ww#........",
"#w#.........",
"##..........",
"#..........."
};
static void P1490_DrawArrowCursor(SDL_Renderer*r,int x,int y,int s)
{
 int row,col;
 if(!r||s<1)return;
 for(row=0;row<P1490_ARROW_H;row++){
  const char*line=P1490_arrow[row];
  col=0;
  while(col<P1490_ARROW_W){
   char c=line[col];
   int start=col;
   SDL_Rect rc;
   if(c=='.'){while(col<P1490_ARROW_W&&line[col]=='.')col++;continue;}
   while(col<P1490_ARROW_W&&line[col]==c)col++;
   if(c=='#'){if(SDL_SetRenderDrawColor(r,0,0,0,255)<0)return;}
   else{if(SDL_SetRenderDrawColor(r,255,255,255,255)<0)return;}
   rc.x=x+start*s;rc.y=y+row*s;rc.w=(col-start)*s;rc.h=s;
   if(SDL_RenderFillRect(r,&rc)<0)return;
  }
 }
}
/* move the drawn cursor toward the logical one at a bounded, steady speed.
 * Proportional easing bursts when the target jitters; a rate limit does not. */
static void P1490_StepToward(float*tx,float*ty,float x,float y,float maxstep)
{
 float dx=x-*tx,dy=y-*ty;
 float ax=dx<0.f?-dx:dx, ay=dy<0.f?-dy:dy;
 float d=ax>ay?ax:ay;
 if(d<0.75f){*tx=x;*ty=y;return;}
 if(d>maxstep){*tx+=(dx/d)*maxstep;*ty+=(dy/d)*maxstep;}
 else{*tx=x;*ty=y;}
}
/* P1078: draw the physical Switch pointer on the output backbuffer only. */
static void P1078_RenderLivePhysicalCursor(SDL_Renderer*r,const P441Viewport*vp)
{
 SDL_Window*win;Uint8 cr,cg,cb,ca;
 int x=0,y=0,wx=0,wy=0,s=1;
 static float s_px=-1000000.f,s_py=-1000000.f;
 if(!r||!vp)return;
 win=SDL_GetMouseFocus();
 if(!win)win=SDL_GetKeyboardFocus();
 if(!win)return;
 SDL_GetWindowPosition(win,&wx,&wy);
 OS_CursorGetPos(&x,&y);
 x-=wx;y-=wy;
 if(x<vp->destination.x || y<vp->destination.y ||
    x>=vp->destination.x+vp->destination.w ||
    y>=vp->destination.y+vp->destination.h)return;
 {
  float tx=(float)x,ty=(float)y;
  float dxn=tx-s_px,dyn=ty-s_py;
  if(dxn<0.f)dxn=-dxn;
  if(dyn<0.f)dyn=-dyn;
  if(s_px<-999999.f || dxn>48.f || dyn>48.f){s_px=tx;s_py=ty;}
  else P1490_StepToward(&s_px,&s_py,tx,ty,9.f);
  x=(int)(s_px+0.5f);y=(int)(s_py+0.5f);
 }
 if(x<vp->destination.x || y<vp->destination.y ||
    x>=vp->destination.x+vp->destination.w ||
    y>=vp->destination.y+vp->destination.h)return;
 s=(vp->destination.h>=1080)?2:1;
 if(SDL_GetRenderDrawColor(r,&cr,&cg,&cb,&ca)<0)return;
 P1490_DrawArrowCursor(r,x,y,s);
 (void)SDL_SetRenderDrawColor(r,cr,cg,cb,ca);
}
#endif
'''
def run(cmd,label):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,timeout=120)
 out=(p.stdout+p.stderr).decode('utf8','replace')
 require(p.returncode==0,label+' '+out[-2200:])
 return out
def main():
 Q.mkdir(parents=True,exist_ok=True)
 audit=json.loads(OLDREPORT.read_text('utf-8-sig'))
 require(audit['status']=='PASS_P1016_REAL_P982_GUI_8CHILD_UNCHANGED_BOUNDED_NATIVE_PRESENT_TIMER_ARM64'
  and audit['timed_P982_GPU_source_SHA256']==sha(OLD)
  and audit['timed_native_AARCH64_SHA256']==sha(OLDOBJ),
  'user actual Switch renderer old source exact SHA with 8child GUI')
 s=OLD.read_text('utf8')
 at='int P454_RenderPersistentCanvas(SDL_Renderer*r)'
 require(s.count(at)==1 and s.count(' P956_RenderSettingsFocus(r,&vp);')==1
         and s.count('P1088_DrawChildOverlays(r,&vp.destination)')==1,
         'real P982 output after full HD composite and child layers')
 s=s.replace(at,CURSOR+'\n'+at,1)
 s=s.replace(' P956_RenderSettingsFocus(r,&vp);',
             ' P956_RenderSettingsFocus(r,&vp);\n#ifndef P902_HOST_TEST\n P1078_RenderLivePhysicalCursor(r,&vp);\n#endif',1)
 require(s.replace('\n#ifndef P902_HOST_TEST\n P1078_RenderLivePhysicalCursor(r,&vp);\n#endif','',1).replace(CURSOR+'\n','',1)==OLD.read_text('utf8'),
  'only overlay on window backbuffer, original GPU canvas exactly unchanged')
 SRC.write_text(s,'utf8')
 dirs=[D,P454,P445,P438,P441,UP/'inc',SDK/'portlibs/switch/include',SDK/'portlibs/switch/include/SDL2']
 # Full original 8-child GUI host replay is identical when HOS-specific
 # cursor render is disabled by P902_HOST_TEST, as in the original suite.
 host=['C:/msys64/mingw64/bin/gcc.exe','-std=c99','-O2','-Wall','-Wextra','-Werror','-pedantic','-DSDL_MAIN_HANDLED','-DP902_HOST_TEST']
 for v in dirs:host+=['-I',v]
 run([*host,WIN,SRC,CHILD,HOST,INPUT,VP,'-o',HOSTRESULT],
     'real GPL2 HD canvas + all 8 child-window regression')
 hostout=run([HOSTRESULT],'old P982 original 8child/full canvas no overlay in host')
 require('P1090 PASS real original BGI child target GPU' in hostout,
   'never regress original CG compositing')
 cmd=[Z,'cc','-target','aarch64-freestanding-none','-std=c99','-O2','-fPIC',
      '-ffunction-sections','-fdata-sections','-isystem',SDK/'devkitA64/aarch64-none-elf/include']
 for v in dirs:cmd+=['-I',v]
 run([*cmd,'-c',SRC,'-o',OBJ],'real libnx GPU AArch64 output overlay')
 check_aarch64(OBJ)
 require(symbols_in(OLDOBJ)[0]==symbols_in(OBJ)[0] and
         'P454_RenderPersistentCanvas' in symbols_in(OBJ)[0],
         'all original gfx/GNU ABI exports unchanged')
 require('P1078_RenderLivePhysicalCursor' in SRC.read_text('utf8') and
    b'SDL_RenderFillRect' in OBJ.read_bytes(),
    'real SDL cursor graphics compiled into ARM64 GPU owner')
 write_json(REPORT,{'status':'PASS_P1078_SDL_OUTPUT_ONLY_HIGH_CONTRAST_REAL_HOS_CURSOR_ORIGINAL_GPU_ARM64_8CHILD',
   'P1016_exact_old_GPU_sha256':sha(OLD),'P1016_exact_old_GPU_object_sha256':sha(OLDOBJ),
   'P1078_only_overlay_GPU_sha256':sha(SRC),'P1078_GPU_native_AARCH64_sha256':sha(OBJ),
   'existing_P1090_all_8child_host_pass':True,
   'original_VM_SpritePanel_legacy_GBK_SaveLoad_original_art_audio_unchanged':True,
   'new_switch_gameplay_not_verified':True,'host_output':hostout.strip()})
 print('P1078_HIGH_CONTRAST_PHYSICAL_SWITCH_CURSOR_OUTPUT_ONLY_FULL_8CHILD_AND_ARM64_PASS',sha(OBJ))
if __name__=='__main__':main()
