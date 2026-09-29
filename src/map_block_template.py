MAP_BODY_TEMPLATE = """
<div id="map"></div>
<details class="map-explain"><summary>How to read this map / data notes</summary>
  <p><b>How to read this map.</b> Shaded polygons are the tank farm structures mapped in OpenStreetMap
  (individual storage tanks and the parcels that contain them). The dashed amber boundary is the
  <b>1-mile fence-line buffer</b> &mdash; the union of all tank/parcel outlines extended one statute mile;
  receptors inside that zone are the sites counted in the research. Click any marker for measured distances
  and permit details.</p>
  <p>Straight-line distances to OSM-mapped fence lines, not walking distances. Fence-line geometry is
  community-mapped OSM data. Sources: Maine DEP air license orders, OCFS Child Care Choices (Sept 24 2026),
  NCES, SPHA. DEP monitor placements are approximate. Datasets:
  <a href="data.html">data files page</a> &middot; Repo:
  <a href="https://github.com/cristoslc/south-portland-tank-farms">github</a></p>
</details>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const FARMS = __FARMS__;
const RECS = __RECS__;
const MON = __MON__;
const POLYS = __POLYS__;
const BUFFER_RINGS = __BUFFER__;
const map = L.map('map').setView([43.6335, -70.278], 14);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19, attribution:'&copy; OpenStreetMap contributors (ODbL)'}).addTo(map);

const icons = {school:L.divIcon({className:'',html:'<div style="width:14px;height:14px;background:#1b4332;transform:rotate(45deg);border:1.5px solid #fff"></div>',iconSize:[14,14],iconAnchor:[7,7]}),
 childcare:L.divIcon({className:'',html:'<div style="width:12px;height:12px;background:#d62828;transform:rotate(45deg);border:1.5px solid #fff"></div>',iconSize:[12,12],iconAnchor:[6,6]}),
 senior:L.divIcon({className:'',html:'<div style="width:13px;height:13px;background:#7b2cbf;border:1.5px solid #fff;border-radius:2px"></div>',iconSize:[13,13],iconAnchor:[6,6]})};
/* fade basemap outside the buffer */
const WORLD = [[85,-179],[85,179],[-85,179],[-85,-179]];
L.polygon([WORLD, ...BUFFER_RINGS],{stroke:false,fillColor:'#ffffff',fillOpacity:0.70,interactive:false}).addTo(map);
POLYS.forEach(p=>{L.polygon(p.ring.map(c=>[c[1],c[0]]),{color:'#1b4332',weight:0.7,fillColor:p.kind==='tank'?'#1b4332':'#2d6a4f',fillOpacity:0.5}).bindPopup(`<b>${p.kind==='tank'?'Storage tank':'Oil parcel'}</b><br>Farm: ${p.farm}`).addTo(map);});
L.polygon(BUFFER_RINGS,{color:'#f77f00',weight:1.6,dashArray:'6 5',fillColor:'#f77f00',fillOpacity:0.06}).bindPopup('<b>1-mile fence-line buffer</b><br>Union of all tank/parcel polygons buffered one statute mile. Receptors inside this zone are the sites counted in the research.').addTo(map);
FARMS.forEach(f=>{L.marker([f.lat,f.lon]).bindPopup(`<b>${f.name}</b><br>${f.addr}<br>License ${f.lic} &middot; VOC cap ${f.voc} tpy<br>Renewal: ${f.renew}`).addTo(map);
L.marker([f.lat,f.lon],{icon:L.divIcon({className:'',html:`<div style="background:#1b4332;color:#fff;padding:2px 7px;border-radius:4px;font-weight:700;font-size:.72rem;white-space:nowrap">${f.name.split(' ')[0]}</div>`})}).addTo(map);});
RECS.forEach(r=>{L.marker([r.lat,r.lon],{icon:icons[r.cat]}).bindPopup(`<b>${r.name}</b><br>${r.cat==='school'?'Public school':r.cat==='senior'?'Senior housing':'Child care program'}<br><b>${r.min} mi</b> to ${r.near} fence line`).addTo(map);});
MON.forEach(m=>{L.marker([m.lat,m.lon],{icon:L.divIcon({className:'',html:'<div style="width:12px;height:12px;background:#2d6a4f;border:2px solid #fff"></div>'})}).bindPopup(`<b>${m.code}</b> - ${m.name}<br><i>DEP VOC monitor (approximate)</i>`).addTo(map);});
</script>"""