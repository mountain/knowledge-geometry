// https://tex.stackexchange.com/questions/570157/tikz-plot-for-ennepers-minimal-surface
// Enneper's Minimal Surface
// ref:https://mathworld.wolfram.com/EnnepersMinimalSurface.html
//
// ennepers.asy
//
// to get ennepers.png, run
// asy -f png -render=4 ennepers.asy

import graph3;
size(200,0);
currentlight.background=white+opacity(0.0);

currentprojection=
  orthographic(camera=(-200,600,600));

triple f(pair t){
  real r=t.x, phi=t.y;
  real x=r*cos(phi)-1/3*r^3*cos(3*phi);
  real y=-1/3*r*(3*sin(phi)+r^2*sin(3*phi));
  real z=r^2*cos(2*phi);
  return (x,y,z);
}

surface s=surface(f,(0,-pi),(1,pi),nu=12,nv=200,usplinetype=Spline);
draw(s,paleblue+opacity(0.4),meshpen=nullpen,render(merge=true));
