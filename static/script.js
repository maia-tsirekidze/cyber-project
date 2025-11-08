const URLinput = document.getElementById('URL');
const results = document.getElementById('results');
const forms = document.getElementById("forms");
//  
forms.addEventListener("submit", async event=>{
    event.preventDefault();
    let response = await fetch('/scan',{
        method: 'POST',
        body: new FormData(forms)

    })
    let result = await response.json();
    results.innerHTML = `
        <p><b>URL:</b> ${result.url}</p>
        <p><b>IP:</b> ${result.ip}</p>
        <p><b>Report time:</b> ${result.report_time}</p>
        <h3>HTTP Security Headers:</h3>
    `;
     
    const requiredHeaders = [
        'Content-Security-Policy',
        'Strict-Transport-Security',
        'X-Frame-Options',
        'X-Content-Type-Options',
        'Referrer-Policy'
    ]
    requiredHeaders.forEach(h => {
        if(result.headers[h]){
            results.innerHTML += `<p style="color:green">  ✅ -Present ${h}</p>`;
        }else{
            results.innerHTML += `<p style="color:red">  ❌  - Missing ${h} </p>`;
        }
    })
    if( result.warnings.length === 0){
      results.innerHTML +=`<p style="color:green">✅ All required headers are present</p>`;
    }
   
    URLinput.value='';

})
    

