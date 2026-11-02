import React,{useState} from "react";
const fields=[
["age","Age (years)",48,0,120,1],["blood_pressure","Blood pressure (mmHg)",80,30,250,1],
["specific_gravity","Specific gravity",1.02,1,1.1,0.005],["albumin","Albumin (0–5)",0,0,5,1],
["sugar","Sugar (0–5)",0,0,5,1],["blood_glucose","Blood glucose (mg/dL)",110,30,600,1],
["blood_urea","Blood urea (mg/dL)",35,1,300,1],["serum_creatinine","Serum creatinine (mg/dL)",1.1,.1,30,.1],
["hemoglobin","Hemoglobin (g/dL)",14,1,25,.1],["packed_cell_volume","Packed cell volume (%)",44,1,80,1]];
export default function App(){
 const [values,setValues]=useState(Object.fromEntries(fields.map(([k,l,v])=>[k,v])));
 const [result,setResult]=useState(null),[error,setError]=useState(""),[loading,setLoading]=useState(false);
 async function submit(e){e.preventDefault();setError("");setResult(null);setLoading(true);
  try{const r=await fetch("http://127.0.0.1:5000/api/predict",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(values)});
   const d=await r.json();if(!r.ok)throw new Error(d.error||"Request failed");setResult(d);
  }catch(err){setError(err.message+". Check that the Flask backend is running.");}finally{setLoading(false);}}
 return <main className="page"><header><div className="brand">CKD<span>Care</span></div><small>STUDENT ML PROJECT</small></header>
 <section className="hero"><p className="eyebrow">MACHINE LEARNING DEMONSTRATION</p><h1>Chronic Kidney Disease<br/><em>Prediction System</em></h1><p className="sub">Enter sample patient measurements to demonstrate a machine-learning workflow.</p></section>
 <div className="notice"><b>Important:</b> This classroom demo uses synthetic data. It is not medically validated and must never be used for diagnosis or decisions about a real person.</div>
 <section className="panel"><div className="heading"><div><p className="eyebrow">PATIENT INPUT</p><h2>Medical parameters</h2></div><small>01 / INPUT</small></div>
 <form onSubmit={submit}><div className="fields">{fields.map(([key,label,initial,min,max,step])=><label key={key}>{label}<input type="number" required min={min} max={max} step={step} value={values[key]} onChange={e=>setValues({...values,[key]:e.target.value})}/></label>)}</div>
 <button disabled={loading}>{loading?"Processing...":"Run demo prediction"} <span>→</span></button></form>
 {error&&<p className="error">{error}</p>}
 {result&&<div className="result"><p className="eyebrow">DEMO RESULT</p><h2>{result.demo_prediction}</h2><p>Demo model confidence score: <b>{result.demo_score_percent}%</b></p><p className="small">{result.notice}</p><p className="small">MongoDB: {result.saved_to_mongodb?"Record saved":"Not configured / unavailable"}</p></div>}
 </section><footer>React · Flask · scikit-learn · MongoDB</footer></main>;
}
