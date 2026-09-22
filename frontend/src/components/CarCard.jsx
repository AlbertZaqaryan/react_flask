const money = (v) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(v);

export default function CarCard({ car, onEdit, onDelete }) {
  return (
    <div className="car-card">
      <div className="car-head">
        <h3>
          {car.make} {car.model}
        </h3>
        <span className={`badge ${car.available ? "in" : "out"}`}>
          {car.available ? "Available" : "Sold"}
        </span>
      </div>
      <dl>
        <div>
          <dt>Year</dt>
          <dd>{car.year}</dd>
        </div>
        <div>
          <dt>Color</dt>
          <dd>{car.color || "—"}</dd>
        </div>
        <div>
          <dt>Mileage</dt>
          <dd>{Number(car.mileage).toLocaleString()} mi</dd>
        </div>
        <div>
          <dt>Price</dt>
          <dd className="price">{money(car.price)}</dd>
        </div>
      </dl>
      <div className="actions">
        <button onClick={() => onEdit(car)}>Edit</button>
        <button className="danger" onClick={() => onDelete(car)}>
          Delete
        </button>
      </div>
    </div>
  );
}
