(function(_ds){var window=this;var d9=class extends _ds.mC{constructor(){super(["devsite-dialog","devsite-dropdown-list","devsite-view-release-notes-dialog"]);this.Sr=!1;this.releaseNotes=new Map;this.dialog=null;this.path="";this.label="\u7248\u672c\u8bf4\u660e";this.disableAutoOpen=!1}Ma(){return this}async connectedCallback(){super.connectedCallback();try{this.path||(this.path=await _ds.ax(_ds.D().href)),this.releaseNotes=await _ds.yz(this.path)}catch(a){}this.releaseNotes.size===0?this.remove():(this.Sr=!0,this.disableAutoOpen||
location.hash!=="#release__notes"||this.o())}disconnectedCallback(){super.disconnectedCallback();let a;(a=this.dialog)==null||a.remove();this.dialog=null}o(a){a&&(a.preventDefault(),a.stopPropagation());let b;(b=this.dialog)==null||b.remove();this.dialog=document.createElement("devsite-dialog");this.dialog.classList.add("devsite-view-release-notes-dialog-container");_ds.OA((0,_ds.N)`
      <devsite-view-release-notes-dialog
        .releaseNotes=${this.releaseNotes}>
      </devsite-view-release-notes-dialog>
    `,this.dialog);document.body.appendChild(this.dialog);this.dialog.open=!0;this.Ba({category:"Site-Wide Custom Events",action:"release notes: view note",label:`${this.path}`})}render(){if(!this.Sr)return delete this.dataset.shown,(0,_ds.N)``;this.dataset.shown="";return(0,_ds.N)`
      <button class="view-notes-button" @click="${this.o}">
        ${this.label}
      </button>
    `}};_ds.w([_ds.I(),_ds.x("design:type",Object)],d9.prototype,"Sr",void 0);_ds.w([_ds.H({type:String}),_ds.x("design:type",Object)],d9.prototype,"path",void 0);_ds.w([_ds.H({type:String}),_ds.x("design:type",Object)],d9.prototype,"label",void 0);_ds.w([_ds.H({type:Boolean,Aa:"disable-auto-open"}),_ds.x("design:type",Object)],d9.prototype,"disableAutoOpen",void 0);try{customElements.define("devsite-view-release-notes",d9)}catch(a){console.warn("devsite.app.customElement.DevsiteViewReleaseNotes",a)};})(_ds_www);
