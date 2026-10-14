
import { useState } from "react";
import "./App.css";

const features = [
  { icon: "🛡️", title: "Pay Guard", desc: "Check if a payment is safe", color: "green", tag: "Stay protected" },
  { icon: "💬", title: "Message Explainer", desc: "Understand suspicious messages", color: "blue", tag: "Spot scams" },
  { icon: "🎯", title: "Scam Gym", desc: "Practice identifying scams", color: "orange", tag: "Learn safely" },
  { icon: "🤝", title: "Saathi Assistant", desc: "Get simple step-by-step help", color: "purple", tag: "Here to help" },
];

export default function App() {
  const [language, setLanguage] = useState("English");
  const [notice, setNotice] = useState("");

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#home">
          <span className="brand-icon">₹</span>
          <span>Pay<span className="brand-accent">Saathi</span><small>EASY PAY, SAFE PAY</small></span>
        </a>
        <div className="top-actions">
          <label className="language-picker">
            <span>Language</span>
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
              <option>English</option>
              <option>ಕನ್ನಡ</option>
              <option>हिन्दी</option>
            </select>
          </label>
          <div className="profile-avatar">S</div>
        </div>
      </header>

      <section className="welcome" id="home">
        <div className="welcome-copy">
          <span className="eyebrow"><span className="live-dot" /> YOUR TRUSTED PAYMENT COMPANION</span>
          <h1>Every payment.<br /><span>A little more peace of mind.</span></h1>
          <p>Take your time. Check before you pay. Saathi is here to help you stay safe from digital payment scams.</p>
          <button className="primary-button" onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}>
            Explore safety tools <span>→</span>
          </button>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="shield">✓</div>
          <div className="float-card float-card-top"><span>🛡️</span><div><b>Your safety first</b><small>Pause. Check. Proceed.</small></div></div>
          <div className="float-card float-card-bottom"><span>✓</span><div><b>Safer decisions</b><small>One step at a time</small></div></div>
        </div>
      </section>

      <section className="trust-strip">
        <div><span className="trust-icon">✓</span><span><b>Take your time</b><small>No rushed decisions</small></span></div>
        <div><span className="trust-icon">♡</span><span><b>Simple guidance</b><small>Made for everyone</small></span></div>
        <div><span className="trust-icon">⌁</span><span><b>Privacy matters</b><small>Stay alert to scams</small></span></div>
      </section>

      <section className="tools-section" id="features">
        <div className="section-heading">
          <div><span className="eyebrow">YOUR DIGITAL SAFETY KIT</span><h2>How can we help today?</h2><p>Choose a tool. We’ll guide you through it.</p></div>
          <span className="section-count">04 TOOLS</span>
        </div>
        <div className="feature-grid">
          {features.map((feature) => (
            <button className="feature-card" key={feature.title} onClick={() => setNotice(`${feature.title} selected. This feature will connect to the project workflow next.`)}>
              <div className={`feature-icon ${feature.color}`}>{feature.icon}</div>
              <span className="feature-tag">{feature.tag}</span>
              <h3>{feature.title}</h3>
              <p>{feature.desc}</p>
              <span className="card-arrow">Explore tool ↗</span>
            </button>
          ))}
        </div>
        {notice && <div className="notice" role="status">{notice}<button onClick={() => setNotice("")} aria-label="Dismiss">×</button></div>}
      </section>

      <section className="reminder">
        <div className="reminder-icon">💡</div>
        <div><span className="eyebrow">A LITTLE REMINDER</span><h3>Never share your UPI PIN or OTP.</h3><p>You never need to enter a PIN to receive money. If someone pressures you, pause and ask for help.</p></div>
      </section>

      <footer><a className="brand footer-brand" href="#home"><span className="brand-icon">₹</span><span>Pay<span className="brand-accent">Saathi</span></span></a><p>Built with care for safer digital payments.</p><span className="demo-label">DEMO EXPERIENCE · NO REAL PAYMENTS</span></footer>
    </main>
  );
}
