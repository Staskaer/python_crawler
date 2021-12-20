function utf8Encode(string) {    
var utftext = "";    
for (var n = 0; n<string.length; n++) {    
var c = string.charCodeAt(n);    
if (c<128) {    
utftext += String.fromCharCode(c);    
} else if ((c>127) && (c<2048)) {    
utftext += String.fromCharCode((c >> 6) | 192);    
utftext += String.fromCharCode((c & 63) | 128);    
} else {    
utftext += String.fromCharCode((c >> 12) | 224);    
utftext += String.fromCharCode(((c >> 6) & 63) | 128);    
utftext += String.fromCharCode((c & 63) | 128);    
}    
}    
return utftext;    
}

function utf8Decode(inputStr) {
var outputStr = "";
var code1, code2, code3, code4;
for(var i = 0; i < inputStr.length; i++) {
code1 = inputStr.charCodeAt(i);
if(code1 < 128) {
outputStr += String.fromCharCode(code1);
}else if(code1 < 224) {
code2 = inputStr.charCodeAt(++i);
outputStr += String.fromCharCode(((code1 & 31) << 6) | (code2 & 63));
}else if(code1 < 240) {
code2 = inputStr.charCodeAt(++i);
code3 = inputStr.charCodeAt(++i);
outputStr += String.fromCharCode(((code1 & 15) << 12) | ((code2 & 63) << 6) | (code3 & 63));
}else {
code2 = inputStr.charCodeAt(++i);
code3 = inputStr.charCodeAt(++i);
code4 = inputStr.charCodeAt(++i);
outputStr += String.fromCharCode(((code1 & 7) << 18) | ((code2 & 63) << 12) |((code3 & 63) << 6) | (code2 & 63));
}
}
return outputStr;
}
let IMG1=new Image();
let IMGINFO=[];
let IMG2=new Image();
let MODE=4;
let SRC1="";
let SRC2="";
function a1(){
requestAnimationFrame(function(){
requestAnimationFrame(function(){
try{
let f=gen(MODE);
if(SRC1){URL.revokeObjectURL(SRC1)}
SRC1=URL.createObjectURL(f);
document.getElementById("a1").href=SRC1;
document.getElementById("img1").src=SRC1;
document.getElementById("a1").style.display="inline";
document.getElementById("a1").download="download.png"
}catch(e){alert("图片生成失败")}
})
})
}
function a2(){
try{
let f=sol();
if(SRC2){URL.revokeObjectURL(SRC2)}
SRC2=URL.createObjectURL(f[0]);
document.getElementById("a2").href=SRC2;
document.getElementById("img2").src=SRC2;
document.getElementById("info2a").style.display="block";
document.getElementById("a2").download=f[1];
document.getElementById("info2").innerHTML=f[1]
}catch(e){alert("图片读取失败")}
}
function select(){
let l=[0,"500K","1M","1.5M","2M"]
MODE=parseInt(document.getElementById("select").value);
document.getElementById("info1").innerHTML="建议里图大小：小于"+l[MODE]
}
function ipt1(){
var oFReader = new FileReader();
var ofile = document.getElementById("ipt1").files[0];
oFReader.readAsDataURL(ofile);
oFReader.onloadend = function(oFRevent){
var osrc = oFRevent.target.result;
IMG1.src=osrc;

}
}

function ipt(){
var oFReader = new FileReader();
var ofile = document.getElementById("ipt").files[0];
oFReader.readAsArrayBuffer(ofile);
oFReader.onloadend = function(oFRevent){
try{
let l=new Uint8Array(oFRevent.target.result);
IMGINFO=[ [l.length,utf8Encode(ofile.name),ofile.type],l];
}catch(e){}
}
}

function ipt2(){
var oFReader = new FileReader();
var ofile = document.getElementById("ipt2").files[0];
oFReader.readAsDataURL(ofile);
oFReader.onloadend = function(oFRevent){
var osrc = oFRevent.target.result;
IMG2.src=osrc;
IMG2.onload=function(){
a2()
}
}
}


