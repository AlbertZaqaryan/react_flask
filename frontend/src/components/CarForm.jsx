import { useEffect, useState } from "react";

const EMPTY = {
  make: "",
  model: "",
  year: new Date().getFullYear(),
  color: "",
  price: "",
  mileage: 0,
  available: true,
};

export default function CarForm({ initial, onSubmit, onCancel }) {
  const [form, setForm] = useState(EMPTY);

  useEffect(() => {
    setForm(initial ? { ...EMPTY, ...initial } : EMPTY);
  }, [initial]);

  const change = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({ ...f, [name]: type === "checkbox" ? checked : value }));
  };

  const submit = (e) => {
    e.preventDefault();
    onSubmit({
      ...form,
      year: Number(form.year),
      price: Number(form.price),
      mileage: Number(form.mileage),
    });
    if (!initial) setForm(EMPTY);
  };

  return (
    <form className="car-form" onSubmit={submit}>
      <h2>{initial ? "Edit car" : "Add a car"}</h2>
      <div className="grid">
        <label>
          Make
          <input name="make" value={form.make} onChange={change} required />
        </label>
        <label>
          Model
          <input name="model" value={form.model} onChange={change} required />
        </label>
        <label>
          Year
          <input name="year" type="number" value={form.year} onChange={change} required />
        </label>
        <label>
          Color
          <input name="color" value={form.color || ""} onChange={change} />
        </label>
        <label>
          Price ($)
          <input name="price" type="number" step="0.01" value={form.price} onChange={change} required />
        </label>
        <label>
          Mileage
          <input name="mileage" type="number" value={form.mileage} onChange={change} />
        </label>
        <label className="checkbox">
          <input name="available" type="checkbox" checked={form.available} onChange={change} />
          Available
        </label>
      </div>
      <div className="actions">
        <button type="submit" className="primary">
          {initial ? "Save changes" : "Add car"}
        </button>
        {initial && (
          <button type="button" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
