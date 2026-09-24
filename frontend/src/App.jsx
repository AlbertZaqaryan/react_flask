import { useCallback, useEffect, useState } from "react";
import { createCar, deleteCar, getCars, updateCar } from "./api";
import CarCard from "./components/CarCard.jsx";
import CarForm from "./components/CarForm.jsx";

export default function App() {
  const [cars, setCars] = useState([]);
  const [search, setSearch] = useState("");
  const [editing, setEditing] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async (term = "") => {
    setLoading(true);
    setError("");
    try {
      setCars(await getCars(term));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleSearch = (e) => {
    e.preventDefault();
    load(search);
  };

  const handleCreate = async (car) => {
    try {
      await createCar(car);
      await load(search);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleUpdate = async (car) => {
    try {
      await updateCar(editing.id, car);
      setEditing(null);
      await load(search);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleDelete = async (car) => {
    if (!window.confirm(`Delete ${car.make} ${car.model}?`)) return;
    try {
      await deleteCar(car.id);
      await load(search);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>🚗 Car Club Misaki mot</h1>
        <form className="search" onSubmit={handleSearch}>
          <input
            placeholder="Search make or model..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit">Search</button>
        </form>
      </header>

      {error && <div className="error">{error}</div>}

      <CarForm
        key={editing ? editing.id : "new"}
        initial={editing}
        onSubmit={editing ? handleUpdate : handleCreate}
        onCancel={() => setEditing(null)}
      />

      {loading ? (
        <p className="muted">Loading...</p>
      ) : cars.length === 0 ? (
        <p className="muted">No cars found.</p>
      ) : (
        <div className="car-grid">
          {cars.map((car) => (
            <CarCard
              key={car.id}
              car={car}
              onEdit={setEditing}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
