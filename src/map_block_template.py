MAP_BODY_TEMPLATE = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>
/* --- interactive map page layout: framed map + real legend sidebar --- */
.map-layout{display:flex;gap:14px;height:calc(100vh - 57px - 28px);padding:14px;box-sizing:border-box}
.map-frame{flex:1 1 auto;position:relative;border:1px solid #e0e0e0;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(27,67,50,.10);background:#f9fafb}
#map{position:absolute;inset:0;width:100%;height:100%}
.map-sidebar{flex:0 0 295px;max-width:295px;overflow-y:auto;background:#fff;border:1px solid #e0e0e0;border-radius:12px;box-shadow:0 2px 10px rgba(27,67,50,.10);padding:14px 16px;font-size:.85rem;line-height:1.5}
.map-sidebar h3{margin:0 0 8px;color:#1b4332;font-size:.98rem;font-weight:800;letter-spacing:-.01em}
.side-sec + .side-sec{margin-top:14px;padding-top:12px;border-top:1px solid #e0e0e0}
.leg{display:flex;align-items:center;gap:9px;margin:7px 0}
.leg .sq{width:11px;height:11px;flex:none;transform:rotate(45deg);border:1px solid rgba(27,67,50,.55)}
.leg .ring{width:14px;height:14px;flex:none;border:2px dashed #f77f00;border-radius:50%}
.leg .dot{width:12px;height:12px;flex:none;border-radius:50%;border:1.5px solid #fff;box-shadow:0 1px 2px rgba(0,0,0,.25)}
.leg .star{color:#f77f00;font-size:1.15rem;flex:none;line-height:1}
.leg .mon{width:10px;height:10px;flex:none;background:#2d6a4f;transform:rotate(45deg);border:2px solid #fff;box-shadow:0 1px 2px rgba(0,0,0,.3)}
.fact{display:flex;gap:9px;margin:7px 0;align-items:baseline}
.fact .n{font-weight:800;color:#52b788;font-size:1.02rem;min-width:28px}
.fact .t{color:#1a1a2e}
.side-sec p{margin:6px 0;color:#1a1a2e}
.side-note{font-size:.76rem;color:#555}
a.side-link{color:#2d6a4f;text-decoration:none;font-weight:600}
a.side-link:hover{text-decoration:underline}
.leaflet-container{font:inherit;background:#fff}
.leaflet-popup-content{font-size:.85rem;line-height:1.45}
.leaflet-popup-content b{color:#1b4332}
.farm-label{background:#1b4332;color:#fff;padding:2px 7px;border-radius:4px;font-weight:700;font-size:.72rem;white-space:nowrap;border:none;box-shadow:0 1px 4px rgba(0,0,0,.4)}
@media (max-width:840px){
  .map-layout{flex-direction:column;height:auto}
  .map-frame{height:62vh;flex:none}
  .map-sidebar{flex:none;max-width:none;width:auto}
}
</style>
<div class="map-layout">
  <div class="map-frame"><div id="map"></div></div>
  <aside class="map-sidebar">
    <div class="side-sec">
      <h3>Legend</h3>
      <div class="leg"><span class="sq" style="background:#1b4332"></span>Storage tank (OSM)</div>
      <div class="leg"><span class="sq" style="background:#2d6a4f"></span>Oil parcel (OSM)</div>
      <div class="leg"><span class="ring"></span>1-mile fence-line buffer</div>
      <div class="leg"><span class="dot" style="background:#1b4332"></span>Public school (7)</div>
      <div class="leg"><span class="dot" style="background:#d62828"></span>Child care program (25)</div>
      <div class="leg"><span class="dot" style="background:#7b2cbf"></span>Senior housing (9)</div>
      <div class="leg"><span class="star">&#9733;</span>Tank farm facility (6)</div>
      <div class="leg"><span class="dot" style="background:#d62828;opacity:.35;border-color:#d62828"></span>Permitted VOC tpy (&rarr; bubble size)</div>
      <div class="leg"><span class="mon"></span>DEP VOC monitor (7)</div>
    </div>
    <div class="side-sec">
      <h3>Key Facts</h3>
      <div class="fact"><span class="n">42</span><span class="t">sensitive sites within 1 mile of a tank-farm fence line</span></div>
      <div class="fact"><span class="n">7</span><span class="t">public schools &mdash; all of them</span></div>
      <div class="fact"><span class="n">25</span><span class="t">licensed child care programs (centers, nurseries, family homes)</span></div>
      <div class="fact"><span class="n">9</span><span class="t">senior housing facilities</span></div>
      <div class="fact"><span class="n">~594</span><span class="t">tons/yr licensed VOC caps across the six facilities (DEP orders; bubble size shows each)</span></div>
      <p style="margin-top:8px">Closest pairings: <b>Kaler Elementary</b> 0.04 mi from the Pipe Line parcel; <b>Betsy Ross House</b> adjacent to the Gulf/Sunoco parcel; <b>Growing Learners</b> child care on the Sprague fence line.</p>
    </div>
    <div class="side-sec">
      <h3>About this map</h3>
      <p><b>How to read it.</b> Shaded polygons are the tank farm structures mapped in OpenStreetMap
      (individual storage tanks and the parcels that contain them). The dashed amber boundary is the
      <b>1-mile fence-line buffer</b> &mdash; the union of all tank/parcel outlines extended one statute mile;
      receptors inside that zone are the sites counted in the research. Click any marker for measured
      distances and permit details.</p>
      <p class="side-note">Distances are straight-line fence-line distances, not walking routes. Fence-line
      geometry is community-mapped OSM data; City of South Portland assessor parcels would be the
      parcel-exact upgrade. DEP monitor placements are approximate (named street locations). Basemap is faded
      outside the buffer so the study area stands out.</p>
      <p style="margin-top:8px">
        <a class="side-link" href="report.html">Research report</a> &middot;
        <a class="side-link" href="factcheck.html">Fact-check log</a> &middot;
        <a class="side-link" href="data.html">Data files</a> &middot;
        <a class="side-link" href="https://github.com/cristoslc/south-portland-tank-farms">GitHub repo</a>
      </p>
      <p class="side-note" style="margin-top:6px">Sources: Maine DEP air license orders; OCFS Child Care
      Choices (captured Sept 24, 2026); NCES; SPHA; OpenStreetMap (ODbL).</p>
    </div>
  </aside>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const FARMS = __FARMS__;
const RECS = __RECS__;
const MON = __MON__;
const POLYS = __POLYS__;
const BUFFER_RINGS = __BUFFER__;
const map = L.map('map').setView([43.6335, -70.278], 14);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19, attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors (ODbL)'}).addTo(map);

const icons = {school:L.divIcon({className:'',html:'<div style="width:14px;height:14px;background:#1b4332;transform:rotate(45deg);border:1.5px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[14,14],iconAnchor:[7,7]}),
 childcare:L.divIcon({className:'',html:'<div style="width:12px;height:12px;background:#d62828;transform:rotate(45deg);border:1.5px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[12,12],iconAnchor:[6,6]}),
 senior:L.divIcon({className:'',html:'<div style="width:13px;height:13px;background:#7b2cbf;border:1.5px solid #fff;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[13,13],iconAnchor:[6,6]})};

/* fade basemap outside the buffer: white world-donut with the buffer as a hole, under data layers */
const WORLD = [[85,-179],[85,179],[-85,179],[-85,-179]];
L.polygon([WORLD, ...BUFFER_RINGS],{stroke:false,fillColor:'#ffffff',fillOpacity:0.70,interactive:false}).addTo(map);

POLYS.forEach(p=>{L.polygon(p.ring.map(c=>[c[1],c[0]]),{color:'#1b4332',weight:0.7,fillColor:p.kind==='tank'?'#1b4332':'#2d6a4f',fillOpacity:0.55}).bindPopup(`<b>${p.kind==='tank'?'Storage tank':'Oil parcel'}</b><br>Farm: ${p.farm}`).addTo(map);});

L.polygon(BUFFER_RINGS,{color:'#f77f00',weight:1.6,dashArray:'6 5',fillColor:'#f77f00',fillOpacity:0.05,interactive:false}).addTo(map);

FARMS.forEach(f=>{L.marker([f.lat,f.lon]).bindPopup(`<b>${f.name}</b><br>${f.addr}<br>License ${f.lic} &middot; VOC cap ${f.voc} tpy<br>Renewal: ${f.renew}`).addTo(map);
L.marker([f.lat,f.lon],{icon:L.divIcon({className:'',html:`<div class="farm-label">${f.name.split(' ')[0]}</div>`})}).addTo(map);});

FARMS.forEach(f=>{L.circle([f.lat,f.lon],{radius:12*Math.sqrt(f.voc),color:'#d62828',weight:1,fillColor:'#d62828',fillOpacity:0.18}).bindPopup(`<b>Petroleum terminal</b><br>${f.name}<br>Petroleum VOC: <b>${f.voc} tons/yr</b>`).addTo(map);});
RECS.forEach(r=>{L.marker([r.lat,r.lon],{icon:icons[r.cat]}).bindPopup(`<b>${r.name}</b><br>${r.cat==='school'?'Public school':r.cat==='senior'?'Senior housing':'Child care program'}<br><b>${r.min} mi</b> to ${r.near} fence line`).addTo(map);});

MON.forEach(m=>{L.marker([m.lat,m.lon],{icon:L.divIcon({className:'',html:'<div style="width:10px;height:10px;background:#2d6a4f;transform:rotate(45deg);border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[14,14],iconAnchor:[7,7]})}).bindPopup(`<b>${m.code}</b> - ${m.name}<br><i>DEP VOC monitoring station (location approximate)</i>`).addTo(map);});

/* invalidate size after layout settles so tiles fill the frame */
setTimeout(()=>map.invalidateSize(), 250);
</script>"""