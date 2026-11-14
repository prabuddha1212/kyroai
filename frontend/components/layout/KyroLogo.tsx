"use client";

import React, { useEffect, useState } from "react";

export function KyroLogo({
  size = 46,
  showParticles = true,
  withReveal = true,
  className = "",
}: {
  size?: number;
  showParticles?: boolean;
  withReveal?: boolean;
  className?: string;
}) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div
      className={`relative inline-flex items-center justify-center shrink-0 rounded-2xl group transition-transform duration-300 hover:scale-105 ${className}`}
      style={{ width: size, height: size }}
      title="KyroAI 3D Logo"
    >
      {/* 2D Vector Base matching color scheme */}
      <KyroLogoSvg size={size} />

      {/* Interactive 3D WebGL Logo with complete spin-in reveal, floating idle, particles & lighting */}
      {mounted && (
        <iframe
          srcDoc={`<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0;overflow:hidden}
html,body{width:100%;height:100%;background:transparent}
#c{width:100%;height:100%;display:block;cursor:pointer}
</style>
</head>
<body>
<canvas id="c"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\/script>
<script>
(function(){
  var canvas=document.getElementById('c');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var renderer=new THREE.WebGLRenderer({canvas:canvas,antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
  var scene=new THREE.Scene();
  var camera=new THREE.PerspectiveCamera(35,1,0.1,50);
  camera.position.set(0,0,7.3);

  scene.add(new THREE.AmbientLight(0x88ffd0,0.65));
  var key=new THREE.PointLight(0x39ffb0,2.6,30);key.position.set(3,3,5);scene.add(key);
  var rim=new THREE.PointLight(0x00c8ff,1.9,30);rim.position.set(-4,-2,3);scene.add(rim);
  var top=new THREE.DirectionalLight(0xffffff,0.95);top.position.set(0,4,4);scene.add(top);

  function rr(w,h,r){var s=new THREE.Shape(),x=-w/2,y=-h/2;
    s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);s.lineTo(x+w,y+h-r);
    s.quadraticCurveTo(x+w,y+h,x+w-r,y+h);s.lineTo(x+r,y+h);s.quadraticCurveTo(x,y+h,x,y+h-r);
    s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);return s;}
  function poly(p){var s=new THREE.Shape();s.moveTo(p[0][0],p[0][1]);for(var i=1;i<p.length;i++)s.lineTo(p[i][0],p[i][1]);s.closePath();return s;}
  function ext(shape,depth,bevel){return new THREE.ExtrudeGeometry(shape,{depth:depth,bevelEnabled:true,bevelThickness:bevel,bevelSize:bevel,bevelSegments:4,curveSegments:18});}

  var logo=new THREE.Group();scene.add(logo);
  var baseMat=new THREE.MeshPhysicalMaterial({color:0x1fa56f,metalness:0.25,roughness:0.28,clearcoat:1,clearcoatRoughness:0.15,emissive:0x0a5a3a,emissiveIntensity:0.5});
  var base=new THREE.Mesh(ext(rr(2.3,2.3,0.55),0.35,0.08),baseMat);base.position.z=-0.2;logo.add(base);

  var darkMat=new THREE.MeshPhysicalMaterial({color:0x0b2a21,metalness:0.5,roughness:0.35,clearcoat:0.6});
  var kg=new THREE.Group();
  var stem=poly([[-0.62,-0.62],[-0.28,-0.62],[-0.28,0.62],[-0.62,0.62]]);
  var up=poly([[-0.28,0.02],[0.02,0.62],[0.40,0.62],[0.02,-0.06]]);
  var lo=poly([[-0.28,-0.06],[0.02,0.02],[0.40,-0.62],[0.02,-0.62]]);
  [stem,up,lo].forEach(function(s){var m=new THREE.Mesh(ext(s,0.22,0.03),darkMat);kg.add(m);});
  kg.position.set(-0.12,0,0.28);logo.add(kg);

  var chevMat=new THREE.MeshPhysicalMaterial({color:0xdfffee,emissive:0x7dffc8,emissiveIntensity:0.95,roughness:0.18});
  var chev=new THREE.Mesh(ext(poly([[0.62,0.42],[0.30,0.0],[0.62,-0.42],[0.76,-0.30],[0.50,0.0],[0.76,0.30]]),0.14,0.02),chevMat);
  chev.position.set(0.05,0,0.46);logo.add(chev);

  // Shockwave pulsing ring
  var ringGeo=new THREE.RingGeometry(1.4,1.48,64);
  var ringMat=new THREE.MeshBasicMaterial({color:0x39ffb0,transparent:true,opacity:0,side:THREE.DoubleSide});
  var ring=new THREE.Mesh(ringGeo,ringMat);ring.position.z=-0.3;scene.add(ring);

  ${
    showParticles
      ? `
  // Mint ambient particles
  var N=90,pos=new Float32Array(N*3),vel=[];
  for(var i=0;i<N;i++){
    var a=Math.random()*6.283,r=1.3+Math.random()*1.7;
    pos[i*3]=Math.cos(a)*r;pos[i*3+1]=Math.sin(a)*r;pos[i*3+2]=(Math.random()-0.5)*2.2;
    vel.push(Math.random()*0.35+0.1);
  }
  var pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(pos,3));
  var pm=new THREE.PointsMaterial({color:0x39ffb0,size:0.06,transparent:true,opacity:0.75});
  var pts=new THREE.Points(pg,pm);scene.add(pts);
  `
      : ""
  }

  function resize(){var s=canvas.clientWidth||${size};renderer.setSize(s,s,false);camera.aspect=1;camera.updateProjectionMatrix();}
  window.addEventListener('resize',resize);resize();

  var mx=0,my=0;
  window.addEventListener('pointermove',function(e){
    mx=(e.clientX/window.innerWidth-0.5)*2;
    my=(e.clientY/window.innerHeight-0.5)*2;
  });

  function easeOutBack(x){var c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}
  function easeOut(x){return 1-Math.pow(1-x,3);}
  var t0=performance.now();

  function animate(now){
    var t=(now-t0)/1000;
    var withReveal=${withReveal ? "true" : "false"};
    var p=(reduce || !withReveal)?1:Math.min(t/1.5,1);
    var s=Math.max(0.0001,easeOutBack(p));
    logo.scale.setScalar(s);

    var spin=(1-easeOut(p))*Math.PI*3;
    var idle=reduce?0:Math.sin(t*1.1)*0.32;
    logo.rotation.y=-spin+idle+mx*0.35;
    logo.rotation.x=(1-easeOut(p))*0.6+my*0.25+(reduce?0:Math.cos(t*0.8)*0.08);
    logo.position.y=reduce?0:Math.sin(t*1.5)*0.08;

    // K & chevron pop forward
    var kp=easeOut(Math.min(Math.max((t-0.5)/0.7,0),1));
    kg.position.z=-0.2+0.48*kp;
    chev.position.z=-0.1+0.56*kp;

    // shockwave ring burst on reveal
    var rp=Math.min(Math.max((t-0.9)/1.1,0),1);
    ring.scale.setScalar(1+rp*1.5);
    ringMat.opacity=(rp>0 && rp<1)?0.75*(1-rp):0;

    ${
      showParticles
        ? `
    var a=pg.attributes.position.array;
    for(var i=0;i<N;i++){
      a[i*3+1]+=vel[i]*0.006;
      if(a[i*3+1]>2.5)a[i*3+1]=-2.5;
    }
    pg.attributes.position.needsUpdate=true;
    pts.rotation.y=t*0.1;
    `
        : ""
    }

    key.position.x=3*Math.cos(t*0.8);key.position.y=3*Math.sin(t*0.6);
    renderer.render(scene,camera);
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);

  // Click on canvas to replay animation
  canvas.addEventListener('click',function(){
    t0=performance.now();
  });
})();
<\/script>
</body>
</html>`}
          title="KyroAI 3D Logo"
          className="absolute inset-0 w-full h-full border-0 select-none z-10"
        />
      )}
    </div>
  );
}

