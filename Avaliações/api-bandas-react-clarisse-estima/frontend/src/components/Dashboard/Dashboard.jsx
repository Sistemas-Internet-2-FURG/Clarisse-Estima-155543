import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./dashboard.css";

const Dashboard = () => {
  const [bandas, setBandas] = useState([]);
  const [integrantes, setIntegrantes] = useState([]);
  const navigate = useNavigate();

  const fetchWithAuth = async (endpoint, method = "GET") => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Você precisa estar logado para acessar esta página.");
      navigate("/login");
      return null;
    }

    try {
      const response = await fetch(endpoint, {
        method,
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        return await response.json();
      } else {
        const errorData = await response.json();
        alert(errorData.message || `Erro ao acessar ${endpoint}.`);
        return null;
      }
    } catch (error) {
      alert("Erro de conexão com o servidor.");
      return null;
    }
  };

  const fetchBandas = async () => {
    const bandasData = await fetchWithAuth("http://localhost:5000/bandas");
    if (bandasData) setBandas(bandasData);
  };

  const fetchIntegrantes = async () => {
    const integrantesData = await fetchWithAuth("http://localhost:5000/integrantes");
    if (integrantesData) setIntegrantes(integrantesData);
  };

  useEffect(() => {
    fetchBandas();
    fetchIntegrantes();
  }, []);

  return (
    <div id="body">
      <h1>Lista de bandas</h1>
      <ul id="bandasList">
        {bandas.map((banda) => (
          <li key={banda[0]}>{banda[1]}</li>
        ))}
      </ul>

      <h1>Lista de integrantes</h1>
      <ul id="integrantesList">
        {integrantes.map((integrante) => (
          <li key={integrante[0]}>
            {integrante[1]} - {integrante[2]}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;