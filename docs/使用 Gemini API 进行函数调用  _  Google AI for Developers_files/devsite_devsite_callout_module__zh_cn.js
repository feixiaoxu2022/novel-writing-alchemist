(function(_ds){var window=this;var gra=async function(a,b){const c=a.o;let d;const e=b.id!==((d=a.oa)==null?void 0:d.id);e&&(a.className=b.id,a.eventLabel=`devsite-callout-${b.id}`,a.o=new _ds.aQ(b.origin,a.eventLabel));a.oa=b;c&&e&&await _ds.$P(c)},hra=async function(a){a.eventHandler.listen(document.body,"devsite-before-page-change",()=>{a.hide()})},ira=async function(a,b){let c;((c=a.callout)==null?0:c.Gf)&&a.callout.Gf(b);await a.hide();a.Ba({category:"Site-Wide Custom Events",action:"callout-dismiss",label:a.eventLabel})},
P_=async function(a,b){let c;((c=a.callout)==null?0:c.Ke)&&a.callout.Ke(b);let d;((d=a.callout)==null?0:d.qj)||await a.hide();a.Ba({category:"Site-Wide Custom Events",action:"callout-action",label:a.eventLabel})},jra=function(a){let b,c;if(((b=a.callout)==null?0:b.Me)&&`${(c=a.callout)==null?void 0:c.Me}`){let d,e;return(0,_ds.N)`<div class="devsite-callout-branding">
          <img
            class="devsite-callout-branding-image"
            src="${(d=a.callout)==null?void 0:d.Me}"
            alt="${((e=a.callout)==null?void 0:e.Kg)||""}" />
        </div>
        <hr />`}return(0,_ds.N)``},kra=function(a){let b,c;if(((b=a.callout)==null?0:b.rq)&&`${(c=a.callout)==null?void 0:c.rq}`){let d,e;return(0,_ds.N)`<div class="devsite-callout-hero">
        <img
          class="devsite-callout-hero-image"
          src="${(d=a.callout)==null?void 0:d.rq}"
          alt="${((e=a.callout)==null?void 0:e.zA)||""}" />
      </div>`}return(0,_ds.N)``},lra=function(a){let b;if((b=a.callout)==null?0:b.Cu)return(0,_ds.N)``;let c;return(0,_ds.N)` <div class="devsite-callout-header">
        <h2>${((c=a.callout)==null?void 0:c.title)||""}</h2>
      </div>`},mra=function(a){let b;if((b=a.callout)==null?0:b.loading)return(0,_ds.N)`<div class="devsite-callout-body"
        ><devsite-spinner size="24"></devsite-spinner
      ></div>`;let c,d;var e;if(((c=a.callout)==null?0:c.body)&&`${(d=a.callout)==null?void 0:d.body}`){{let f;if(((f=a.callout)==null?void 0:f.body)instanceof _ds.qg){let g;a=(0,_ds.N)`${(0,_ds.rP)((g=a.callout)==null?void 0:g.body)}`}else a=(0,_ds.N)`${(e=a.callout)==null?void 0:e.body}`}e=(0,_ds.N)`<div class="devsite-callout-body">
        ${a}
      </div>`}else e=(0,_ds.N)``;return e},nra=function(a){var b;if((b=a.callout)==null||!b.Uc)return(0,_ds.N)``;var c;b=(0,_ds.nz)({button:!0,"button-primary":!0,"devsite-callout-action":!0,"button-disabled":((c=a.callout)==null?void 0:c.Dt)||!1});let d;c=(d=a.callout)==null?void 0:d.yy;let e;if((e=a.callout)==null?0:e.yk){let g,h;return(0,_ds.N)`<a
        @click=${k=>{P_(a,k)}}
        href="${((g=a.callout)==null?void 0:g.yk)||""}"
        class="${b}"
        aria-label=${c!=null?c:_ds.AA}
        data-title=${c!=null?c:_ds.AA}>
        ${((h=a.callout)==null?void 0:h.Uc)||""}
      </a>`}let f;return(0,_ds.N)`<button
        @click=${g=>{P_(a,g)}}
        class="${b}"
        aria-label=${c!=null?c:_ds.AA}
        data-title=${c!=null?c:_ds.AA}>
        ${((f=a.callout)==null?void 0:f.Uc)||""}
      </button>`},Q_=class extends _ds.mC{set callout(a){gra(this,a)}get callout(){return this.oa}get open(){let a;return((a=this.ma.value)==null?void 0:a.open)||!1}constructor(){super(["devsite-spinner"]);this.eventHandler=new _ds.u;this.eventLabel="";this.oa=this.ea=this.o=null;this.ma=new _ds.nP}connectedCallback(){super.connectedCallback();hra(this)}disconnectedCallback(){super.disconnectedCallback();let a;(a=this.o)==null||a.cancel()}Ma(){return this}async ready(){await this.j}async show(){await this.ready();
if(!this.open){var a;await ((a=this.o)==null?void 0:a.schedule(()=>{document.activeElement instanceof HTMLElement&&(this.ea=document.activeElement);var b;(b=this.ma.value)==null||b.show();let c;(c=this.querySelector(".devsite-callout-action"))==null||c.focus();let d;b={message:"\u201c"+(((d=this.callout)==null?void 0:d.title)||"")+"\u201d\u5bf9\u8bdd\u6846\u5df2\u6253\u5f00"};document.body.dispatchEvent(new CustomEvent("devsite-a11y-announce",{detail:b}));this.Ba({category:"Site-Wide Custom Events",
action:"callout-impression",label:this.eventLabel,nonInteraction:!0})},()=>{let b;(b=this.ma.value)==null||b.close();let c;(c=this.querySelector(".devsite-callout-action"))==null||c.blur();this.ea&&this.ea.focus()}))}}async hide(){await this.ready();let a;await ((a=this.o)==null?void 0:_ds.$P(a))}render(){if(!this.callout)return(0,_ds.N)``;let a;return(0,_ds.N)`
      <dialog
        closedby="none"
        ${(0,_ds.pP)(this.ma)}
        aria-label="${((a=this.callout)==null?void 0:a.title)||""}"
        class="devsite-callout">
        ${jra(this)} ${kra(this)}
        ${lra(this)} ${mra(this)}
        <div class="devsite-callout-buttons">
          <button
            @click=${b=>{ira(this,b)}}
            class="button button-dismiss devsite-callout-dismiss">
            ${"\u5173\u95ed"}
          </button>
          ${nra(this)}
        </div>
      </dialog>
    `}};_ds.w([_ds.H({Aa:!1}),_ds.x("design:type",Object),_ds.x("design:paramtypes",[Object])],Q_.prototype,"callout",null);try{customElements.define("devsite-callout",Q_)}catch(a){console.warn("Unrecognized DevSite custom element - DevsiteCallout",a)};})(_ds_www);
