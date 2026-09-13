/* EmlaLock Lovelace card
 * Automatically discovers EmlaLock entities and action buttons.
 * Add as a Lovelace resource and use: type: custom:emlalock-card
 */

class EmlaLockCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._hass = null;
    this._root = document.createElement("div");
    this.shadowRoot.appendChild(this._root);
  }

  setConfig(config) {
    this._config = config || {};
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    return 12;
  }

  _findEntity(...suffixes) {
    if (!this._hass?.states) return null;
    const states = Object.values(this._hass.states);
    const wanted = suffixes.map((value) => value.toLowerCase());
    return states.find((item) => {
      const id = item.entity_id.toLowerCase();
      const name = String(item.attributes?.friendly_name || "").toLowerCase();
      if (!id.includes("emlalock") && !name.includes("emlalock")) return false;
      return wanted.some((suffix) =>
        id.endsWith(`_${suffix}`) || name === `emlalock ${suffix.replaceAll("_", " ")}`
      );
    }) || null;
  }

  _button(...suffixes) {
    return this._findEntity(...suffixes);
  }

  _value(entity, fallback = "—") {
    if (!entity || entity.state === "unknown" || entity.state === "unavailable") return fallback;
    return entity.state;
  }

  _isAvailable(entity) {
    return Boolean(entity && entity.state !== "unavailable" && entity.state !== "unknown");
  }

  _buttonHtml(entity, label, key) {
    const disabled = !this._isAvailable(entity);
    return `<button class="action" data-button="${key}" ${disabled ? "disabled" : ""}>${label}</button>`;
  }

  _render() {
    if (!this._hass) return;

    const session = this._findEntity("session");
    const active = this._findEntity("session_active", "active");
    const start = this._findEntity("start_date", "start");
    const passed = this._findEntity("time_in_lock", "time_passed", "passed");
    const end = this._findEntity("end_date", "end");
    const remaining = this._findEntity("time_remaining", "remaining");
    const maximum = this._findEntity("maximum", "maximum_duration");
    const minimum = this._findEntity("minimum", "minimum_duration");
    const requirements = this._findEntity("requirement_links", "requirements");

    const addHour = this._button("add_1_hour");
    const subtractHour = this._button("subtract_1_hour", "remove_1_hour");
    const addDay = this._button("add_1_day");
    const subtractDay = this._button("subtract_1_day", "remove_1_day");

    const activeValue = this._value(active, "Off");
    const isActive = ["on", "true", "active", "yes"].includes(String(activeValue).toLowerCase());

    this._root.innerHTML = `
      <style>
        :host { display: block; }
        ha-card { overflow: hidden; border-radius: 24px; background: #1b1d1e; color: #f4f5f7; border: 1px solid #34383b; box-shadow: none; }
        .card { padding: 18px 16px 20px; font-family: var(--paper-font-body1_-_font-family, Arial, sans-serif); }
        .header { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 2px 4px 18px; }
        .identity { display: flex; align-items: center; gap: 12px; min-width: 0; }
        .lock { color: #08a9df; font-size: 30px; line-height: 1; }
        .title { font-size: 25px; font-weight: 700; letter-spacing: .2px; }
        .subtitle { color: #aeb3b8; font-size: 15px; margin-top: 3px; }
        .status { display: flex; align-items: center; gap: 8px; border-radius: 24px; padding: 12px 15px; font-size: 14px; font-weight: 700; white-space: nowrap; }
        .status.on { color: #08b8f0; background: #103b4b; }
        .status.off { color: #aeb3b8; background: #303336; }
        .dot { width: 10px; height: 10px; border-radius: 50%; background: currentColor; }
        .sensors { display: flex; flex-direction: column; gap: 9px; }
        .row { display: flex; align-items: center; min-height: 65px; border-radius: 17px; background: #242729; padding: 10px 12px; box-sizing: border-box; }
        .row-icon { width: 40px; flex: 0 0 40px; color: #d8dde5; font-size: 24px; text-align: center; }
        .row-content { min-width: 0; flex: 1; padding-left: 8px; }
        .label { color: #aeb7c5; font-size: 13px; font-weight: 700; letter-spacing: .6px; text-transform: uppercase; }
        .value { color: #f4f5f7; font-size: 18px; font-weight: 600; margin-top: 4px; overflow-wrap: anywhere; }
        .chevron { color: #cdd4df; font-size: 31px; line-height: 1; padding-left: 8px; }
        .divider { height: 1px; background: #383c3f; margin: 18px 0 16px; }
        .section-title { color: #aeb7c5; font-size: 14px; font-weight: 700; letter-spacing: .7px; margin: 0 0 13px; }
        .actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .action { border: 0; border-radius: 16px; min-height: 58px; padding: 10px 8px; background: #08a9df; color: white; font: inherit; font-size: 16px; font-weight: 700; cursor: pointer; transition: filter .15s ease, opacity .15s ease; }
        .action:hover:not(:disabled) { filter: brightness(1.08); }
        .action:active:not(:disabled) { filter: brightness(.92); }
        .action:disabled { background: #4b5053; color: #9da3a8; opacity: .7; cursor: not-allowed; }
        @media (max-width: 430px) {
          .header { align-items: flex-start; }
          .status { padding: 10px 11px; font-size: 12px; }
          .title { font-size: 22px; }
          .row { min-height: 61px; }
          .value { font-size: 16px; }
          .action { font-size: 14px; }
        }
      </style>
      <ha-card>
        <div class="card">
          <div class="header">
            <div class="identity">
              <div class="lock">🔒</div>
              <div>
                <div class="title">EmlaLock</div>
                <div class="subtitle">${this._escape(this._value(session))}</div>
              </div>
            </div>
            <div class="status ${isActive ? "on" : "off"}">
              <span class="dot"></span> Session ${isActive ? "active" : "inactive"}
            </div>
          </div>

          <div class="sensors">
            ${this._row("👤", "Session", this._value(session))}
            ${this._row("●", "Session active", this._value(active, "Off"))}
            ${this._row("▣", "Start date", this._value(start))}
            ${this._row("⏱", "Time passed", this._value(passed))}
            ${this._row("▣", "End date", this._value(end))}
            ${this._row("⌛", "Time remaining", this._value(remaining))}
            ${this._row("⏱", "Maximum duration", this._value(maximum))}
            ${this._row("⏱", "Minimum duration", this._value(minimum))}
            ${this._row("🔗", "Requirement links", this._value(requirements))}
          </div>

          <div class="divider"></div>
          <div class="section-title">CHANGE DURATION</div>
          <div class="actions">
            ${this._buttonHtml(addHour, "Add 1 hour", "add-hour")}
            ${this._buttonHtml(subtractHour, "Subtract 1 hour", "subtract-hour")}
            ${this._buttonHtml(addDay, "Add 1 day", "add-day")}
            ${this._buttonHtml(subtractDay, "Subtract 1 day", "subtract-day")}
          </div>
        </div>
      </ha-card>
    `;

    this._root.querySelectorAll("button[data-button]").forEach((button) => {
      button.addEventListener("click", () => {
        const entities = {
          "add-hour": addHour,
          "subtract-hour": subtractHour,
          "add-day": addDay,
          "subtract-day": subtractDay,
        };
        const target = entities[button.dataset.button];
        if (target && this._hass) {
          this._hass.callService("button", "press", { entity_id: target.entity_id });
        }
      });
    });
  }

  _row(icon, label, value) {
    return `<div class="row"><div class="row-icon">${icon}</div><div class="row-content"><div class="label">${label}</div><div class="value">${this._escape(value)}</div></div><div class="chevron">›</div></div>`;
  }

  _escape(value) {
    return String(value ?? "—")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
}

customElements.define("emlalock-card", EmlaLockCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "emlalock-card",
  name: "EmlaLock Card",
  description: "A dashboard card for EmlaLock with automatic entity discovery and holder-key-aware buttons.",
  preview: true,
});