/**
 * 2D SVG vector logo matching the exact 3D geometry of KyroAI
 */
export function KyroLogoSvg({ size = 46, className = "" }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="-1.3 -1.3 2.6 2.6"
      className={`shrink-0 drop-shadow-[0_0_14px_rgba(34,196,135,0.5)] ${className}`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="kyroBaseGrad" x1="-1" y1="-1" x2="1" y2="1">
          <stop offset="0%" stopColor="#2ee59d" />
          <stop offset="100%" stopColor="#148356" />
        </linearGradient>
        <linearGradient id="kyroChevGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#ffffff" />
          <stop offset="100%" stopColor="#86ffcd" />
        </linearGradient>
        <filter id="kyroGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="0" stdDeviation="0.09" floodColor="#39ffb0" floodOpacity="0.85" />
        </filter>
      </defs>

      {/* Rounded Squircle Base */}
      <rect
        x="-1.15"
        y="-1.15"
        width="2.3"
        height="2.3"
        rx="0.55"
        fill="url(#kyroBaseGrad)"
        stroke="rgba(255,255,255,0.28)"
        strokeWidth="0.04"
      />

      {/* Dark K glyph */}
      <g fill="#0b2a21" transform="translate(-0.12, 0)">
        <polygon points="-0.62,-0.62 -0.28,-0.62 -0.28,0.62 -0.62,0.62" />
        <polygon points="-0.28,0.02 0.02,0.62 0.40,0.62 0.02,-0.06" />
        <polygon points="-0.28,-0.06 0.02,0.02 0.40,-0.62 0.02,-0.62" />
      </g>

      {/* Glowing Chevron / AI mark */}
      <polygon
        points="0.67,0.42 0.35,0.0 0.67,-0.42 0.81,-0.30 0.55,0.0 0.81,0.30"
        fill="url(#kyroChevGrad)"
        filter="url(#kyroGlow)"
      />
    </svg>
  );
}
