import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import "./login.css";

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setErrorMessage("Por favor, preencha todos os campos.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/login", { email, password });
      localStorage.setItem("token", response.data.access_token);
      setErrorMessage("");
      navigate("/dashboard");
    } catch (error) {
      console.error('Login failed:', error);
      setErrorMessage("Erro ao conectar com o servidor.");
      alert('Login failed: ' + (error.response?.data?.message || 'Unknown error'));
    }
  };

  return (
    <div id="body">
      <h1>Entrar na sua conta</h1>
      <form id="loginForm" onSubmit={handleSubmit}>
        <input
          type="email"
          id="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          aria-label="Email"
        />
        <input
          type="password"
          id="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          aria-label="Senha"
        />
        <button type="submit" id="loginButton">
          Entrar
        </button>
      </form>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <h2>
        Não tem uma conta? <a href="/register">Registrar</a>
      </h2>
    </div>
  );
}

export default Login;
