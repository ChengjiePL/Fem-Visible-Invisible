import "./App.css";
import Barra from "./components/Barra";
import Datos from "./components/Datos";

function App() {
  return (
    <div className="app-container">
      <Barra />
      <main className="main-content">
        <Datos />
      </main>
    </div>
  );
}
export default App;
