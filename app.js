const fileInput = document.getElementById('file');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const video = document.getElementById('video');
const btnCinematic = document.getElementById('btnCinematic');
const btnReset = document.getElementById('btnReset');
const btnSuggest = document.getElementById('btnSuggest');
const btnApply = document.getElementById('btnApply');
const notes = document.getElementById('notes');
const suggestionsEl = document.getElementById('suggestions');
const variantsEl = document.getElementById('variants');

let img = new Image();
let originalBitmap = null;
let currentSuggestion = null;

function drawImage(imgEl){
  const w = imgEl.videoWidth || imgEl.width;
  const h = imgEl.videoHeight || imgEl.height;
  const maxW = 640;
  const scale = Math.min(1, maxW / w);
  canvas.width = Math.floor(w*scale);
  canvas.height = Math.floor(h*scale);
  ctx.filter = 'none';
  ctx.drawImage(imgEl, 0, 0, canvas.width, canvas.height);
  originalBitmap = ctx.getImageData(0,0,canvas.width, canvas.height);
}

fileInput.addEventListener('change', e => {
  const f = e.target.files[0];
  if(!f) return;
  const url = URL.createObjectURL(f);
  if(f.type.startsWith('image/')){
    video.style.display = 'none';
    img.onload = () => drawImage(img);
    img.src = url;
  } else if (f.type.startsWith('video/')){
    video.style.display = 'block';
    video.src = url;
    video.addEventListener('loadeddata', () => {
      drawImage(video);
      video.currentTime = 0;
    }, { once: true });
  }
});

btnCinematic.addEventListener('click', () => {
  if(!originalBitmap) return;
  ctx.putImageData(originalBitmap,0,0);
  ctx.filter = 'contrast(1.08) saturate(0.9) brightness(1.03)';
  ctx.drawImage(canvas,0,0);
  const grd = ctx.createRadialGradient(canvas.width/2, canvas.height/2, Math.min(canvas.width,canvas.height)/4, canvas.width/2, canvas.height/2, Math.max(canvas.width,canvas.height)/1.2);
  grd.addColorStop(0,'rgba(0,0,0,0)');
  grd.addColorStop(1,'rgba(0,0,0,0.35)');
  ctx.fillStyle = grd;
  ctx.fillRect(0,0,canvas.width, canvas.height);
});

btnReset.addEventListener('click', () => {
  if(!originalBitmap) return;
  ctx.putImageData(originalBitmap,0,0);
  ctx.filter = 'none';
});

async function getClaudeSuggestion(text) {
  const res = await fetch('/api/claude', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return res.json();
}

btnSuggest.addEventListener('click', async () => {
  btnSuggest.disabled = true;
  suggestionsEl.textContent = 'Thinking...';
  try {
    const result = await getClaudeSuggestion(notes.value || 'Make it pop');
    suggestionsEl.textContent = JSON.stringify(result, null, 2);
  } catch {
    suggestionsEl.textContent = 'Error getting suggestion.';
  }
  btnSuggest.disabled = false;
});

btnApply.addEventListener('click', async () => {
  if(!currentSuggestion || !originalBitmap) return;
  if(currentSuggestion.action === 'edit'){
    btnCinematic.click();
  } else if (currentSuggestion.action === 'caption'){
    ctx.putImageData(originalBitmap,0,0);
    ctx.fillStyle = 'rgba(0,0,0,0.6)';
    ctx.fillRect(0, canvas.height-48, canvas.width, 48);
    ctx.fillStyle = 'white';
    ctx.font = '20px system-ui';
    ctx.fillText(currentSuggestion.params.text || 'New caption', 16, canvas.height-16);
  } else {
    btnCinematic.click();
  }
  variantsEl.innerHTML = '';
  for(let i=0;i<2;i++){
    const thumb = document.createElement('canvas');
    thumb.width = 240; thumb.height = Math.floor(canvas.height*(240/canvas.width));
    const tctx = thumb.getContext('2d');
    tctx.drawImage(canvas, 0, 0, thumb.width, thumb.height);
    const div = document.createElement('div'); div.className='variant';
    div.appendChild(thumb);
    const variantData = thumb.toDataURL(); // base64 of the variant image
    const res = await fetch('/api/fetch-score', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ image: variantData })
    });
    const { score } = await res.json();
    const p = document.createElement('p'); p.textContent = 'Score: '+score;
    div.appendChild(p);
    variantsEl.appendChild(div);
  }
});