function dataURLtoBlob(dataurl) {
var arr = dataurl.split(',');
var _arr = arr[1];
var mime = arr[0].match(/:(.*?);/)[1],
bstr =atob(_arr),
n = bstr.length,
u8arr = new Uint8Array(n);
while (n--) {
u8arr[n] = bstr.charCodeAt(n);
}
return new Blob([u8arr.buffer], {type: mime});
}

function gen(mode){
let modelist=[0,3,mode];
let word=IMGINFO[0].join(String.fromCharCode(1))+String.fromCharCode(0);
let length=2+parseInt((word.length+IMGINFO[1].length)*8/(mode*3))
let ax=Math.sqrt(length/(IMG1.width*IMG1.height));
let wid=Math.ceil(IMG1.width*ax);
let hit=Math.ceil(IMG1.height*ax);
let cv=document.createElement("canvas");
let cvd=cv.getContext("2d");
cv.width=wid;
cv.height=hit;
cvd.fillStyle="#ffffff";
cvd.fillRect(0,0,wid,hit);
cvd.drawImage(IMG1,0,0,wid,hit);

if(document.getElementById("beizhucheckbox").checked){
let w=document.getElementById("beizhu").value;
cvd.font="16px Arial";
cvd.textBaseline="middle";
cvd.fillStyle="rgba(255,255,255,0.75)";
cvd.fillRect(0,0,cvd.measureText(w).width+8,28);
cvd.fillStyle="#000000";
cvd.fillText(w,4,14,wid-8);
}
  
return new File([dataURLtoBlob(en(mode,modelist,cvd.getImageData(0,0,wid,hit),word,IMGINFO[1]," wytk.github.io"))],"download.png",{type:"image/png"})
}
function sol(){
let cv=document.createElement("canvas");
let cvd=cv.getContext("2d");
cv.width=IMG2.width;
cv.height=IMG2.height;
cvd.drawImage(IMG2,0,0);
let imgdata=cvd.getImageData(0,0,IMG2.width,IMG2.height);  
if(imgdata.data[0]%8 !=0 || imgdata.data[1]%8 !=3 || imgdata.data[2]%8 ==0 || imgdata.data[2]%8 >5){
throw "error"
}
let klist=de(imgdata.data[2]%8,imgdata);
let file=new File([klist[1].buffer],utf8Decode(klist[0][1]),{type:klist[0][2]})
return [file,utf8Decode(klist[0][1])]
}


function closer(mode,m,n){
let a=m % mode
if(255-m<=mode/2 || m<mode/2){
return parseInt(m/mode)*mode+n 
}else if(n-a>mode/2){
return parseInt(m/mode)*mode+n-mode 
}else if(a-n>=mode/2){
return parseInt(m/mode)*mode+n+mode 
}else{
return parseInt(m/mode)*mode+n 
}
}


