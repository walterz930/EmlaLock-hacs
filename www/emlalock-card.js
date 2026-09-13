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

  _icon(symbol) {
    return `<span class="icon">${symbol}</span>`;
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
