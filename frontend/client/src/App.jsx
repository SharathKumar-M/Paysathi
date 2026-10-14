
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/v1/pay-guard/analyze";

const features = [
  { icon: "🛡️", title: "Pay Guard", desc: "Check if a payment is safe", color: "green", tag: "Stay protected" },
  { icon: "💬", title: "Message Explainer", desc: "Understand suspicious messages", color: "blue", tag: "Spot scams" },
  { icon: "🎯", title: "Scam Gym", desc: "Practice identifying scams", color: "orange", tag: "Learn safely" },
  { icon: "🤝", title: "Saathi Assistant", desc: "Get simple step-by-step help", color: "purple", tag: "Here to help" },
];

export default function App() {
  const [language, setLanguage] = useState("en");
  const [page, setPage] = useState("home");
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    payee_name: "",
    payee_id: "",
    amount: "",
    purpose_text: "",
    is_new_payee: true,
    on_phone_call: false,
  });

  function updateField(event) {
    const { name, value, type, checked } = event.target;
    setForm((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  async function analyzePayment(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    const payload = {
      language,
      payee_name: form.payee_name.trim(),
      payee_id: form.payee_id.trim(),
      amount: Number(form.amount),
      purpose_text: form.purpose_text.trim(),
      request_type: "pay",
      is_new_payee: form.is_new_payee,
      recipient_type: "person",
      on_phone_call: form.on_phone_call,
    };

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const detail =
          typeof data.detail === "string"
            ? data.detail
            : `The server returned error ${response.status}.`;
        throw new Error(detail);
      }

      setResult(data);
      setPage("result");
    } catch (err) {
      setError(
        err instanceof TypeError
          ? "Cannot connect to PaySaathi backend. Check that the backend server is running on port 8000."
          : err.message || "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function openTool(title) {
    if (title === "Pay Guard") {
      setError("");
      setResult(null);
      setPage("payguard");
    } else {
      setNotice(`${title} is next on our frontend development list.`);
    }
  }

  function renderHeader() {
    return (
      <header className="topbar">
        <button className="brand brand-button" onClick={() => setPage("home")}>
          <span className="brand-icon">₹</span>
          <span>
            Pay<span className="brand-accent">Saathi</span>
            <small>EASY PAY, SAFE PAY</small>
          </span>
        </button>

        <div className="top-actions">
          <label className="language-picker">
            <span>Language</span>
            <select
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
            >
              <option value="en">English</option>
              <option value="kn">ಕನ್ನಡ</option>
              <option value="hi">हिन्दी</option>
            </select>
          </label>
          <div className="profile-avatar">S</div>
        </div>
      </header>
    );
  }

  function renderHome() {
    return (
      <>
        <section className="welcome" id="home">
          <div className="welcome-copy">
            <span className="eyebrow">
              <span className="live-dot" /> YOUR TRUSTED PAYMENT COMPANION
            </span>
            <h1>
              Every payment.
              <br />
              <span>A little more peace of mind.</span>
            </h1>
            <p>
              Take your time. Check before you pay. Saathi is here to help you
              stay safe from digital payment scams.
            </p>
            <button
              className="primary-button"
              onClick={() =>
                document.getElementById("features")?.scrollIntoView({
                  behavior: "smooth",
                })
              }
            >
              Explore safety tools <span>→</span>
            </button>
          </div>

          <div className="hero-art" aria-hidden="true">
            <div className="orbit orbit-one" />
            <div className="orbit orbit-two" />
            <div className="shield">✓</div>
            <div className="float-card float-card-top">
              <span>🛡️</span>
              <div>
                <b>Your safety first</b>
                <small>Pause. Check. Proceed.</small>
              </div>
            </div>
            <div className="float-card float-card-bottom">
              <span>✓</span>
              <div>
                <b>Safer decisions</b>
                <small>One step at a time</small>
              </div>
            </div>
          </div>
        </section>

        <section className="trust-strip">
          <div>
            <span className="trust-icon">✓</span>
            <span><b>Take your time</b><small>No rushed decisions</small></span>
          </div>
          <div>
            <span className="trust-icon">♡</span>
            <span><b>Simple guidance</b><small>Made for everyone</small></span>
          </div>
          <div>
            <span className="trust-icon">⌁</span>
            <span><b>Privacy matters</b><small>Stay alert to scams</small></span>
          </div>
        </section>

        <section className="tools-section" id="features">
          <div className="section-heading">
            <div>
              <span className="eyebrow">YOUR DIGITAL SAFETY KIT</span>
              <h2>How can we help today?</h2>
              <p>Choose a tool. We’ll guide you through it.</p>
            </div>
            <span className="section-count">04 TOOLS</span>
          </div>

          <div className="feature-grid">
            {features.map((feature) => (
              <button
                className="feature-card"
                key={feature.title}
                onClick={() => openTool(feature.title)}
              >
                <div className={`feature-icon ${feature.color}`}>
                  {feature.icon}
                </div>
                <span className="feature-tag">{feature.tag}</span>
                <h3>{feature.title}</h3>
                <p>{feature.desc}</p>
                <span className="card-arrow">Explore tool ↗</span>
              </button>
            ))}
          </div>

          {notice && (
            <div className="notice" role="status">
              {notice}
              <button onClick={() => setNotice("")} aria-label="Dismiss">
                ×
              </button>
            </div>
          )}
        </section>

        <section className="reminder">
          <div className="reminder-icon">💡</div>
          <div>
            <span className="eyebrow">A LITTLE REMINDER</span>
            <h3>Never share your UPI PIN or OTP.</h3>
            <p>
              You never need to enter a PIN to receive money. If someone
              pressures you, pause and ask for help.
            </p>
          </div>
        </section>
      </>
    );
  }

  function renderPayGuard() {
    return (
      <section className="workflow-section">
        <button className="back-button" onClick={() => setPage("home")}>
          ← Back to dashboard
        </button>

        <div className="workflow-heading">
          <div className="feature-icon green workflow-icon">🛡️</div>
          <span className="eyebrow">PAYMENT SAFETY CHECK</span>
          <h1>Let's check this payment.</h1>
          <p>
            Answer a few simple questions. PaySaathi will check for warning
            signs before you proceed.
          </p>
          <div className="simulation-note">
            <span>ⓘ</span>
            This is a safety assessment, not a real payment. Never enter your
            UPI PIN or OTP here.
          </div>
        </div>

        <form className="guard-form" onSubmit={analyzePayment}>
          <div className="form-section-title">
            <span>01</span>
            <div>
              <h2>Payment details</h2>
              <p>Tell us who you are paying and why.</p>
            </div>
          </div>

          <div className="form-grid">
            <label className="field">
              <span>Receiver's name *</span>
              <input
                name="payee_name"
                value={form.payee_name}
                onChange={updateField}
                placeholder="e.g. Ravi Kumar"
                required
                maxLength={100}
              />
            </label>

            <label className="field">
              <span>UPI ID or receiver reference</span>
              <input
                name="payee_id"
                value={form.payee_id}
                onChange={updateField}
                placeholder="e.g. name@upi"
                maxLength={150}
              />
              <small>Do not enter account passwords or PINs.</small>
            </label>

            <label className="field">
              <span>Amount (₹) *</span>
              <input
                name="amount"
                type="number"
                value={form.amount}
                onChange={updateField}
                placeholder="Enter amount"
                min="1"
                max="100000000"
                step="0.01"
                required
              />
            </label>

            <label className="field field-full">
              <span>Why are you making this payment? *</span>
              <textarea
                name="purpose_text"
                value={form.purpose_text}
                onChange={updateField}
                placeholder="Example: Someone called asking me to pay a fee to keep my account active..."
                rows={4}
                maxLength={2000}
                required
              />
              <small>
                Mention any urgent demands or suspicious instructions.
              </small>
            </label>
          </div>

          <div className="form-divider" />

          <div className="form-section-title">
            <span>02</span>
            <div>
              <h2>Have you noticed any pressure?</h2>
              <p>These details can help identify warning signs.</p>
            </div>
          </div>

          <label className="check-option">
            <input
              type="checkbox"
              name="is_new_payee"
              checked={form.is_new_payee}
              onChange={updateField}
            />
            <span>
              <b>This is a new or unfamiliar receiver.</b>
              <small>I have not paid this person before.</small>
            </span>
          </label>

          <label className="check-option">
            <input
              type="checkbox"
              name="on_phone_call"
              checked={form.on_phone_call}
              onChange={updateField}
            />
            <span>
              <b>Someone is on a call with me about this payment.</b>
              <small>They may be guiding or pressuring me to pay.</small>
            </span>
          </label>

          {error && (
            <div className="error-message" role="alert">
              <b>Unable to check this payment</b>
              <p>{error}</p>
            </div>
          )}

          <button className="primary-button submit-button" type="submit" disabled={loading}>
            {loading ? "Checking warning signs..." : "Check payment safety"}
            {!loading && <span>→</span>}
          </button>
          <p className="form-footnote">
            PaySaathi does not send money, contact your bank, or block
            payments.
          </p>
        </form>
      </section>
    );
  }

  function renderResult() {
    const verdict = String(
      result?.verdict ?? result?.risk_verdict ?? ""
    ).toUpperCase();

    const validVerdicts = ["GREEN", "AMBER", "RED"];
    const hasVerdict = validVerdicts.includes(verdict);

    const verdictInfo = {
      GREEN: {
        title: "No known warning signs matched",
        description:
          "The current checks did not identify a known warning pattern. This does not prove the receiver is safe.",
        icon: "✓",
      },
      AMBER: {
        title: "Pause and double-check",
        description:
          "Some warning signs may need closer attention. Verify the request independently before deciding.",
        icon: "!",
      },
      RED: {
        title: "Stop and review the warning signs",
        description:
          "The assessment identified serious warning signs. Do not rush or follow instructions from someone pressuring you.",
        icon: "!",
      },
    };

    const info = verdictInfo[verdict];
    const warnings = Array.isArray(result?.warnings)
      ? result.warnings
      : Array.isArray(result?.reasons)
        ? result.reasons
        : [];

    return (
      <section className="workflow-section">
        <button className="back-button" onClick={() => setPage("payguard")}>
          ← Back to payment details
        </button>

        <div className="result-panel">
          {hasVerdict ? (
            <>
              <div className={`result-symbol result-${verdict.toLowerCase()}`}>
                {info.icon}
              </div>
              <span className="eyebrow">PAY GUARD ASSESSMENT</span>
              <h1>{info.title}</h1>
              <span className={`verdict-pill verdict-${verdict.toLowerCase()}`}>
                {verdict} RISK CHECK
              </span>
              <p className="result-description">{info.description}</p>

              {warnings.length > 0 && (
                <div className="warning-list">
                  <h2>Warning signs to review</h2>
                  {warnings.map((item, index) => (
                    <article className="warning-item" key={item.code ?? index}>
                      <span>!</span>
                      <div>
                        <b>{item.title ?? item.code ?? `Warning ${index + 1}`}</b>
                        {item.detail && <p>{item.detail}</p>}
                      </div>
                    </article>
                  ))}
                </div>
              )}

              <div className="result-safety-note">
                <b>Remember</b>
                <p>
                  Never share your UPI PIN or OTP. If you feel pressured,
                  pause and independently verify the request.
                </p>
              </div>
            </>
          ) : (
            <>
              <div className="result-symbol result-amber">i</div>
              <span className="eyebrow">PAY GUARD RESPONSE</span>
              <h1>We received a response.</h1>
              <p className="result-description">
                The API response did not contain a recognised GREEN, AMBER,
                or RED verdict field. No risk level has been invented.
              </p>
              <details className="response-details">
                <summary>Inspect the API response</summary>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </details>
            </>
          )}

          <div className="result-actions">
            <button className="primary-button" onClick={() => setPage("payguard")}>
              Check another payment
            </button>
            <button className="secondary-button" onClick={() => setPage("home")}>
              Back to dashboard
            </button>
          </div>
          <p className="form-footnote">
            Simulation only. A risk result is guidance, not a guarantee of
            safety or proof of fraud.
          </p>
        </div>
      </section>
    );
  }

  return (
    <main className="app-shell">
      {renderHeader()}

      {page === "home" && renderHome()}
      {page === "payguard" && renderPayGuard()}
      {page === "result" && renderResult()}

      <footer>
        <button className="brand brand-button footer-brand" onClick={() => setPage("home")}>
          <span className="brand-icon">₹</span>
          <span>Pay<span className="brand-accent">Saathi</span></span>
        </button>
        <p>Built with care for safer digital payments.</p>
        <span className="demo-label">DEMO EXPERIENCE · NO REAL PAYMENTS</span>
      </footer>
    </main>
  );
}
