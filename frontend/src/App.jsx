// src/App.jsx
import React, { useMemo, useState, useEffect } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Navigate,
  useNavigate,
} from "react-router-dom";

/* ===========================
   LOGO CORPORATIVO
   =========================== */
function LogoLuxChile({ size = 42 }) {
  return (
    <div className="flex items-center gap-2 select-none">
      <svg width={size} height={size} viewBox="0 0 64 64" className="drop-shadow-sm">
        <defs>
          <linearGradient id="luxgrad" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0%" stopColor="#0ea5e9" />
            <stop offset="100%" stopColor="#22c55e" />
          </linearGradient>
        </defs>
        <rect rx="14" width="64" height="64" fill="url(#luxgrad)"></rect>
        <path
          d="M18 40 L28 22 L36 34 L46 24"
          stroke="white"
          strokeWidth="4"
          fill="none"
          strokeLinejoin="round"
        />
        <circle cx="46" cy="24" r="3" fill="white" />
      </svg>
      <div className="leading-tight">
        <div className="font-semibold text-slate-800">LuxChile</div>
        <div className="text-xs text-slate-500">Logística & Rutas</div>
      </div>
    </div>
  );
}

/* ===========================
   CONFIG & HELPERS
   =========================== */
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function api(path, { method = "GET", body } = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`HTTP ${res.status}: ${txt}`);
  }
  const isJson =
    res.headers.get("content-type")?.includes("application/json") ?? false;
  return isJson ? res.json() : res.text();
}

function formatCLP(v) {
  const n = Number(v || 0);
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(n);
}

function useLeafletCssOnce() {
  useMemo(() => {
    if (!document.querySelector('link[data-leaflet]')) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      link.setAttribute("data-leaflet", "1");
      document.head.appendChild(link);
    }
  }, []);
}

/* ===========================
   LAYOUT PRINCIPAL
   =========================== */
function Shell({ user, onLogout, children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-20 bg-white border-b shadow-sm">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center gap-4">
          <LogoLuxChile size={34} />
          <nav className="ml-auto flex items-center gap-3 text-sm">
            <Link className="hover:underline" to="/home">Inicio</Link>
            <Link className="hover:underline" to="/stock">Stock</Link>
            <Link className="hover:underline" to="/rutas">Rutas</Link>
            <Link className="hover:underline" to="/incidentes">Incidentes</Link>
            <Link className="hover:underline" to="/asignaciones">Asignar carga</Link>
            <span className="ml-4 text-slate-500">{user}</span>
            <button
              className="ml-2 rounded-xl border px-3 py-1 text-sm hover:bg-slate-100"
              onClick={onLogout}
            >
              Salir
            </button>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">{children}</main>

      <footer className="border-t py-4 text-center text-xs text-slate-500">
        MVP académico • FastAPI + React
      </footer>
    </div>
  );
}

/* ===========================
   LOGIN
   =========================== */
import trucksUrl from "./assets/trucks.jpg";

function Login({ onLogin }) {
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (!user.trim() || !pass.trim()) {
      setError("Completa usuario y contraseña.");
      return;
    }
    setLoading(true);
    setTimeout(() => {
      onLogin(user.trim());
      navigate("/home");
    }, 400);
  }

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Form */}
      <div className="flex w-full md:w-1/2 items-center justify-center p-8 md:p-12">
        <div className="w-full max-w-sm">
          <div className="mb-8">
            <LogoLuxChile size={42} />
          </div>

          <h2 className="text-2xl font-semibold text-slate-900 mb-1">Bienvenido</h2>
          <p className="text-slate-600 mb-8">
            Ingresa tu usuario y contraseña para continuar.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-slate-600 mb-1">Usuario</label>
              <input
                className="w-full rounded-xl border px-3 py-2"
                value={user}
                onChange={(e) => setUser(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm text-slate-600 mb-1">Contraseña</label>
              <input
                type="password"
                className="w-full rounded-xl border px-3 py-2"
                value={pass}
                onChange={(e) => setPass(e.target.value)}
              />
            </div>
            {error && <p className="text-sm text-rose-600">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-sky-600 py-2 text-white hover:bg-sky-700 disabled:opacity-50"
            >
              {loading ? "Ingresando…" : "Ingresar"}
            </button>
          </form>
        </div>
      </div>

      {/* Imagen */}
      <div className="relative hidden md:block w-1/2 overflow-hidden">
        <img
          src={trucksUrl}
          alt="Camiones"
          className="absolute inset-0 h-full w-full object-cover grayscale opacity-70"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-black/40 to-black/20" />
        <div className="relative z-10 h-full w-full flex items-center justify-center">
          <h3 className="text-white/90 text-4xl font-semibold drop-shadow">LuxChile Panel</h3>
        </div>
      </div>
    </div>
  );
}

/* ===========================
   HOME
   =========================== */
function StatCard({ label, value, sublabel }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-slate-900">{value}</p>
      {sublabel && <p className="mt-1 text-xs text-slate-500">{sublabel}</p>}
    </div>
  );
}

function TrendSparkline({ points = [5, 8, 6, 12, 10, 14, 18] }) {
  const w = 160, h = 48, max = Math.max(...points), min = Math.min(...points);
  const path = points
    .map((y, i) => {
      const px = (i / (points.length - 1)) * (w - 8) + 4;
      const py = h - ((y - min) / (max - min || 1)) * (h - 8) - 4;
      return `${i === 0 ? "M" : "L"} ${px.toFixed(1)} ${py.toFixed(1)}`;
    })
    .join(" ");
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      <path d={path} fill="none" stroke="#0f172a" strokeOpacity="0.5" strokeWidth="2" />
      {points.map((y, i) => {
        const px = (i / (points.length - 1)) * (w - 8) + 4;
        const py = h - ((y - min) / (max - min || 1)) * (h - 8) - 4;
        return <circle key={i} cx={px} cy={py} r="2" fill="#0f172a" fillOpacity="0.55" />;
      })}
    </svg>
  );
}

