// docs/js/clarity.js
(function() {
  // OPTIONAL: gate load behind a simple consent flag you control
  const consent = localStorage.getItem("analytics_consent") === "yes";
  if (!consent) return;

  // ---- paste your Clarity snippet, but with defer + secure insert ----
  // Replace "YOUR-CLARITY-ID" with your project ID
  (function(c,l,a,r,i,t,y){
      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=true;t.defer=true;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "twpirk0ect");
})();
