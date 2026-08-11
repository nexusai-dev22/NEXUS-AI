function Dashboard() {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>Dashboard</h1>
          <p>Centro de control de NEXUS AI</p>
        </div>

        <div className="estado">
          <span className="estado-punto"></span>
          Sistema Online
        </div>
      </header>

      <section className="tarjetas">
        <div className="tarjeta">
          <h3>IA</h3>
          <strong>Activa</strong>
          <p>NEXUS AI está funcionando correctamente.</p>
        </div>

        <div className="tarjeta">
          <h3>Robots</h3>
          <strong>0</strong>
          <p>Robots conectados actualmente.</p>
        </div>

        <div className="tarjeta">
          <h3>Visión</h3>
          <strong>Lista</strong>
          <p>Sistema de visión preparado.</p>
        </div>

        <div className="tarjeta">
          <h3>Proyectos</h3>
          <strong>0</strong>
          <p>Proyectos activos.</p>
        </div>
      </section>

      <section className="actividad">
        <h2>Actividad del sistema</h2>

        <div className="actividad-item">
          <span>●</span>
          <div>
            <strong>Sistema iniciado</strong>
            <p>NEXUS AI está listo para trabajar.</p>
          </div>
        </div>

        <div className="actividad-item">
          <span>●</span>
          <div>
            <strong>Frontend conectado</strong>
            <p>La interfaz React está funcionando correctamente.</p>
          </div>
        </div>

        <div className="actividad-item">
          <span>●</span>
          <div>
            <strong>Backend</strong>
            <p>Preparado para conectar con FastAPI.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
