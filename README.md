# Communication

A lightweight **data visualization library** for building clear, expressive charts and graphs.

> Communication is about turning raw data into visuals that people actually understand. This library aims to make that fast, consistent, and pleasant to work with.

---

## ✨ Features

- 📊 **Core chart types** — bar, line, scatter, area, and pie charts
- 🎨 **Theming** — consistent color palettes that work in light and dark modes
- ⚡ **Lightweight** — minimal dependencies and a small footprint
- 🧩 **Composable API** — build complex visualizations from simple building blocks
- ♿ **Accessible** — sensible defaults for color contrast and labels

> **Note:** This project is in early development. The feature list above describes the intended direction — check the [Roadmap](#-roadmap) for current status.

---

## 🚀 Getting Started

### Installation

```bash
# Once published, install via your package manager
npm install communication
```

### Quick Example

```js
import { Chart } from "communication";

const chart = new Chart("#container", {
  type: "bar",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr"],
    values: [40, 55, 30, 70],
  },
});

chart.render();
```

---

## 📖 Usage

Each chart is created by passing a container selector and a configuration object:

| Option   | Type     | Description                                  |
| -------- | -------- | -------------------------------------------- |
| `type`   | `string` | Chart type (`bar`, `line`, `scatter`, ...)   |
| `data`   | `object` | The dataset to visualize                     |
| `theme`  | `string` | Optional theme name (`light` / `dark`)       |
| `width`  | `number` | Chart width in pixels                        |
| `height` | `number` | Chart height in pixels                       |

---

## 🗺 Roadmap

- [ ] Core rendering engine
- [ ] Bar and line charts
- [ ] Scatter and area charts
- [ ] Theming and color palettes
- [ ] Interactivity (tooltips, zoom, hover)
- [ ] Documentation site with live examples

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Open a pull request

---

## 📄 License

This project is released under the [MIT License](LICENSE).
