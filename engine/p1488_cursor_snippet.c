/* P1488: desktop-style arrow cursor + sub-pixel smoothing for the Switch pad.
 *
 * Drop-in replacement for the CURSOR string in
 *   01_工具脚本\p1409_P1078_visible_native_game_cursor_output_only_GPU.py
 *
 * Changes vs the old yellow crosshair:
 *  1. Shape: classic 12x19 pointer bitmap, '#' = 1px black outline,
 *     'w' = white body, '.' = transparent. Hot spot = bitmap top-left,
 *     i.e. exactly (x,y) from OS_CursorGetPos, so the tip sits on the click
 *     point with no offset.
 *  2. Motion: the pad moves the logical cursor in whole pixels per frame,
 *     which reads as stepping. Keep a float display position and ease it
 *     toward the logical position, so the drawn cursor moves continuously.
 *     A large jump (> 48 px, e.g. the script warping the cursor into a menu)
 *     snaps immediately instead of gliding.
 *
 * Still drawn after the persistent canvas and the 8 child overlays, before
 * SDL_RenderPresent; never into the 1280x960 game texture.
 */
#ifndef P902_HOST_TEST
#define P1488_ARROW_W 12
#define P1488_ARROW_H 19
static const char*const P1488_arrow[P1488_ARROW_H]={
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
static void P1488_DrawArrowCursor(SDL_Renderer*r,int x,int y,int s)
{
 int row,col;
 if(!r||s<1)return;
 for(row=0;row<P1488_ARROW_H;row++){
  const char*line=P1488_arrow[row];
  col=0;
  while(col<P1488_ARROW_W){
   char c=line[col];
   int start=col;
   SDL_Rect rc;
   if(c=='.'){while(col<P1488_ARROW_W&&line[col]=='.')col++;continue;}
   while(col<P1488_ARROW_W&&line[col]==c)col++;
   if(c=='#'){if(SDL_SetRenderDrawColor(r,0,0,0,255)<0)return;}
   else{if(SDL_SetRenderDrawColor(r,255,255,255,255)<0)return;}
   rc.x=x+start*s;rc.y=y+row*s;rc.w=(col-start)*s;rc.h=s;
   if(SDL_RenderFillRect(r,&rc)<0)return;
  }
 }
}
/* P1078: draw the physical Switch pointer on the output backbuffer only. */
static void P1078_RenderLivePhysicalCursor(SDL_Renderer*r,const P441Viewport*vp)
{
 SDL_Window*win;Uint8 cr,cg,cb,ca;
 int x=0,y=0,wx=0,wy=0,s=2;
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
 /* sub-pixel ease: removes the per-frame integer stepping of the pad */
 {
  float tx=(float)x,ty=(float)y;
  float dxn=tx-s_px,dyn=ty-s_py;
  if(dxn<0.f)dxn=-dxn;
  if(dyn<0.f)dyn=-dyn;
  if(s_px<-999999.f || dxn>48.f || dyn>48.f){s_px=tx;s_py=ty;}
  else{
   s_px+=(tx-s_px)*0.55f;
   s_py+=(ty-s_py)*0.55f;
   if(tx-s_px<0.5f && s_px-tx<0.5f)s_px=tx;
   if(ty-s_py<0.5f && s_py-ty<0.5f)s_py=ty;
  }
  x=(int)(s_px+0.5f);y=(int)(s_py+0.5f);
 }
 if(x<vp->destination.x || y<vp->destination.y ||
    x>=vp->destination.x+vp->destination.w ||
    y>=vp->destination.y+vp->destination.h)return;
 s=(vp->destination.h>=900)?3:2;
 if(SDL_GetRenderDrawColor(r,&cr,&cg,&cb,&ca)<0)return;
 P1488_DrawArrowCursor(r,x,y,s);
 (void)SDL_SetRenderDrawColor(r,cr,cg,cb,ca);
}
#endif
