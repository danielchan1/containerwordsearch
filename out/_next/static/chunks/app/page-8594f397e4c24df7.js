(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[931],{7957:function(e,t,r){Promise.resolve().then(r.bind(r,7083))},7083:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return l}});var n=r(7437),o=r(2265),s=r(6463),i=e=>{let{onSubmit:t}=e;var r=(0,s.useSearchParams)().get("prompt");let o=async e=>{let n=new FormData(e.currentTarget).get("prompt");r||(r=""),n&&n!=r&&t(n)};return(0,n.jsx)("form",{onSubmit:o,children:(0,n.jsxs)("div",{style:{marginBottom:"10px"},children:[(0,n.jsxs)("label",{style:{marginRight:"10px"},children:["Enter a prompt:",(0,n.jsx)("input",{type:"text",name:"prompt",style:{marginLeft:"10px",padding:"5px",borderRadius:"4px",border:"1px solid #ccc",minWidth:"200px"},maxLength:3,minLength:2,required:!0})]}),(0,n.jsx)("button",{type:"submit",style:{padding:"5px 10px",backgroundColor:"#007bff",color:"white",border:"none",borderRadius:"4px",cursor:"pointer"},children:"Search"})]})})},a=r(6648);function l(){let e=(0,s.useRouter)(),[t,r]=(0,o.useState)(null),[l,c]=(0,o.useState)([]),[d,p]=(0,o.useState)(!0),[h,u]=(0,o.useState)(null),[x,m]=(0,o.useState)(!1),f=async e=>{try{let t=await fetch("https://containerwordsearch.pythonanywhere.com/api/search",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({prompt:e})});if(!t.ok)throw Error("Network response failed.");let r=await t.json();c(r)}catch(e){console.error("Error fetching words:",e),u("There was a problem with the fetch operation: ".concat(e))}finally{p(!1)}};return(0,o.useEffect)(()=>{let e=new URLSearchParams(location.search).get("prompt");e&&r(e)},[]),(0,o.useEffect)(()=>{if(t)f(t);else{p(!1);return}},[t]),(0,n.jsx)("main",{className:"flex min-h-screen flex-col items-center justify-between",children:(0,n.jsxs)("div",{style:{fontFamily:"Arial, sans-serif",maxWidth:"600px",margin:"auto",padding:"20px"},children:[(0,n.jsx)("h1",{style:{marginBottom:"20px",fontSize:"30px"},children:"Container Word Search"}),(0,n.jsx)(o.Suspense,{children:(0,n.jsx)(i,{onSubmit:t=>{p(!0),u(null),c([]),e.push("/?prompt=".concat(t))}})}),d&&(0,n.jsx)("div",{children:"Loading..."}),h&&(0,n.jsxs)("div",{children:["Error: ",h]}),!d&&!h&&(0,n.jsxs)("div",{children:[t&&(0,n.jsxs)("h2",{style:{marginTop:"20px"},children:["Words ",t?"containing":""," ",t," (",l.length," found)",l.length>0?":":""]}),(0,n.jsx)("ul",{style:{listStyleType:"none",padding:"0"},children:l.map((e,t)=>(0,n.jsx)("li",{style:{marginBottom:"5px",backgroundColor:"#f0f0f0",padding:"10px",borderRadius:"4px"},children:e.toLowerCase()},t))})]}),(0,n.jsx)("button",{onClick:()=>{window.scroll({top:x?0:document.body.offsetHeight,left:0,behavior:"smooth"}),m(!x)},style:{position:"fixed",bottom:"20px",left:"50%",background:"transparent",border:"none",cursor:"pointer"},children:(0,n.jsx)(a.default,{src:x?"/up.svg":"/down.svg",alt:"",width:24,height:24})})]})})}}},function(e){e.O(0,[595,971,23,744],function(){return e(e.s=7957)}),_N_E=e.O()}]);