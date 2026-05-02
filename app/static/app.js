const btn = document.getElementById('analyze');
const result = document.getElementById('result');
btn.onclick = async () => {
  const text = document.getElementById('input').value.trim();
  if (!text) return;
  result.innerHTML = '<div class="card">Analyzing...</div>';
  const r = await fetch('/api/analyze', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
  const data = await r.json();
  let html = `<div class="card"><span class="badge">Overall: ${data.overall_label}</span> Confidence: ${data.confidence}</div>`;
  for (const c of data.claims) {
    html += `<div class="card"><h3>${c.claim}</h3><p>Classifier: ${c.classifier_label} (${c.classifier_confidence}) | Routed: ${c.routed_to_verifier}</p><p><b>Verdict:</b> ${c.final_verdict}</p><p>${c.explanation}</p>`;
    if (c.evidence.length) html += '<h4>Evidence</h4>';
    for (const e of c.evidence) html += `<div class='ev'><b>${e.title}</b> (${e.source})<br/>${e.snippet}<br/>score=${e.score.toFixed(3)}</div>`;
    html += '</div>';
  }
  result.innerHTML = html;
};