function en(mode,fplist,imgdata,aword,blist,cword){
let aa=Math.ceil(8/3/mode);
let n=imgdata.width*imgdata.height;
let j=0;
let k="";
let i=1;
let mlist=[1,2,4,8,16,32,64,128];
let cv=document.createElement("canvas");
let cvd=cv.getContext("2d");
cv.width=imgdata.width;
cv.height=imgdata.height;
imgdata.data[0]=closer(8,imgdata.data[0],fplist[0]);
imgdata.data[1]=closer(8,imgdata.data[1],fplist[1]);
imgdata.data[2]=closer(8,imgdata.data[2],fplist[2]);
while(i<n && j<aword.length){
k=k+(aword.charCodeAt(j)+256).toString(2).slice(1);
for(let ii=0;ii<aa;ii++){
if(k.length>=mode*3){
imgdata.data[4*i  ]=closer(mlist[mode],imgdata.data[4*i  ],parseInt(k.slice(0     ,mode  ),2));
imgdata.data[4*i+1]=closer(mlist[mode],imgdata.data[4*i+1],parseInt(k.slice(mode  ,mode*2),2));
imgdata.data[4*i+2]=closer(mlist[mode],imgdata.data[4*i+2],parseInt(k.slice(mode*2,mode*3),2));
k=k.slice(mode*3);
i++
}
}
j++
}
j=0;
while(i<n && j<blist.length){
k=k+(blist[j]+256).toString(2).slice(1);
for(let ii=0;ii<aa;ii++){
if(k.length>=mode*3){
imgdata.data[4*i  ]=closer(mlist[mode],imgdata.data[4*i  ],parseInt(k.slice(0     ,mode  ),2));
imgdata.data[4*i+1]=closer(mlist[mode],imgdata.data[4*i+1],parseInt(k.slice(mode  ,mode*2),2));
imgdata.data[4*i+2]=closer(mlist[mode],imgdata.data[4*i+2],parseInt(k.slice(mode*2,mode*3),2));
k=k.slice(mode*3);
i++
}
}
j++
}
j=0;
while(i<n){
k=k+(cword.charCodeAt(j%cword.length)+256).toString(2).slice(1);
for(let ii=0;ii<aa;ii++){
if(k.length>=mode*3){
imgdata.data[4*i  ]=closer(mlist[mode],imgdata.data[4*i  ],parseInt(k.slice(0     ,mode  ),2));
imgdata.data[4*i+1]=closer(mlist[mode],imgdata.data[4*i+1],parseInt(k.slice(mode  ,mode*2),2));
imgdata.data[4*i+2]=closer(mlist[mode],imgdata.data[4*i+2],parseInt(k.slice(mode*2,mode*3),2));
k=k.slice(mode*3);
i++
}
}
j++
}
cvd.putImageData(imgdata,0,0);
return cv.toDataURL();
}

function de(mode,imgdata){
let aa=Math.ceil(3*mode/8);
let n=imgdata.width*imgdata.height;
let j=0;
let k="";
let i=1;
let mlist=[1,2,4,8,16,32,64,128];
let word="";
let blist//=new Uint8Array();
let blength=0;
while(i<n && (word.length==0 || word.slice(-1).charCodeAt(0)>0)){
k=k+(imgdata.data[4*i  ]+256).toString(2).slice(-mode);
k=k+(imgdata.data[4*i+1]+256).toString(2).slice(-mode);
k=k+(imgdata.data[4*i+2]+256).toString(2).slice(-mode);
i++
for(let ii=0;ii<aa;ii++){
if(k.length>=8 && (word.length==0 || word.slice(-1).charCodeAt(0)>0)){
word=word+String.fromCharCode(parseInt(k.slice(0,8),2));
k=k.slice(8);
}
}
}
//word分隔符:","
blength=parseInt(word.split(String.fromCharCode(1))[0]);
if(!(blength>-1)){
throw "error"
}
if(!(word.split(String.fromCharCode(1)).length>2)){
throw "error"
}
blist=new Uint8Array(blength);
if(k.length>=8 && j<blength){
blist[j]=parseInt(k.slice(0,8),2);
k=k.slice(8);
j++
}
while(i<n && j<blength){
k=k+(imgdata.data[4*i  ]+256).toString(2).slice(-mode);
k=k+(imgdata.data[4*i+1]+256).toString(2).slice(-mode);
k=k+(imgdata.data[4*i+2]+256).toString(2).slice(-mode);
i++
for(let ii=0;ii<aa;ii++){
if(k.length>=8 && j<blength){
blist[j]=parseInt(k.slice(0,8),2);
k=k.slice(8);
j++
}
}
}
return [word.split(String.fromCharCode(0))[0].split(String.fromCharCode(1)),blist]
}
window.onload=function(){
let w="<!DOCTYPE "+"html>"+document.documentElement.outerHTML;
document.getElementById("bc").href=URL.createObjectURL(new Blob([w],{type:"text/html"}))
}