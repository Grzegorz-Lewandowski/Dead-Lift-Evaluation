function InstructionCard() {
  return (
    <section className="card instruction-card">
      <h2>Jak przygotować nagranie?</h2>

      <div className="instruction-grid">
        <div>
          <strong>1. Ustaw kamerę z boku</strong>
          <p>Najlepiej tak, aby cała sylwetka i sztanga były widoczne.</p>
        </div>

        <div>
          <strong>2. Nagraj całą serię</strong>
          <p>Film powinien obejmować pozycję startową, podnoszenie i opuszczanie.</p>
        </div>

        <div>
          <strong>3. Prześlij film</strong>
          <p>System wykryje powtórzenia i oceni wybrane elementy techniki.</p>
        </div>
      </div>
    </section>
  )
}

export default InstructionCard