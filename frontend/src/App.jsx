
import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

const initialForm = {
  age: 20,
  floors: 2,
  families: 2,
  building_size: "Medium",
  building_height: "Medium",
  construction_material: "Rc Engineered",
  building_usage: "Residential",
};

const materials = [
  "Adobe Mud",
  "Mud Mortar Stone",
  "Stone Flag",
  "Cement Mortar Stone",
  "Mud Mortar Brick",
  "Cement Mortar Brick",
  "Timber",
  "Bamboo",
  "Rc Non Engineered",
  "Rc Engineered",
  "Other",
];

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activePage, setActivePage] = useState("assessment");
  const [modelMetrics, setModelMetrics] = useState(null);
  const [metricsError, setMetricsError] = useState("");
  const [metricsLoading, setMetricsLoading] = useState(true);
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem("structuralguard-theme") || "light";
    } catch {
      return "light";
    }
  });

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem("structuralguard-theme", theme);
    } catch {
      // The theme still works if browser storage is unavailable.
    }
  }, [theme]);

  useEffect(() => {
    async function loadMetrics() {
      try {
        const response = await fetch(`${API_URL}/api/metrics`);
        if (!response.ok) {
          throw new Error("Unable to load model evaluation metrics.");
        }
        const data = await response.json();
        setModelMetrics(data);
        setMetricsError("");
      } catch (err) {
        setMetricsError(err.message);
      } finally {
        setMetricsLoading(false);
      }
    }
    loadMetrics();
  }, []);

  function update(key, value) {
    setForm((old) => ({ ...old, [key]: value }));
  }

  async function assessBuilding(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          age: Number(form.age),
          floors: Number(form.floors),
          families: Number(form.families),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Assessment failed.");
      }

      setResult(data);
      setActivePage("results");
    } catch (err) {
      setError(
        err.message.toLowerCase().includes("fetch")
          ? "Cannot connect to the prediction server. Make sure the backend is running."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  function startNewAssessment() {
    setResult(null);
    setError("");
    setActivePage("assessment");
  }

  function downloadReport() {
    if (!result) return;

    const lines = [
      "STRUCTURALGUARD AI",
      "Building Damage Assessment Report",
      "",
      `Generated: ${new Date().toLocaleString()}`,
      "",
      "BUILDING INFORMATION",
      `Building age: ${form.age} years`,
      `Number of floors: ${form.floors}`,
      `Number of families: ${form.families}`,
      `Building size: ${form.building_size}`,
      `Building height: ${form.building_height}`,
      `Construction material: ${form.construction_material}`,
      `Building usage: ${form.building_usage}`,
      "",
      "PREDICTION RESULTS",
      `Predicted damage: ${result.damage}`,
      `Infrastructure risk: ${result.risk}`,
      `Model confidence: ${Number(result.confidence).toFixed(2)}%`,
      "",
      "DAMAGE PROBABILITIES",
      ...["Low", "Medium", "High"].map(
        (level) =>
          `${level} damage: ${Number(
            result.probabilities?.[level] ?? 0
          ).toFixed(2)}%`
      ),
      "",
      "MODEL EVALUATION",
      `Test accuracy: ${
        accuracyPercentage == null
          ? "Unavailable"
          : `${Number(accuracyPercentage).toFixed(2)}%`
      }`,
      "",
      "IMPORTANT DISCLAIMER",
      "This result is a machine-learning prediction based on the supplied",
      "building characteristics. It is not a structural safety certificate.",
      "Consult a qualified structural engineer for an actual inspection.",
    ];

    const blob = new Blob(
      ["\uFEFF" + lines.join("\n")],
      { type: "text/plain;charset=utf-8" }
    );
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "StructuralGuard_Assessment_Report.txt";
    link.click();
    URL.revokeObjectURL(url);
  }

  const accuracyPercentage =
    modelMetrics?.accuracy_percentage ??
    (modelMetrics?.accuracy != null
      ? modelMetrics.accuracy * 100
      : null);

  const pageTitle =
    activePage === "assessment" ? "Building Assessment" : "Assessment Results";

  const damageClass = result?.damage?.toLowerCase() || "";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">S</div>
          <div>
            <strong>StructuralGuard</strong>
            <span>AI PLATFORM</span>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>

        <button
          type="button"
          className={`nav-item ${activePage === "assessment" ? "active" : ""}`}
          onClick={() => setActivePage("assessment")}
        >
          <span>▦</span> Building Assessment
        </button>

        <button
          type="button"
          className={`nav-item ${activePage === "results" ? "active" : ""}`}
          onClick={() => setActivePage("results")}
        >
          <span>◷</span> Assessment Results
        </button>

        <div className="sidebar-bottom">
          <div className="online-dot" />
          <div>
            <strong>Prediction Engine</strong>
            <span>Random Forest Model</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> {pageTitle}
          </div>

          <button
            type="button"
            className="theme-toggle"
            onClick={() =>
              setTheme((old) => (old === "light" ? "dark" : "light"))
            }
          >
            {theme === "light" ? "☾ Dark mode" : "☀ Light mode"}
          </button>
        </header>

        <section className="page-heading">
          <div>
            <div className="eyebrow">STRUCTURAL INTELLIGENCE</div>
            <h1>{pageTitle}</h1>
            <p>
              {activePage === "assessment"
                ? "Enter building characteristics to generate a machine-learning damage prediction."
                : "Review your building prediction, damage probabilities, and model performance."}
            </p>
          </div>
          <div className="heading-icon">⌂</div>
        </section>

        {activePage === "assessment" && (
          <section className="workspace-grid">
            <form
              className="panel assessment-panel"
              onSubmit={assessBuilding}
            >
              <div className="panel-heading">
                <div className="panel-icon">⌂</div>
                <div>
                  <h2>Building Information</h2>
                  <p>Enter the building details below.</p>
                </div>
              </div>

              <div className="form-grid">
                <label>
                  Building age
                  <div className="input-wrap">
                    <input
                      type="number"
                      min="0"
                      max="200"
                      value={form.age}
                      onChange={(e) => update("age", e.target.value)}
                      required
                    />
                    <span>years</span>
                  </div>
                </label>

                <label>
                  Number of floors
                  <input
                    type="number"
                    min="1"
                    max="20"
                    value={form.floors}
                    onChange={(e) => update("floors", e.target.value)}
                    required
                  />
                </label>

                <label>
                  Number of families
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={form.families}
                    onChange={(e) => update("families", e.target.value)}
                    required
                  />
                </label>

                <label>
                  Building size
                  <select
                    value={form.building_size}
                    onChange={(e) => update("building_size", e.target.value)}
                  >
                    {["Small", "Medium", "Large"].map((value) => (
                      <option key={value} value={value}>{value}</option>
                    ))}
                  </select>
                </label>

                <label>
                  Building height
                  <select
                    value={form.building_height}
                    onChange={(e) => update("building_height", e.target.value)}
                  >
                    {["Low", "Medium", "High"].map((value) => (
                      <option key={value} value={value}>{value}</option>
                    ))}
                  </select>
                </label>

                <label className="full-width">
                  Main construction material
                  <select
                    value={form.construction_material}
                    onChange={(e) =>
                      update("construction_material", e.target.value)
                    }
                  >
                    {materials.map((value) => (
                      <option key={value} value={value}>{value}</option>
                    ))}
                  </select>
                </label>

                <label className="full-width">
                  Building usage
                  <select
                    value={form.building_usage}
                    onChange={(e) => update("building_usage", e.target.value)}
                  >
                    <option value="Residential">Residential</option>
                    <option value="Other">Other</option>
                  </select>
                </label>
              </div>

              {error && <div className="error-message">{error}</div>}

              <button className="primary-button" disabled={loading}>
                {loading ? "Analyzing building..." : "Run assessment"}
                <span>→</span>
              </button>

              <p className="form-footnote">
                ✦ Powered by your trained Random Forest model
              </p>
            </form>

        
                
          </section>
        )}

        {activePage === "results" && (
          <>
            {!result ? (
              <section className="panel no-results-panel">
                <div className="panel-icon purple">◷</div>
                <h2>No assessment results yet</h2>
                <p>
                  Enter the building details and run an assessment first.
                  Your prediction and model analytics will appear here.
                </p>
                <button
                  type="button"
                  className="primary-button"
                  onClick={() => setActivePage("assessment")}
                >
                  Go to Building Assessment →
                </button>
              </section>
            ) : (
              <>
                <section className="panel results-page-panel">
                  <div className="panel-heading result-heading">
                    <div className="panel-icon purple">✳</div>
                    <div>
                      <h2>AI Assessment Results</h2>
                      <p>Prediction for the building details you submitted.</p>
                    </div>
                    <span className="result-tag">COMPLETE</span>
                  </div>

                  <div className="result-content">
                    <div className={`damage-banner ${damageClass}`}>
                      <div>
                        <span className="result-overline">
                          PREDICTED DAMAGE LEVEL
                        </span>
                        <h3>{result.damage} Damage</h3>
                      </div>
                      <div className="damage-symbol">
                        {result.damage_class === 1
                          ? "✓"
                          : result.damage_class === 2
                            ? "!"
                            : "↑"}
                      </div>
                    </div>

                    <div className="result-metrics">
                      <div className="metric-card">
                        <span>Infrastructure risk</span>
                        <strong
                          className={`risk-${result.risk.split(" ")[0].toLowerCase()}`}
                        >
                          {result.risk}
                        </strong>
                      </div>
                      <div className="metric-card">
                        <span>Model confidence</span>
                        <strong>
                          {Number(result.confidence).toFixed(1)}%
                        </strong>
                      </div>
                    </div>

                    <div className="probability-section">
                      <div className="probability-title">
                        <h3>Damage probability</h3>
                        <span>Model output</span>
                      </div>

                      {["Low", "Medium", "High"].map((level) => {
                        const probability = Number(
                          result.probabilities?.[level] ?? 0
                        );
                        return (
                          <div className="probability-item" key={level}>
                            <div className="probability-label">
                              <span>
                                <i className={`legend-dot ${level.toLowerCase()}`} />
                                {level} damage
                              </span>
                              <strong>{probability.toFixed(1)}%</strong>
                            </div>
                            <div className="progress-track">
                              <div
                                className={`progress-fill ${level.toLowerCase()}`}
                                style={{
                                  width: `${Math.max(0, Math.min(100, probability))}%`,
                                }}
                              />
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    <div className="result-actions">
                      <button
                        type="button"
                        className="secondary-button"
                        onClick={downloadReport}
                      >
                        Download assessment report
                      </button>
                      <button
                        type="button"
                        className="secondary-button"
                        onClick={startNewAssessment}
                      >
                        ↻ New assessment
                      </button>
                    </div>

                    <p className="report-note">
                      This prediction is a machine-learning estimate, not a
                      structural safety certificate. Consult a qualified
                      structural engineer for an actual inspection.
                    </p>
                  </div>
                </section>

                <section className="model-evaluation">
                  <div className="panel evaluation-panel">
                    <div className="panel-heading">
                      <div className="panel-icon">%</div>
                      <div>
                        <h2>Model Accuracy</h2>
                        <p>Performance on the held-out test dataset</p>
                      </div>
                    </div>

                    {metricsLoading ? (
                      <p className="metrics-caption">Loading model accuracy...</p>
                    ) : accuracyPercentage != null ? (
                      <>
                        <div className="accuracy-value">
                          {Number(accuracyPercentage).toFixed(2)}<span>%</span>
                        </div>
                        <p className="metrics-caption">
                          Evaluated on{" "}
                          {modelMetrics.test_samples?.toLocaleString() ?? "—"}{" "}
                          test samples
                        </p>
                      </>
                    ) : (
                      <p className="error-message">
                        {metricsError || "Model accuracy is unavailable."}
                      </p>
                    )}
                  </div>

                  <div className="panel evaluation-panel confusion-panel">
                    <div className="panel-heading">
                      <div className="panel-icon purple">▦</div>
                      <div>
                        <h2>Confusion Matrix</h2>
                        <p>Actual versus predicted damage grade</p>
                      </div>
                    </div>

                    {metricsLoading ? (
                      <p className="metrics-caption">Loading confusion matrix...</p>
                    ) : modelMetrics?.confusion_matrix && modelMetrics?.class_labels ? (
                      <div className="confusion-table-wrap">
                        <table className="confusion-table">
                          <thead>
                            <tr>
                              <th>Actual \ Predicted</th>
                              {modelMetrics.class_labels.map((label) => (
                                <th key={label}>Grade {label}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {modelMetrics.confusion_matrix.map((row, i) => (
                              <tr key={modelMetrics.class_labels[i]}>
                                <th>Grade {modelMetrics.class_labels[i]}</th>
                                {row.map((value, j) => (
                                  <td
                                    key={j}
                                    className={i === j ? "correct-cell" : ""}
                                  >
                                    {value.toLocaleString()}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                        <p className="metrics-caption">
                          Diagonal values are correct predictions; other values
                          are misclassifications.
                        </p>
                      </div>
                    ) : (
                      <p className="error-message">
                        {metricsError || "Confusion matrix is unavailable."}
                      </p>
                    )}
                  </div>
                </section>
              </>
            )}
          </>
        )}

        <footer className="app-footer">
          <span>STRUCTURALGUARD AI</span>
          <span>Machine Learning · Structural Damage Classification</span>
        </footer>
      </main>
    </div>
  );
}
