# Cognitive Supply Network - Multi-Agent System

A multi-agent AI system for cognitive supply chain networks — powered by Google ADK / LiteLLM with a Next.js frontend.

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| **Node.js** | ≥ 18 | Frontend (Next.js) |
| **Python** | ≥ 3.12 | Backend (FastAPI + ADK agents) |
| **uv** | latest | Python package manager (used by backend scripts) |

Install `uv` if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Project Structure

```
smart_supply_chain_agent_1.0/
├── frontend/          # Next.js UI (contains package.json for all JS deps)
├── backend/           # FastAPI + Google ADK agents
│   ├── .env.example   # Copy this to .env and fill in your keys
│   ├── pyproject.toml # Python dependencies
│   └── src/
│       ├── agents/    # ADK LlmAgent definitions
│       └── tools/     # Business logic (demand, inventory, vendor, routing, alert)
├── scripts/           # Shell scripts called by npm run dev
│   ├── setup-agent.sh # Installs Python deps via uv sync
│   └── run-agent.sh   # Starts the FastAPI backend
└── notebooks/         # Prototype / reference notebooks
```

---

## Setup

### Step 1 — Configure environment variables

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in your credentials:

```env
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PROVIDER=google   # or openai
```

- **`GOOGLE_API_KEY`** — Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- **`OPENAI_API_KEY`** — Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **`PROVIDER`** — Set to `google` to use Gemini models, `openai` to use GPT models

---

### Step 2 — Install all dependencies (frontend + backend)

Everything is wired through `frontend/package.json`. A single install command sets up both the Node.js packages and the Python backend (via `postinstall` → `setup-agent.sh` → `uv sync`).

```bash
cd frontend

# using npm
npm install

# or using yarn
yarn install
```

> The `postinstall` script automatically runs `scripts/setup-agent.sh` which calls `uv sync` inside `backend/` to create the Python virtual environment and install all Python dependencies from `pyproject.toml`.

---

### Step 3 — Run the development server

From the `frontend/` directory:

```bash
# using npm
npm run dev

# or using yarn
yarn dev
```

This starts **both** services concurrently:

| Service | Command | URL |
|---------|---------|-----|
| Next.js UI | `next dev --turbopack` | http://localhost:3000 |
| FastAPI backend | `uv run -m main` | http://localhost:8000 |

---

## Available Scripts

Run these from the `frontend/` directory:

| Script | Description |
|--------|-------------|
| `npm run dev` | Start UI + backend together |
| `npm run dev:ui` | Start Next.js UI only |
| `npm run dev:agent` | Start FastAPI backend only |
| `npm run dev:debug` | Start both with `LOG_LEVEL=debug` |
| `npm run build` | Build Next.js for production |
| `npm run lint` | Run ESLint |

---

## AI Provider

The `PROVIDER` environment variable controls which LLM is used:

```env
PROVIDER=google   # Uses Gemini via GOOGLE_API_KEY
PROVIDER=openai   # Uses GPT via OPENAI_API_KEY
```

> **Note on free-tier quotas:** Google's free tier allows 20 requests/day per model. A full 5-agent supply chain run uses ~15–20 requests. For unrestricted usage, enable billing on your Google Cloud project.

---

> [!NOTE]
> Happy Learning!
