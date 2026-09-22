// All requests go to /api, which nginx (prod) or the Vite proxy (dev) forwards
// to the FastAPI backend.
const BASE = "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body.detail) message = body.detail;
    } catch (_) {
      /* ignore non-JSON error bodies */
    }
    throw new Error(message);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const getCars = (search = "") =>
  request(`/cars${search ? `?search=${encodeURIComponent(search)}` : ""}`);

export const createCar = (car) =>
  request("/cars", { method: "POST", body: JSON.stringify(car) });

export const updateCar = (id, car) =>
  request(`/cars/${id}`, { method: "PUT", body: JSON.stringify(car) });

export const deleteCar = (id) =>
  request(`/cars/${id}`, { method: "DELETE" });