function HomePage({ user = "" }) {
  // KPIs demo
  const [kpi, setKpi] = React.useState({
    ordersInTransit: 128,
    weeklyIncidents: 3,
    avgDurationMin: 54,
    slaOK: "98.6%",
  });
  const [trend, setTrend] = React.useState([7, 8, 5, 11, 9, 12, 15]);
  const [recentInc, setRecentInc] = React.useState([]);
  const [recentRoutes, setRecentRoutes] = React.useState([]);
  const navigate = useNavigate();

  async function fetchRecentIncidents() {
    try {
      const data = await api("/incidentes?limit=3");
      setRecentInc(Array.isArray(data) ? data : []);
    } catch (_) {
      setRecentInc([]);
    }
  }

  async function fetchRecentRoutes() {
    try {
      const data = await api("/routes/recent?limit=3");
      setRecentRoutes(Array.isArray(data) ? data : []);
    } catch (_) {
      setRecentRoutes([]);
    }
  }

  React.useEffect(() => {
    fetchRecentIncidents();
    fetchRecentRoutes();
  }, []);

  function refresh() {
    setKpi((k) => ({
      ...k,
      ordersInTransit: k.ordersInTransit + Math.round((Math.random() - 0.5) * 6),
      weeklyIncidents: Math.max(0, k.weeklyIncidents + Math.round((Math.random() - 0.5) * 2)),
      avgDurationMin: Math.max(20, k.avgDurationMin + Math.round((Math.random() - 0.5) * 6)),
      slaOK: `${(97 + Math.random() * 3).toFixed(1)}%`,
    }));
    setTrend((t) => {
      const nxt = [
        ...t.slice(1),
        Math.max(3, Math.min(18, (t.at(-1) || 10) + Math.round((Math.random() - 0.5) * 4))),
      ];
      return nxt;
    });
    // refrescamos actividad reciente también
    fetchRecentIncidents();
    fetchRecentRoutes();
  }

  return (
    <section>
      {/* Header con imagen tenue */}
      <div className="relative overflow-hidden rounded-2xl border border-slate-200">
        <img
          src={trucksUrl}
          alt="Camiones"
          className="absolute inset-0 h-full w-full object-cover grayscale opacity-30"
        />
        <div className="relative z-10 flex flex-col md:flex-row md:items-end justify-between p-6 md:p-8 bg-gradient-to-br from-white/70 to-white/40">
          <div>
            <h2 className="text-2xl font-semibold text-slate-900">Menú principal</h2>
            <p className="text-slate-600">
              {user ? `Hola, ${user}.` : "Bienvenido."} ¿Qué quieres hacer hoy?
            </p>
          </div>
          <button
            onClick={refresh}
            className="mt-4 md:mt-0 rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-slate-800 hover:bg-slate-50"
          >
            Actualizar métricas
          </button>
        </div>
      </div>

      {/* KPIs */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard label="Órdenes en tránsito" value={kpi.ordersInTransit} sublabel="flota activa" />
        <StatCard label="Incidentes (semana)" value={kpi.weeklyIncidents} sublabel="reportados" />
        <StatCard label="Duración promedio" value={`${kpi.avgDurationMin} min`} sublabel="rutas completadas" />
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-xs uppercase tracking-wide text-slate-500">Cumplimiento SLA</p>
          <div className="mt-1 flex items-end justify-between">
            <p className="text-2xl font-semibold text-slate-900">{kpi.slaOK}</p>
            <TrendSparkline points={trend} />
          </div>
          <p className="mt-1 text-xs text-slate-500">últimos 7 días</p>
        </div>
      </div>

      {/* Atajos / acciones principales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-4">
        {[
          { title: "Consultar stock", desc: "Disponibilidad por SKU en todas las bodegas.", to: "/stock" },
          { title: "Optimizar rutas", desc: "Distancia, duración y riesgo de trayectos.", to: "/rutas" },
          { title: "Registrar incidente", desc: "Desvíos, accidentes o detenciones.", to: "/incidentes" },
          { title: "Asignar carga", desc: "Responsable, vehículo y destinos.", to: "/asignaciones" },
        ].map((item) => (
          <Link
            key={item.title}
            to={item.to}
            className="rounded-2xl border p-4 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all bg-slate-50"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-slate-900">{item.title}</h3>
                <p className="text-sm text-slate-500 mt-1">{item.desc}</p>
              </div>
              <div className="text-sky-600 text-lg font-semibold">→</div>
            </div>
          </Link>
        ))}
      </div>

      {/* Datos críticos (RESTABLECIDO) */}
      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Incidentes recientes */}
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm cursor-pointer hover:shadow-md"
             onClick={() => navigate('/incidentes/historial')}>
          <div className="flex items-center justify-between">
            <h4 className="font-medium text-slate-900">Incidentes recientes</h4>
            <button onClick={(e)=>{e.stopPropagation(); navigate('/incidentes/historial')}} className="text-xs text-sky-600 hover:underline">Ver todo</button>
          </div>
          <ul className="mt-3 divide-y divide-slate-100">
            {recentInc.map((i) => {
              const when = i.created_at
                ? new Date(i.created_at)
                : null;
              const whenStr = when
                ? when.toLocaleString()
                : "";
              return (
                <li key={i.id} className="py-2 text-sm">
                  <div className="flex items-center justify-between">
                    <p className="text-slate-800">
                      <span className="font-medium">{i.type}</span> • {i.cargo_id} • {i.employee_id}
                    </p>
                    <p className="text-slate-500">{whenStr}</p>
                  </div>
                </li>
              );
            })}
            {recentInc.length === 0 && (
              <li className="py-2 text-sm text-slate-500">Sin datos recientes.</li>
            )}
          </ul>
        </div>

        {/* Rutas recientes */}
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm cursor-pointer hover:shadow-md"
             onClick={() => navigate('/rutas/historial')}>
          <div className="flex items-center justify-between">
            <h4 className="font-medium text-slate-900">Rutas recientes</h4>
            <button onClick={(e)=>{e.stopPropagation(); navigate('/rutas/historial')}} className="text-xs text-sky-600 hover:underline">Ver todo</button>
          </div>
          <table className="mt-3 w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500">
                <th className="py-2">Origen</th>
                <th>Destino</th>
                <th>Dist.</th>
                <th>Duración</th>
                <th>Riesgo</th>
              </tr>
            </thead>
            <tbody>
              {recentRoutes.map((r) => {
                const risk = r.risk_score <= 0.33 ? "Bajo" : r.risk_score <= 0.66 ? "Medio" : "Alto";
                return (
                  <tr key={r.id} className="border-t text-slate-800">
                    <td className="py-2">{r.origin_text || `${r.origin_lat?.toFixed?.(2)}, ${r.origin_lon?.toFixed?.(2)}`}</td>
                    <td>{r.destination_text || `${r.destination_lat?.toFixed?.(2)}, ${r.destination_lon?.toFixed?.(2)}`}</td>
                    <td>{Math.round(r.distance_km)} km</td>
                    <td>{r.duration_min}</td>
                    <td>
                      <span
                        className={`rounded-full px-2 py-0.5 text-xs ${
                          risk === "Bajo"
                            ? "bg-emerald-100 text-emerald-800"
                            : risk === "Medio"
                            ? "bg-amber-100 text-amber-800"
                            : "bg-rose-100 text-rose-800"
                        }`}
                      >
                        {risk}
                      </span>
                    </td>
                  </tr>
                );
              })}
              {recentRoutes.length === 0 && (
                <tr className="border-t text-slate-500"><td className="py-2" colSpan={5}>Sin rutas recientes.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

/* ===========================
   STOCK
   =========================== */
function StockPage() {
  const [sku, setSku] = useState("SKU001");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function consultar() {
    if (!sku.trim()) return;
    setLoading(true);
    setErr("");
    setData(null);
    try {
      const res = await api("/stock/consultar", { method: "POST", body: { sku: sku.trim() } });
      setData(res);
    } catch {
      setErr("No se pudo obtener el stock. Intente nuevamente.");
    } finally {
      setLoading(false);
    }
  }

  const totalStock = data?.inventario?.reduce((acc, r) => acc + (Number(r.stock) || 0), 0) ?? 0;
  const bodegas = data?.inventario?.length ?? 0;
  const bajos = data?.inventario?.filter((r) => String(r.estado).toUpperCase() === "BAJO_STOCK").length ?? 0;

  return (
    <section className="min-h-[88vh] bg-slate-50 py-10">
      <div className="max-w-6xl mx-auto bg-white shadow-sm rounded-2xl border border-slate-200 overflow-hidden">
        {/* Encabezado */}
        <div className="bg-slate-100 border-b border-slate-200 px-6 py-5 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="bg-white p-2 rounded-xl shadow-sm border border-slate-300">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-slate-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"
                  d="M3 7l9-4 9 4M3 7l9 4m0 0 9-4M12 11v10m-9-6 9 4 9-4" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-semibold text-slate-900">Consultar Stock</h1>
              <p className="text-sm text-slate-600">
                Disponibilidad por bodega para un SKU específico.
              </p>
            </div>
          </div>

          <div className="flex gap-2">
            <input
              className="rounded-lg border border-slate-300 px-3 py-2 text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-400"
              value={sku}
              onChange={(e) => setSku(e.target.value)}
              placeholder="Ej: SKU001"
            />
            <button
              onClick={consultar}
              disabled={loading || !sku.trim()}
              className="rounded-lg bg-sky-600 hover:bg-sky-700 text-white px-4 py-2 font-medium disabled:opacity-50 transition-all"
            >
              {loading ? "Consultando..." : "Consultar"}
            </button>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-slate-200 text-center">
          <div className="py-4">
            <div className="text-xs uppercase text-slate-500 font-medium">Total Stock</div>
            <div className="text-xl font-semibold text-slate-800">{totalStock}</div>
          </div>
          <div className="py-4">
            <div className="text-xs uppercase text-slate-500 font-medium">Bodegas con inventario</div>
            <div className="text-xl font-semibold text-slate-800">{bodegas}</div>
          </div>
          <div className="py-4">
            <div className="text-xs uppercase text-slate-500 font-medium">Bajo Stock</div>
            <div className={`text-xl font-semibold ${bajos > 0 ? "text-amber-600" : "text-emerald-600"}`}>{bajos}</div>
          </div>
        </div>

        {/* Resultados */}
        <div className="p-6">
          {err && (
            <p className="text-rose-600 bg-rose-50 border border-rose-200 rounded-lg px-3 py-2 text-sm">
              {err}
            </p>
          )}

          {loading && (
            <div className="flex items-center gap-2 text-slate-600 text-sm">
              <svg className="h-5 w-5 animate-spin text-sky-400" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
              Consultando inventario...
            </div>
          )}

          {data && data.inventario?.length > 0 && (
            <div className="rounded-xl border border-slate-200 overflow-hidden mt-4">
              <div className="flex items-center justify-between px-4 py-2 bg-slate-50 border-b border-slate-200">
                <p className="text-sm text-slate-700">
                  Resultado para <span className="font-semibold text-slate-900">{data.sku}</span>
                </p>
                <button
                  onClick={() => {
                    const rows = [
                      ["Bodega", "Stock", "Estado"],
                      ...(data.inventario || []).map((r) => [r.bodega, r.stock, r.estado]),
                    ];
                    const csv = rows.map((r) => r.join(",")).join("\n");
                    const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = `stock_${data.sku}.csv`;
                    a.click();
                    URL.revokeObjectURL(url);
                  }}
                  className="text-sm border border-slate-300 rounded-md px-3 py-1 hover:bg-slate-100"
                >
                  Exportar CSV
                </button>
              </div>

              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-slate-600">
                  <tr>
                    <th className="text-left py-2 px-4">Bodega</th>
                    <th className="text-left py-2 px-4">Stock</th>
                    <th className="text-left py-2 px-4">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {data.inventario.map((r, i) => (
                    <tr key={i} className="border-t hover:bg-slate-50 transition-colors">
                      <td className="py-2 px-4">{r.bodega}</td>
                      <td className="py-2 px-4">{r.stock}</td>
                      <td className="py-2 px-4">
                        <span
                          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                            r.estado === "BAJO_STOCK"
                              ? "bg-amber-100 text-amber-700"
                              : "bg-emerald-100 text-emerald-700"
                          }`}
                        >
                          {r.estado}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {data && !data.inventario?.length && (
            <p className="text-slate-500 text-sm mt-3">No se encontraron bodegas para este SKU.</p>
          )}
        </div>
      </div>
    </section>
  );
}

/* ===========================
   MAP PREVIEW (Leaflet en iframe)
   =========================== */
function MapPreview({ path = [] }) {
  const coords = Array.isArray(path)
    ? path
        .filter((p) => Array.isArray(p) && p.length >= 2)
        .map(([lat, lon]) => [Number(lat), Number(lon)])
        .filter(([lat, lon]) => Number.isFinite(lat) && Number.isFinite(lon))
    : [];

  if (coords.length < 2) {
    return (
      <div className="w-full h-[360px] grid place-items-center text-slate-500 text-sm">
        No hay trayecto para mostrar.
      </div>
    );
  }

  const html = `<!doctype html><html><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>html,body,#map{height:100%;margin:0}.leaflet-container{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,'Helvetica Neue',Arial}</style>
</head><body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
  const coords = ${JSON.stringify(coords)};
  const map = L.map('map', { zoomControl: true });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19, attribution:'&copy; OpenStreetMap'}).addTo(map);
  const latlngs = coords.map(c => L.latLng(c[0], c[1]));
  const poly = L.polyline(latlngs, { weight: 4, color: '#2563eb' }).addTo(map);
  map.fitBounds(poly.getBounds(), { padding: [22,22] });
  L.marker(latlngs[0]).addTo(map).bindPopup('Origen').openPopup();
  L.marker(latlngs[latlngs.length-1]).addTo(map).bindPopup('Destino');
</script>
</body></html>`;

  return (
    <iframe
      title="map"
      className="w-full h-[420px] rounded-xl border border-slate-200"
      srcDoc={html}
      sandbox="allow-scripts allow-same-origin"
    />
  );
}

/* ===========================
   RUTAS (estilo Stock)
   =========================== */
function RutasPage() {
  const [originAddr, setOriginAddr] = useState("Santiago, Chile");
  const [destAddr, setDestAddr] = useState("Viña del Mar, Chile");
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function geocodeDireccion(q) {
    const r = await fetch(`${API_BASE}/routes/geocode?q=` + encodeURIComponent(q));
    if (!r.ok) throw new Error(`No se pudo geocodificar "${q}"`);
    return r.json(); // { lat, lon }
  }

  async function calcular() {
    setLoading(true);
    setErr("");
    setRes(null);
    try {
      const [o, d] = await Promise.all([geocodeDireccion(originAddr), geocodeDireccion(destAddr)]);
      const body = { origin: { lat: o.lat, lon: o.lon }, destination: { lat: d.lat, lon: d.lon } };
      const data = await api(`/routes/optimize?origin_text=${encodeURIComponent(originAddr)}&destination_text=${encodeURIComponent(destAddr)}`, { method: "POST", body });
      setRes(data);
    } catch (e) {
      setErr(e.message || "Error al calcular la ruta");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mx-auto max-w-6xl">
      <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-sm">
        <div className="flex items-center gap-3 p-4 md:p-5 bg-slate-50/70">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-white ring-1 ring-slate-200">
            <svg width="22" height="22" viewBox="0 0 24 24" className="text-slate-600">
              <path fill="currentColor" d="M19 3a3 3 0 0 1 3 3c0 2.5-3 5.5-3 5.5S16 8.5 16 6a3 3 0 0 1 3-3m0 1.5A1.5 1.5 0 1 0 20.5 6A1.5 1.5 0 0 0 19 4.5M7 4a3 3 0 0 1 3 3c0 2.5-3 5.5-3 5.5S4 9.5 4 7a3 3 0 0 1 3-3m0 1.5A1.5 1.5 0 1 0 8.5 7A1.5 1.5 0 0 0 7 5.5M6 17a3 3 0 0 1 3 3c0 2.5-3 5.5-3 5.5S3 22.5 3 20a3 3 0 0 1 3-3m0 1.5A1.5 1.5 0 1 0 7.5 20A1.5 1.5 0 0 0 6 18.5" />
            </svg>
          </div>
          <div>
            <h2 className="text-xl md:text-2xl font-semibold text-slate-900">Optimización de Ruta</h2>
            <p className="text-sm text-slate-500">Geocodificamos tus direcciones y calculamos el mejor trayecto.</p>
          </div>
        </div>

        <div className="p-4 md:p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div className="rounded-xl ring-1 ring-slate-200 bg-white p-4">
              <h3 className="font-medium text-slate-800 mb-3">Origen</h3>
              <label className="block text-sm text-slate-600 mb-1">Dirección</label>
              <input
                className="w-full rounded-xl border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-sky-300"
                placeholder="Ej: Av. Libertador Bernardo O'Higgins 1111, Santiago"
                value={originAddr}
                onChange={(e) => setOriginAddr(e.target.value)}
              />
            </div>

            <div className="rounded-xl ring-1 ring-slate-200 bg-white p-4">
              <h3 className="font-medium text-slate-800 mb-3">Destino</h3>
              <label className="block text-sm text-slate-600 mb-1">Dirección</label>
              <input
                className="w-full rounded-xl border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-sky-300"
                placeholder="Ej: 14 Norte 555, Viña del Mar"
                value={destAddr}
                onChange={(e) => setDestAddr(e.target.value)}
              />
            </div>
          </div>

          <button
            onClick={calcular}
            disabled={loading}
            className="mt-4 rounded-xl bg-sky-600 px-4 py-2 text-white hover:bg-sky-700 disabled:opacity-50"
          >
            {loading ? "Calculando…" : "Calcular ruta"}
          </button>

          {err && <p className="mt-3 text-rose-600">{err}</p>}
        </div>

        {res && (
          <div className="px-4 md:px-6 pb-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
              <div className="rounded-xl ring-1 ring-slate-200 bg-white p-4">
                <h3 className="font-medium text-slate-800 mb-3">Resumen</h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div className="rounded-lg bg-slate-50 p-3">
                    <div className="text-slate-500">Distancia</div>
                    <div className="mt-1 text-lg font-semibold">{res.distance_km} km</div>
                  </div>
                  <div className="rounded-lg bg-slate-50 p-3">
                    <div className="text-slate-500">Duración</div>
                    <div className="mt-1 text-lg font-semibold">{res.duration_hms || res.duration_min}</div>
                  </div>
                  <div className="rounded-lg bg-slate-50 p-3">
                    <div className="text-slate-500">Peajes</div>
                    <div className="mt-1 text-lg font-semibold">{formatCLP(res.toll_cost_clp ?? (Number(res.toll_cost || 0) * 1000))}</div>
                  </div>
                  <div className="rounded-lg bg-slate-50 p-3">
                    <div className="text-slate-500">Riesgo</div>
                    <div className="mt-1 text-lg font-semibold">{res.risk_score}</div>
                  </div>
                </div>
              </div>

              <div className="lg:col-span-2 rounded-xl ring-1 ring-slate-200 bg-white p-2">
                <MapPreview path={res.path?.coords || []} />
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

/* ===========================
   INCIDENTES
   =========================== */
function IncidentMap({ lat, lon }) {
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
    return (
      <div className="w-full h-[320px] grid place-items-center text-slate-500 text-sm">
        No fue posible renderizar el mapa.
      </div>
    );
  }

  const html = `<!doctype html><html><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>html,body,#map{height:100%;margin:0}.leaflet-container{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,'Helvetica Neue',Arial}</style>
</head><body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
  const lat = ${Number(lat)}, lon = ${Number(lon)};
  const map = L.map('map');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19, attribution:'&copy; OpenStreetMap'}).addTo(map);
  const mk = L.marker([lat, lon]).addTo(map);
  mk.bindPopup('Coordenadas<br>Lat: '+lat.toFixed(6)+'<br>Lon: '+lon.toFixed(6));
  map.setView([lat, lon], 14);
</script>
</body></html>`;

  return (
    <iframe
      title="incident-map"
      className="w-full h-[340px] rounded-xl border"
      srcDoc={html}
      sandbox="allow-scripts allow-same-origin"
    />
  );
}

function IncidentSuccess({ resp, onReset }) {
  return (
    <div className="mt-5 rounded-2xl border bg-white shadow-sm">
      <div className="flex items-center gap-3 border-b px-4 py-3 bg-emerald-50">
        <span className="text-emerald-600 text-xl">✅</span>
        <h3 className="text-emerald-700 font-semibold">Incidente registrado con éxito</h3>
        <div className="ml-auto">
          <button
            onClick={onReset}
            className="text-sm rounded-lg border px-3 py-1.5 hover:bg-slate-50"
          >
            Registrar otro
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 p-4">
        <div className="rounded-xl border bg-white p-4">
          <dl className="text-sm space-y-2">
            <div className="grid grid-cols-3">
              <dt className="text-slate-500">ID de Carga</dt>
              <dd className="col-span-2 font-medium">{resp.cargo_id}</dd>
            </div>
            <div className="grid grid-cols-3">
              <dt className="text-slate-500">Vehículo</dt>
              <dd className="col-span-2 font-medium">{resp.vehicle_id}</dd>
            </div>
            <div className="grid grid-cols-3">
              <dt className="text-slate-500">RUT Empleado</dt>
              <dd className="col-span-2 font-medium">{resp.employee_id}</dd>
            </div>
            <div className="grid grid-cols-3">
              <dt className="text-slate-500">Tipo</dt>
              <dd className="col-span-2 font-medium">{resp.type}</dd>
            </div>
            <div className="grid grid-cols-3">
              <dt className="text-slate-500">Descripción</dt>
              <dd className="col-span-2">{resp.description}</dd>
            </div>
            <div className="grid grid-cols-3">
              <dt className="text-slate-500">Lat/Lon</dt>
              <dd className="col-span-2 text-slate-700">
                {resp.location?.lat?.toFixed?.(6)} / {resp.location?.lon?.toFixed?.(6)}
              </dd>
            </div>
            <p className="mt-2 text-xs text-slate-400">Código interno: #{resp.id}</p>
          </dl>
        </div>

        <div className="rounded-xl border bg-white p-2">
          <IncidentMap lat={Number(resp.location?.lat)} lon={Number(resp.location?.lon)} />
        </div>
      </div>
    </div>
  );
}

function IncidentesPage() {
  const TIPOS = ["DESVIO_RUTA", "DETENCION_NO_PROGRAMADA", "ACCIDENTE", "ROBO", "OTRO"];

  const [cargaIdSolo, setCargaIdSolo] = useState("123");
  const [vehicleId, setVehicleId] = useState("CAMION-88");
  const [rut, setRut] = useState("21421299-4");
  const [tipo, setTipo] = useState(TIPOS[0]);
  const [description, setDescription] = useState("Desvío por accidente");
  const [address, setAddress] = useState("Santiago, Chile");

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [resp, setResp] = useState(null);

  const reset = () => {
    setResp(null);
    setErr("");
    setLoading(false);
  };

  async function geocodeDireccion(q) {
    const r = await fetch(`${API_BASE}/routes/geocode?q=` + encodeURIComponent(q));
    if (!r.ok) throw new Error("No se pudo geocodificar la dirección");
    return r.json(); // { lat, lon }
  }

  function normalizaIdCarga(id) {
    const t = String(id).trim();
    return t.toUpperCase().startsWith("CARGA-") ? t.toUpperCase() : `CARGA-${t}`;
  }

  async function enviar() {
    try {
      setLoading(true);
      setErr("");
      setResp(null);

      if (!cargaIdSolo || !vehicleId || !rut || !address) {
        throw new Error("Completa todos los campos requeridos.");
      }

      const loc = await geocodeDireccion(address);
      const payload = {
        cargo_id: normalizaIdCarga(cargaIdSolo),
        vehicle_id: vehicleId,
        employee_id: rut,
        type: tipo,
        description,
        location: { lat: loc.lat, lon: loc.lon },
      };

      const r = await fetch(`${API_BASE}/incidentes/registrar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);

      setResp(await r.json());
    } catch (e) {
      setErr(e.message || "No se pudo registrar el incidente");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mx-auto max-w-6xl">
      <div className="rounded-2xl border bg-white shadow-sm overflow-hidden">
        <div className="flex items-center gap-3 border-b bg-slate-50/70 px-4 py-3">
          <span className="text-slate-600 text-xl">🚨</span>
          <div>
            <h2 className="text-xl font-semibold text-slate-900">Registrar Incidente</h2>
            <p className="text-sm text-slate-500">
              Completa los datos del evento. Geocodificaremos la dirección automáticamente.
            </p>
          </div>
        </div>

        <div className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block text-sm">
              <span className="text-slate-600">ID de Carga</span>
              <input
                className="mt-1 w-full rounded-xl border px-3 py-2"
                placeholder="123"
                value={cargaIdSolo}
                onChange={(e) => setCargaIdSolo(e.target.value)}
              />
              <span className="block mt-1 text-xs text-slate-500">
                Se enviará como <b>{normalizaIdCarga(cargaIdSolo)}</b>
              </span>
            </label>

            <label className="block text-sm">
              <span className="text-slate-600">Vehículo</span>
              <input
                className="mt-1 w-full rounded-xl border px-3 py-2"
                placeholder="CAMION-88"
                value={vehicleId}
                onChange={(e) => setVehicleId(e.target.value)}
              />
            </label>

            <label className="block text-sm">
              <span className="text-slate-600">RUT</span>
              <input
                className="mt-1 w-full rounded-xl border px-3 py-2"
                placeholder="21421299-4"
                value={rut}
                onChange={(e) => setRut(e.target.value)}
              />
            </label>

            <label className="block text-sm">
              <span className="text-slate-600">Tipo de incidente</span>
              <select
                className="mt-1 w-full rounded-xl border px-3 py-2 bg-white"
                value={tipo}
                onChange={(e) => setTipo(e.target.value)}
              >
                {TIPOS.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </label>

            <div className="md:col-span-2">
              <label className="block text-sm">
                <span className="text-slate-600">Descripción</span>
                <textarea
                  className="mt-1 w-full rounded-xl border px-3 py-2"
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </label>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm">
                <span className="text-slate-600">Dirección exacta</span>
                <input
                  className="mt-1 w-full rounded-xl border px-3 py-2"
                  placeholder="Ej: Av. Libertador Bernardo O'Higgins 1111, Santiago"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                />
                <span className="block mt-1 text-xs text-slate-500">
                  Se geocodificará a coordenadas automáticamente antes de registrar.
                </span>
              </label>
            </div>
          </div>

          <div className="mt-4 flex items-center gap-3">
            <button
              onClick={enviar}
              disabled={loading}
              className="rounded-xl bg-sky-600 px-4 py-2 text-white hover:bg-sky-700 disabled:opacity-50"
            >
              {loading ? "Registrando…" : "Registrar"}
            </button>
            {err && <p className="text-rose-600 text-sm">{err}</p>}
          </div>
        </div>
      </div>

      {resp && <IncidentSuccess resp={resp} onReset={reset} />}
    </section>
  );
}

/* ===========================
   ASIGNACIONES (NUEVA PÁGINA)
   =========================== */
function AsignacionesPage() {
  // Formulario
  const [cargoId, setCargoId] = useState("CARGA-1001");
  const [responsableRut, setResponsableRut] = useState("21.421.299-4");
  const [vehiculoId, setVehiculoId] = useState("CAMION-12");
  const [origen, setOrigen] = useState("Bodega Central, Santiago");
  const [destino, setDestino] = useState("Cliente XYZ, Viña del Mar");
  const [fechaHora, setFechaHora] = useState("");
  const [prioridad, setPrioridad] = useState("MEDIA");
  const [notas, setNotas] = useState("");

  // Estado
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [okMsg, setOkMsg] = useState("");

  // Listado
  const [items, setItems] = useState([]);
  const [loadingList, setLoadingList] = useState(false);

  function normalizaCarga(id) {
    const t = String(id || "").trim().toUpperCase();
    return t.startsWith("CARGA-") ? t : `CARGA-${t}`;
    }

  async function fetchAsignaciones() {
    try {
      setLoadingList(true);
      setError("");
      const data = await api("/asignaciones", { method: "GET" });
      setItems(Array.isArray(data) ? data : (data?.items || []));
    } catch (e) {
      setError(e.message || "No se pudieron cargar las asignaciones");
    } finally {
      setLoadingList(false);
    }
  }

  useEffect(() => {
    fetchAsignaciones();
  }, []);

  async function crearAsignacion() {
    try {
      setSubmitting(true);
      setError("");
      setOkMsg("");

      if (!cargoId || !responsableRut || !vehiculoId || !origen || !destino) {
        throw new Error("Completa todos los campos requeridos.");
      }

      const payload = {
        // Campos actuales del backend
        cargo_id: normalizaCarga(cargoId),
        vehicle_id: vehiculoId,
        prioridad: prioridad,
        origen,
        destino,
        fecha_hora: fechaHora || null, // ISO 8601 o null
        notas: notas || "",
        // Alias legacy para compatibilidad con versiones previas del backend
        employee_id: responsableRut,
        origin_address: origen,
        destination_address: destino,
        priority: prioridad,
        scheduled_at: fechaHora || null,
      };

      await api("/asignaciones", { method: "POST", body: payload });
      setOkMsg("✅ Asignación creada correctamente.");
      // limpiar mínimos
      setNotas("");
      // refrescar listado
      fetchAsignaciones();
    } catch (e) {
      setError(e.message || "No se pudo crear la asignación");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="mx-auto max-w-6xl">
      <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-sm">
        {/* Header */}
        <div className="flex items-center gap-3 p-4 md:p-5 bg-slate-50/70">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-white ring-1 ring-slate-200">
            <svg width="22" height="22" viewBox="0 0 24 24" className="text-slate-600">
              <path fill="currentColor" d="M3 7h8v10H3zM13 7h8v6h-8zM13 15h8v2h-8z" />
            </svg>
          </div>
          <div>
            <h2 className="text-xl md:text-2xl font-semibold text-slate-900">Asignar carga</h2>
            <p className="text-sm text-slate-500">Define responsable, vehículo y direcciones.</p>
          </div>
        </div>

        {/* Formulario */}
        <div className="p-4 md:p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block text-sm">
              <span className="text-slate-600">ID Carga</span>
              <input
                className="mt-1 w-full rounded-xl border px-3 py-2"
                value={cargoId}
                onChange={(e) => setCargoId(e.target.value)}
                placeholder="CARGA-1001"
              />
              <span className="block mt-1 text-xs text-slate-500">
                Se enviará como <b>{normalizaCarga(cargoId)}</b>
              </span>
            </label>

            <label className="block text-sm">
              <span className="text-slate-600">RUT Responsable</span>
              <input
                className="mt-1 w-full rounded-xl border px-3 py-2"
                value={responsableRut}
                onChange={(e) => setResponsableRut(e.target.value)}
                placeholder="21.421.299-4"
              />
            </label>

            <label className="block text-sm">
              <span className="text-slate-600">Vehículo</span>
              <input
                className="mt-1 w-full rounded-xl border px-3 py-2"
                value={vehiculoId}
                onChange={(e) => setVehiculoId(e.target.value)}
                placeholder="CAMION-12"
              />
            </label>

            <label className="block text-sm">
              <span className="text-slate-600">Prioridad</span>
              <select
                className="mt-1 w-full rounded-xl border px-3 py-2 bg-white"
                value={prioridad}
                onChange={(e) => setPrioridad(e.target.value)}
              >
                <option value="ALTA">ALTA</option>
                <option value="MEDIA">MEDIA</option>
                <option value="BAJA">BAJA</option>
              </select>
            </label>

            <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className="block text-sm">
                <span className="text-slate-600">Origen</span>
                <input
                  className="mt-1 w-full rounded-xl border px-3 py-2"
                  value={origen}
                  onChange={(e) => setOrigen(e.target.value)}
                  placeholder="Bodega Central, Santiago"
                />
              </label>

              <label className="block text-sm">
                <span className="text-slate-600">Destino</span>
                <input
                  className="mt-1 w-full rounded-xl border px-3 py-2"
                  value={destino}
                  onChange={(e) => setDestino(e.target.value)}
                  placeholder="Cliente XYZ, Viña del Mar"
                />
              </label>
            </div>

            <label className="block text-sm">
              <span className="text-slate-600">Fecha y hora (opcional)</span>
              <input
                type="datetime-local"
                className="mt-1 w-full rounded-xl border px-3 py-2"
                value={fechaHora}
                onChange={(e) => setFechaHora(e.target.value)}
              />
            </label>

            <div className="md:col-span-2">
              <label className="block text-sm">
                <span className="text-slate-600">Notas (opcional)</span>
                <textarea
                  className="mt-1 w-full rounded-xl border px-3 py-2"
                  rows={3}
                  value={notas}
                  onChange={(e) => setNotas(e.target.value)}
                />
              </label>
            </div>
          </div>

          <div className="mt-4 flex items-center gap-3">
            <button
              onClick={crearAsignacion}
              disabled={submitting}
              className="rounded-xl bg-sky-600 px-4 py-2 text-white hover:bg-sky-700 disabled:opacity-50"
            >
              {submitting ? "Creando…" : "Crear asignación"}
            </button>
            {error && <p className="text-rose-600 text-sm">{error}</p>}
            {okMsg && <p className="text-emerald-600 text-sm">{okMsg}</p>}
          </div>
        </div>

        {/* Listado */}
        <div className="px-4 md:px-6 pb-6">
          <h3 className="font-medium text-slate-800 mb-3">Asignaciones recientes</h3>

          {loadingList ? (
            <p className="text-sm text-slate-500">Cargando…</p>
          ) : items.length === 0 ? (
            <p className="text-sm text-slate-500">No hay asignaciones registradas.</p>
          ) : (
            <div className="rounded-xl border border-slate-200 overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-slate-600">
                  <tr>
                    <th className="text-left py-2 px-4">Carga</th>
                    <th className="text-left py-2 px-4">Responsable</th>
                    <th className="text-left py-2 px-4">Vehículo</th>
                    <th className="text-left py-2 px-4">Origen</th>
                    <th className="text-left py-2 px-4">Destino</th>
                    <th className="text-left py-2 px-4">Prioridad</th>
                    <th className="text-left py-2 px-4">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((a, i) => (
                    <tr key={a.id || i} className="border-t hover:bg-slate-50">
                      <td className="py-2 px-4">{a.cargo_id}</td>
                      <td className="py-2 px-4">{a.responsable?.rut || a.employee_id}</td>
                      <td className="py-2 px-4">{a.vehicle_id}</td>
                      <td className="py-2 px-4">{a.origen || a.origin_address}</td>
                      <td className="py-2 px-4">{a.destino || a.destination_address}</td>
                      <td className="py-2 px-4">
                        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                          (a.priority || a.prioridad) === "ALTA" ? "bg-rose-100 text-rose-700"
                          : (a.priority || a.prioridad) === "MEDIA" ? "bg-amber-100 text-amber-700"
                          : "bg-slate-100 text-slate-700"
                        }`}>
                          {a.priority || a.prioridad || prioridad}
                        </span>
                      </td>
                      <td className="py-2 px-4">
                        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                          (a.status || a.estado) === "EN_CURSO" ? "bg-amber-100 text-amber-700"
                          : (a.status || a.estado) === "ENTREGADA" ? "bg-emerald-100 text-emerald-700"
                          : "bg-slate-100 text-slate-700"
                        }`}>
                          {(a.status || a.estado || "ASIGNADA")}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

/* ===========================
   HISTÓRICO: INCIDENTES
   =========================== */
function IncidentesHistPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  async function fetchAll() {
    try {
      setLoading(true);
      setError("");
      const data = await api("/incidentes?limit=50");
      setItems(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e.message || "No se pudieron cargar los incidentes");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchAll(); }, []);

  async function removeItem(id) {
    if (!id) return;
    if (!confirm("¿Eliminar este incidente?")) return;
    try {
      setDeletingId(id);
      const r = await fetch(`${API_BASE}/incidentes/${id}`, { method: 'DELETE' });
      if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
      setItems((arr) => arr.filter((x) => x.id !== id));
    } catch (e) {
      setError(e.message || "No se pudo eliminar");
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <section className="mx-auto max-w-6xl">
      <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-sm">
        <div className="flex items-center justify-between p-4 md:p-5 bg-slate-50/70">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-white ring-1 ring-slate-200">
              <span className="text-slate-600">🚨</span>
            </div>
            <div>
              <h2 className="text-xl md:text-2xl font-semibold text-slate-900">Histórico de Incidentes</h2>
              <p className="text-sm text-slate-500">Últimos registrados</p>
            </div>
          </div>
          <button
            onClick={fetchAll}
            disabled={loading}
            className="rounded-xl border border-slate-300 bg-white px-3 py-1.5 text-sm hover:bg-slate-50 disabled:opacity-50"
          >
            {loading ? "Actualizando…" : "Actualizar"}
          </button>
        </div>

        <div className="p-4 md:p-6">
          {error && <p className="text-sm text-rose-600 mb-2">{error}</p>}
          <div className="overflow-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-500">
                  <th className="py-2 px-3">Fecha</th>
                  <th className="py-2 px-3">Tipo</th>
                  <th className="py-2 px-3">Carga</th>
                  <th className="py-2 px-3">Vehículo</th>
                  <th className="py-2 px-3">RUT</th>
                  <th className="py-2 px-3">Descripción</th>
                  <th className="py-2 px-3">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {items.map((i) => (
                  <tr key={i.id} className="border-t">
                    <td className="py-2 px-3">{i.created_at ? new Date(i.created_at).toLocaleString() : ""}</td>
                    <td className="py-2 px-3">{i.type}</td>
                    <td className="py-2 px-3">{i.cargo_id}</td>
                    <td className="py-2 px-3">{i.vehicle_id}</td>
                    <td className="py-2 px-3">{i.employee_id}</td>
                    <td className="py-2 px-3 max-w-[360px] truncate" title={i.description || ""}>{i.description}</td>
                    <td className="py-2 px-3">
                      <button
                        onClick={() => removeItem(i.id)}
                        disabled={deletingId === i.id}
                        className="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50 disabled:opacity-50"
                      >
                        {deletingId === i.id ? 'Eliminando…' : 'Eliminar'}
                      </button>
                    </td>
                  </tr>
                ))}
                {items.length === 0 && (
                  <tr className="border-t text-slate-500"><td className="py-3 px-3" colSpan={7}>Sin incidentes.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ===========================
   HISTÓRICO: RUTAS
   =========================== */
function RutasHistPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  async function fetchAll() {
    try {
      setLoading(true);
      setError("");
      const data = await api("/routes/recent?limit=50");
      setItems(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e.message || "No se pudo cargar el historial");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchAll(); }, []);

  async function removeItem(id) {
    if (!id) return;
    if (!confirm("¿Eliminar esta ruta del historial?")) return;
    try {
      setDeletingId(id);
      const r = await fetch(`${API_BASE}/routes/recent/${id}`, { method: 'DELETE' });
      if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
      setItems((arr) => arr.filter((x) => x.id !== id));
    } catch (e) {
      setError(e.message || "No se pudo eliminar");
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <section className="mx-auto max-w-6xl">
      <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-sm">
        <div className="flex items-center justify-between p-4 md:p-5 bg-slate-50/70">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-white ring-1 ring-slate-200">
              <svg width="22" height="22" viewBox="0 0 24 24" className="text-slate-600"><path fill="currentColor" d="M13 19V9l3 3l7-7l-1.5-1.5L16 9l-3-3H3v13z"/></svg>
            </div>
            <div>
              <h2 className="text-xl md:text-2xl font-semibold text-slate-900">Histórico de Rutas</h2>
              <p className="text-sm text-slate-500">Origen y destino</p>
            </div>
          </div>
          <button
            onClick={fetchAll}
            disabled={loading}
            className="rounded-xl border border-slate-300 bg-white px-3 py-1.5 text-sm hover:bg-slate-50 disabled:opacity-50"
          >
            {loading ? "Actualizando…" : "Actualizar"}
          </button>
        </div>

        <div className="p-4 md:p-6">
          {error && <p className="text-sm text-rose-600 mb-2">{error}</p>}
          <div className="overflow-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-500">
                  <th className="py-2 px-3">Origen</th>
                  <th className="py-2 px-3">Destino</th>
                  <th className="py-2 px-3">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {items.map((r) => (
                  <tr key={r.id} className="border-t">
                    <td className="py-2 px-3">{r.origin_text || `${r.origin_lat?.toFixed?.(2)}, ${r.origin_lon?.toFixed?.(2)}`}</td>
                    <td className="py-2 px-3">{r.destination_text || `${r.destination_lat?.toFixed?.(2)}, ${r.destination_lon?.toFixed?.(2)}`}</td>
                    <td className="py-2 px-3">
                      <button
                        onClick={() => removeItem(r.id)}
                        disabled={deletingId === r.id}
                        className="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50 disabled:opacity-50"
                      >
                        {deletingId === r.id ? 'Eliminando…' : 'Eliminar'}
                      </button>
                    </td>
                  </tr>
                ))}
                {items.length === 0 && (
                  <tr className="border-t text-slate-500"><td className="py-3 px-3" colSpan={3}>Sin rutas guardadas.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ===========================
   APP ROOT
   =========================== */
export default function App() {
  const [user, setUser] = useState(null);

  return (
    <BrowserRouter>
      {!user ? (
        <Routes>
          <Route path="*" element={<Login onLogin={setUser} />} />
        </Routes>
      ) : (
        <Shell user={user} onLogout={() => setUser(null)}>
          <Routes>
            <Route path="/" element={<Navigate to="/home" replace />} />
            <Route path="/home" element={<HomePage user={user} />} />
            <Route path="/stock" element={<StockPage />} />
            <Route path="/rutas" element={<RutasPage />} />
            <Route path="/incidentes" element={<IncidentesPage />} />
            <Route path="/incidentes/historial" element={<IncidentesHistPage />} />
            <Route path="/rutas/historial" element={<RutasHistPage />} />
            <Route path="/asignaciones" element={<AsignacionesPage />} />
            <Route path="*" element={<Navigate to="/home" replace />} />
          </Routes>
        </Shell>
      )}
    </BrowserRouter>
  );
}
