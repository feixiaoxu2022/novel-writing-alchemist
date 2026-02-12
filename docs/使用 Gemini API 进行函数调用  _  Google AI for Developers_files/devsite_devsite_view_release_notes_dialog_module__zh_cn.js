(function(_ds){var window=this;var lDa=function(a){a.eventHandler.listen(a,"DropdownItemClicked",b=>{kDa(a,b)})},kDa=async function(a,b){const c=b.getBrowserEvent().detail.id;b=a.querySelector(".devsite-dialog-contents");const d=a.querySelector(`#date-section-${c}`);let e,f,g,h;const k=((g=d==null?void 0:(e=d.getBoundingClientRect())==null?void 0:e.top)!=null?g:0)-((h=b==null?void 0:(f=b.getBoundingClientRect())==null?void 0:f.top)!=null?h:0);d&&b&&b.scrollBy({top:k,behavior:"smooth"});let l,m;a.Lj=(m=(l=a.Rk.find(n=>n.id===c))==
null?void 0:l.title)!=null?m:"";a.o.Va(a.Lj)},nDa=function(a){const b=new IntersectionObserver(c=>{c.forEach(d=>{mDa(a,d.isIntersecting,d)})},{root:a.querySelector(".devsite-dialog-contents")});a.querySelectorAll(".release-note-date-section .release-note").forEach(c=>{b.observe(c)})},mDa=function(a,b,c){let d;const e={id:(d=c.target.getAttribute("id"))!=null?d:"",type:Number(c.target.getAttribute("type"))};if(b){let f;a.Dh=[...((f=a.Dh)!=null?f:[]),e]}else a.Dh=[...a.Dh.filter(f=>f.id!==e.id)]},oDa=
function(a){switch(a){case 4:return{title:"Feature",color:"green"};case 8:return{title:"Announcement",color:"yellow"};case 2:return{title:"Change",color:"yellow"};case 9:return{title:"Libraries",color:"blue"};case 3:return{title:"Fixed",color:"blue"};case 1:return{title:"Breaking",color:"red"};case 5:return{title:"Deprecated",color:"red"};case 6:return{title:"Issue",color:"red"};case 7:return{title:"Security",color:"orange"};default:return{title:"Unspecified",color:"grey"}}},b9=function(a,b){b=oDa(b);
return(0,_ds.N)` <span
      class="release-note-type-chip
          ${a} ${b.color}">
      ${b.title}
    </span>`},pDa=function(a,b){const c=b.replace(/,?\s/g,"").toLowerCase();let d;return(0,_ds.N)`
      <div class="release-note-date-section" id="date-section-${c}">
        <h3 class="release-note-date-header">${b}</h3>
        ${[...((d=a.releaseNotes.get(b))!=null?d:[])].map((e,f)=>{f=`${c}-${f}`;var g;(g=_ds.y(e,_ds.aca,4))?(g=_ds.Dk(g,2),g=g===null||g===void 0?null:_ds.rg(g)):g=null;return(0,_ds.N)` <div
        class="release-note"
        id="${f}"
        type="${_ds.yk(e,2)}">
        ${b9("large",_ds.yk(e,2))}
        <div class="release-note-content">
          ${g?(0,_ds.N)`${(0,_ds.rP)(g)}`:(0,_ds.N)`<p>${_ds.z(e,1)}</p>`}
        </div>
      </div>`})}
      </div>
    `},c9=class extends _ds.mC{constructor(){super(["devsite-dialog","devsite-dropdown-list"]);this.eventHandler=new _ds.u;this.releaseNotes=new Map;this.hideFooter=!1;this.Lj="";this.Rk=[];this.Dh=[];this.o=new _ds.fi(async a=>{this.Ba({category:"Site-Wide Custom Events",action:"release notes: view old note",label:`${await _ds.ax(_ds.D().href)} : ${a}`})},100)}Ma(){return this}async connectedCallback(){super.connectedCallback();this.Lj=[...this.releaseNotes.keys()][0];this.Rk=[...this.releaseNotes.keys()].map(a=>
({id:a.replace(/,?\s/g,"").toLowerCase(),title:a}));lDa(this)}disconnectedCallback(){super.disconnectedCallback()}m(a){super.m(a);nDa(this)}render(){return(0,_ds.N)`
      <div class="devsite-dialog-header">
        <div>
          <h3 class="no-link title">
            ${"\u7248\u672c\u8bf4\u660e"}
          </h3>
          <div class="chip-wrapper">
            ${[...(new Set(this.Dh.map(a=>a.type)))].map(a=>b9("small",a))}
          </div>
        </div>
        <devsite-dropdown-list
            .listItems=${this.Rk}>
          <p slot="toggle" class="selected-date-toggle">${this.Lj}</p>
        </devsite-dropdown-list>
      </div>
      <div class="devsite-dialog-contents">
        ${[...this.releaseNotes.keys()].map(a=>pDa(this,a))}
      </div>
      ${_ds.M(this.hideFooter,()=>"",()=>(0,_ds.N)`
              <div class="devsite-dialog-footer devsite-dialog-buttons">
                <button class="button devsite-dialog-close">
                  Close
                </button>
              </div>
            `)}
      `}};_ds.w([_ds.H({type:Map}),_ds.x("design:type",Object)],c9.prototype,"releaseNotes",void 0);_ds.w([_ds.H({type:Boolean}),_ds.x("design:type",Object)],c9.prototype,"hideFooter",void 0);_ds.w([_ds.I(),_ds.x("design:type",Object)],c9.prototype,"Lj",void 0);_ds.w([_ds.I(),_ds.x("design:type",Array)],c9.prototype,"Rk",void 0);_ds.w([_ds.I(),_ds.x("design:type",Array)],c9.prototype,"Dh",void 0);try{customElements.define("devsite-view-release-notes-dialog",c9)}catch(a){console.warn("devsite.app.customElement.DevsiteViewReleaseNotesDialog",a)};})(_ds_www);
