import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [ingredientes, setIngredientes] = useState("");
  const [permitirExtras, setPermitirExtras] = useState(false);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [cardapio, setCardapio] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setCarregando(true);
    setErro("");
    setCardapio(null);

    try {
      const resposta = await axios.post("http://localhost:5000/gerar-cardapio", {
        ingredientes,
        permitir_extras: permitirExtras,
      });
      setCardapio(resposta.data);
    } catch (err) {
      console.error(err);
      setErro("Erro ao gerar o cardápio. Verifique se o servidor está rodando.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="container">
      <h1>🍽️ Gerador de Receitas: IA Receitas 2000</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Ingredientes disponíveis:
          <textarea
            value={ingredientes}
            onChange={(e) => setIngredientes(e.target.value)}
            placeholder="Ex: arroz, frango, batata, feijão..."
            rows={3}
          />
        </label>

        <label className="checkbox">
          <input
            type="checkbox"
            checked={permitirExtras}
            onChange={() => setPermitirExtras(!permitirExtras)}
          />
          Permitir extras básicos (sal, óleo, alho, cebola)
        </label>

        <button type="submit" disabled={carregando}>
          {carregando ? "Gerando..." : "Gerar cardápio"}
        </button>
      </form>

      {erro && <p className="erro">{erro}</p>}

      {cardapio && (
        <div className="resultado">
          <h2>📅 Cardápio da Semana</h2>
          {Object.entries(cardapio).map(([dia, refeicoes]) => (
            <div key={dia} className="dia">
              <h3>{dia}</h3>
              {refeicoes.map((r, idx) => (
                <div key={idx} className="refeicao">
                  <h4>{idx === 0 ? "Almoço" : "Jantar"}: {r.nome}</h4>
                  <p><strong>Ingredientes:</strong> {r.ingredientes.join(", ")}</p>
                  <p><strong>Modo de preparo:</strong> {r.modo_preparo}</p>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
