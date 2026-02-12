(function(_ds){var window=this;var gwa=async function(a){a.eventHandler.listen(a,"DropdownToggled",c=>{c=c.getBrowserEvent();let d;a.Ba({category:"devsiteLlmTools",action:((d=c.detail)==null?0:d.open)?"llm_tools_dropdown_open":"llm_tools_dropdown_close",label:"dropdown_toggle"})});a.eventHandler.listen(a,"DropdownItemClicked",c=>{c=c.getBrowserEvent();if(c=a.ea.get(c.detail.id))a.Ba({category:"devsiteLlmTools",action:c.By,label:c.analyticsLabel}),c.action()});const b=fwa();b&&(a.o=b,a.Ba({category:"devsiteLlmTools",action:"llm_tools_button_impression"}))},
fwa=function(){const a=_ds.D();a.pathname=`${a.pathname}.md.txt`;return _ds.hg(a.href)},hwa=async function(a){if(!a.o)return null;a.Gl=!0;try{const b=await fetch(_ds.Oo(a.o.toString()).href);if(b)return await b.text()}catch(b){}finally{a.Gl=!1}return null},iwa=async function(a){try{return a.ma||(a.ma=await hwa(a)),a.ma}catch(b){}return null},E4=function(a,b){a.dispatchEvent(new CustomEvent("devsite-show-custom-snackbar-msg",{detail:{msg:b,showClose:!1},bubbles:!0}))},jwa=async function(a){a.Ba({category:"devsiteLlmTools",
action:"llm_tools_copy_markdown_click",label:"main_button"});const b=await iwa(a);b?await _ds.jz(b):E4(a,"\u672a\u80fd\u590d\u5236\u9875\u9762")},F4=class extends _ds.mC{constructor(){super(...arguments);this.Gl=!1;this.eventHandler=new _ds.u;this.ma=null;this.o=void 0;this.items=[{id:"open-markdown",title:"\u4ee5 Markdown \u683c\u5f0f\u67e5\u770b",action:()=>{this.o?_ds.ug(window,this.o,"_blank"):E4(this,"\u672a\u80fd\u6253\u5f00 Markdown \u89c6\u56fe\u3002")},By:"llm_tools_open_markdown_click",
analyticsLabel:"dropdown_item"}];this.oa=this.items.map(a=>({id:a.id,title:a.title}));this.ea=new Map(this.items.map(a=>[a.id,a]))}Ma(){return this}connectedCallback(){super.connectedCallback();gwa(this)}disconnectedCallback(){super.disconnectedCallback();_ds.F(this.eventHandler)}render(){return(0,_ds.N)`
      <div
        class="devsite-llm-tools-container"
        role="group"
        aria-label="${"LLM \u5de5\u5177"}">
        <div class="devsite-llm-tools-button-container">
          <button
            type="button"
            class="button button-white devsite-llm-tools-button"
            ?disabled="${this.Gl}"
            @click=${()=>{jwa(this)}}
            aria-label="${"\u5c06\u9875\u9762\u590d\u5236\u4e3a Markdown"}"
            data-title="${"\u590d\u5236\u9875\u9762"}">
            <span class="material-icons icon-copy" aria-hidden="true"></span>
          </button>
        </div>
        <div class="devsite-llm-tools-dropdown-container">
          <devsite-dropdown-list
            .listItems="${this.oa}"
            open-dropdown-aria-label="${"\u66f4\u591a LLM \u5de5\u5177\u9009\u9879"}"
            close-dropdown-aria-label="${"\u5173\u95ed LLM \u5de5\u5177\u9009\u9879\u83dc\u5355"}">
          </devsite-dropdown-list>
        </div>
      </div>
    `}};F4.prototype.disconnectedCallback=F4.prototype.disconnectedCallback;_ds.w([_ds.I(),_ds.x("design:type",Object)],F4.prototype,"Gl",void 0);try{customElements.define("devsite-llm-tools",F4)}catch(a){console.warn("Unrecognized DevSite custom element - DevsiteLlmTools",a)};})(_ds_www);
