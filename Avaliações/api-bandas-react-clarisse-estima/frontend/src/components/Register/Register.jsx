import React, { useState } from "react";
import "./register.css";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!email || !password) {
      showMessage("Por favor, preencha todos os campos.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        showMessage(data.message, true);
      } else {
        showMessage(data.message || "Erro no registro.");
      }
    } catch (error) {
      showMessage("Erro ao conectar com o servidor.");
    }
  };

  const showMessage = (message, redirect = false) => {
    alert(message);
    if (redirect) window.location.href = "/";
  };

  return (
    <div id="body">
      <h1>Cadastrar novo usuário</h1>

      <form id="registerForm" onSubmit={handleSubmit}>
        <input
          type="email"
          id="registerEmail"
          placeholder="Email"
          required
          aria-label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          id="registerPassword"
          placeholder="Senha"
          required
          aria-label="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div id="buttons">
          <button type="submit" id="registerButton">Registrar</button>
          <button type="button" id="cancelRegister" onClick={() => (window.location.href = "/")}>Cancelar</button>
        </div>
      </form>
    </div>
  );
};

export default Register;
